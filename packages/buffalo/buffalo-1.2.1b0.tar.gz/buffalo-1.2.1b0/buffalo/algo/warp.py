# -*- coding: utf-8 -*-
import time
import json

import numpy as np
from hyperopt import STATUS_OK as HOPT_STATUS_OK

import buffalo.data
from buffalo.misc import aux, log
from buffalo.data.base import Data
from buffalo.algo._warp import CyWARP
from buffalo.evaluate import Evaluable
from buffalo.algo.options import WARPOption
from buffalo.algo.optimize import Optimizable
from buffalo.data.buffered_data import BufferedDataMatrix
from buffalo.algo.base import Algo, Serializable, TensorboardExtention


class WARP(Algo, WARPOption, Evaluable, Serializable, Optimizable, TensorboardExtention):
    """Python implementation for C-WARP.
    """
    def __init__(self, opt_path=None, *args, **kwargs):
        Algo.__init__(self, *args, **kwargs)
        WARPOption.__init__(self, *args, **kwargs)
        Evaluable.__init__(self, *args, **kwargs)
        Serializable.__init__(self, *args, **kwargs)
        Optimizable.__init__(self, *args, **kwargs)
        if opt_path is None:
            opt_path = WARPOption().get_default_option()

        self.logger = log.get_logger('WARP')
        self.opt, self.opt_path = self.get_option(opt_path)
        # TODO:GPU Implementation
        if self.opt.accelerator is True:
            raise NotImplementedError("GPU version WARP is not implemented yet")
        self.obj = CyWARP()

        assert self.obj.init(bytes(self.opt_path, 'utf-8')),\
            'cannot parse option file: %s' % opt_path

        self.data = None
        data = kwargs.get('data')
        data_opt = self.opt.get('data_opt')
        data_opt = kwargs.get('data_opt', data_opt)
        if data_opt:
            self.data = buffalo.data.load(data_opt)
            self.data.create()
        elif isinstance(data, Data):
            self.data = data
        self.logger.info('WARP(%s)' % json.dumps(self.opt, indent=2))
        if self.data:
            self.logger.info(self.data.show_info())
            assert self.data.data_type in ['matrix']

    @staticmethod
    def new(path, data_fields=[]):
        return WARP.instantiate(WARPOption, path, data_fields)

    def set_data(self, data):
        assert isinstance(data, aux.data.Data), 'Wrong instance: {}'.format(type(data))
        self.data = data

    def normalize(self, group='item'):
        if group == 'item' and not self.opt._nrz_Q:
            self.Q = self._normalize(self.Q)
            self.opt._nrz_Q = True
        elif group == 'user' and not self.opt._nrz_P:
            self.P = self._normalize(self.P)
            self.opt._nrz_P = True

    def initialize(self):
        super().initialize()
        assert self.data, 'Data is not setted'
        self.buf = BufferedDataMatrix()
        self.buf.initialize(self.data)
        self.init_factors()

    def init_factors(self):
        header = self.data.get_header()
        self.num_nnz = header['num_nnz']
        for attr_name in ['P', 'Q', 'Qb']:
            setattr(self, attr_name, None)
        self.P = np.random.normal(scale=1.0 / (self.opt.d ** 2),
                                  size=(header['num_users'], self.opt.d)).astype("float32")
        self.Q = np.random.normal(scale=1.0 / (self.opt.d ** 2),
                                  size=(header['num_items'], self.opt.d)).astype("float32")
        self.Qb = np.random.normal(scale=1.0 / (self.opt.d ** 2),
                                   size=(header['num_items'], 1)).astype("float32")
        if not self.opt.use_bias:
            self.Qb *= 0
        self.obj.initialize_model(self.P, self.Q, self.Qb, self.num_nnz)

    def _get_topk_recommendation(self, rows, topk, pool=None):
        p = self.P[rows]
        Qb = self.Qb if self.opt.use_bias else None

        topks = super()._get_topk_recommendation(
            p, self.Q,
            pb=None, Qb=Qb,
            pool=pool, topk=topk, num_workers=self.opt.num_workers)

        return zip(rows, topks)

    def _get_most_similar_item(self, col, topk, pool):
        return super()._get_most_similar_item(col, topk, self.Q, self.opt._nrz_Q, pool)

    def get_scores(self, row_col_pairs):
        rets = {(r, c): self.P[r].dot(self.Q[c]) + self.Qb[c][0] for r, c in row_col_pairs}
        return rets

    def _get_scores(self, row, col):
        scores = (self.P[row] * self.Q[col]).sum(axis=1) + self.Qb[col][0]
        return scores

    def sampling_loss_samples(self):
        users, positives, negatives = [], [], []
        if self.opt.compute_loss_on_training:
            self.logger.info('Sampling loss samples...')
            header = self.data.get_header()
            num_loss_samples = int(header['num_users'] ** 0.5)
            _users = np.random.choice(range(self.P.shape[0]), size=num_loss_samples, replace=False)
            users = []
            positives, negatives = [], []
            for u in _users:
                keys, *_ = self.data.get(u)
                if len(keys) == 0:
                    continue
                seen = set(keys)
                negs = np.random.choice(range(self.Q.shape[0]),
                                        size=len(seen) + 1,
                                        replace=False)
                negs = [n for n in negs if n not in seen]
                users.append(u)
                positives.append(keys[0])
                negatives.append(negs[0])
            self.logger.info('Generated %s loss samples.' % len(users))
        self._sub_samples = [
            np.array(users, dtype=np.int32, order='F'),
            np.array(positives, dtype=np.int32, order='F'),
            np.array(negatives, dtype=np.int32, order='F')
        ]

    def _get_feature(self, index, group='item'):
        if group == 'item':
            return self.Q[index]
        elif group == 'user':
            return self.P[index]
        return None

    def _iterate(self):
        header = self.data.get_header()
        # end = header['num_users']
        update_t, feed_t, updated = 0, 0, 0
        self.buf.set_group('rowwise')
        with log.ProgressBar(log.DEBUG,
                             total=header['num_nnz'], mininterval=30) as pbar:
            start_t = time.time()
            for sz in self.buf.fetch_batch():
                updated += sz
                feed_t += time.time() - start_t
                start_x, next_x, indptr, keys, _ = self.buf.get()
                start_t = time.time()
                self.obj.add_jobs(start_x, next_x, indptr, keys)
                update_t += time.time() - start_t
                pbar.update(sz)
            pbar.refresh()
        self.obj.update_parameters()
        self.logger.debug(f'updated processed({updated}) elapsed(data feed: {feed_t:0.3f} update: {update_t:0.3f}')

    def compute_loss(self):
        return self.obj.compute_loss(self._sub_samples[0],
                                     self._sub_samples[1],
                                     self._sub_samples[2])

    def _prepare_train(self):
        if self.opt.accelerator:
            vdim = self.obj.get_vdim()
            for attr in ["P", "Q"]:
                F = getattr(self, attr)
                if F.shape[1] < vdim:
                    _F = np.empty(shape=(F.shape[0], vdim), dtype=np.float32)
                    _F[:, :F.shape[1]] = F
                    _F[:, self.opt.d:] = 0.0
                    setattr(self, attr, _F)
            indptr, _, batch_size = self.buf.get_indptrs()
            self.obj.set_placeholder(indptr, batch_size)
            self.obj.initialize_model(self.P, self.Q, self.Qb, self.num_nnz, True)
        else:
            self.obj.launch_workers()

    def _finalize_train(self):
        if self.opt.accelerator:
            self.P = self.P[:, :self.opt.d]
            self.Q = self.Q[:, :self.opt.d]
            return 0.0
        else:
            return self.obj.join()

    def train(self):
        self.validation_result = {}
        self.initialize_tensorboard(self.opt.num_iters)
        self.sampling_loss_samples()
        best_loss = 987654321.0
        # initialize placeholder in case of running accelerator otherwise launch workers
        self._prepare_train()
        for i in range(self.opt.num_iters):
            start_t = time.time()
            self._iterate()
            self.obj.wait_until_done()
            loss = self.compute_loss() if self.opt.compute_loss_on_training else 0.0
            metrics = {'train_loss': loss}
            if self.opt.validation and \
               self.opt.evaluation_on_learning and \
               self.periodical(self.opt.evaluation_period, i):
                start_t = time.time()
                self.validation_result = self.get_validation_results()
                vali_t = time.time() - start_t
                val_str = ' '.join([f'{k}:{v:0.5f}' for k, v in self.validation_result.items()])
                self.logger.info(f'Validation: {val_str} Elased {vali_t:0.3f}')
                metrics.update({'val_%s' % k: v
                                for k, v in self.validation_result.items()})
            self.logger.info('Iteration %s: PR-Loss %.3f Elapsed %.3f secs' % (i + 1, loss, time.time() - start_t))
            self.update_tensorboard_data(metrics)
            best_loss = self.save_best_only(loss, best_loss, i)
            if self.early_stopping(loss):
                break
        # reshape factor if using accelerator else join workers
        ret = {'train_loss': self._finalize_train()}
        ret.update({'val_%s' % k: v
                    for k, v in self.validation_result.items()})
        self.finalize_tensorboard()
        return ret

    def _optimize(self, params):
        # TODO: implement
        self._optimize_params = params
        for name, value in params.items():
            assert name in self.opt, 'Unexepcted parameter: {}'.format(name)
            if isinstance(value, np.generic):
                setattr(self.opt, name, value.item())
            else:
                setattr(self.opt, name, value)
        with open(self._temporary_opt_file, 'w') as fout:
            json.dump(self.opt, fout, indent=2)
        assert self.obj.init(bytes(self._temporary_opt_file, 'utf-8')),\
            'cannot parse option file: %s' % self._temporary_opt_file
        self.logger.info(params)
        self.init_factors()
        loss = self.train()
        loss['loss'] = loss.get(self.opt.optimize.loss)
        # TODO: deal with failture of training
        loss['status'] = HOPT_STATUS_OK
        self._optimize_loss = loss
        return loss

    def _get_data(self):
        data = super()._get_data()
        data.extend([('opt', self.opt),
                     ('Q', self.Q),
                     ('Qb', self.Qb),
                     ('P', self.P)])
        return data

    def get_evaluation_metrics(self):
        return ['val_rmse', 'val_ndcg', 'val_map', 'val_accuracy', 'val_error', 'train_loss']
