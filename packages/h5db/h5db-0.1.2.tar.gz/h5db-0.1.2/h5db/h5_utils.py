#!/usr/bin/env python
# coding: utf-8


import h5py
import pickle
from multiprocessing import Process, Manager
import logging
import hashlib
import os


def get_logger(file_path: str = './logger.txt'):

    logging.basicConfig(
        format="%(asctime)s-%(levelname)s-%(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )

    utils_logger = logging.getLogger('h5utils')

    utils_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')

    if file_path is not None:
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        utils_logger.addHandler(file_handler)

    return utils_logger


def isint(value: str):
  try:
    int(value)
    return True
  except ValueError:
    return False


def gen_mod_hash(mod_num: int = 10):
    def mod(key):
        if isint(key):
            return str(int(key) % mod_num)
        else:
            key = int(hashlib.sha1(key.encode()).hexdigest(), 16)
            return str(int(key) % mod_num)

    return mod



def gen_mod_hash_shift(mod_num, shift):
    def mod(key):
        if isint(key):
            sub_key = int(key) // shift
            return str(sub_key % mod_num)
        else:
            key = int(hashlib.sha1(key.encode()).hexdigest(), 16)
            sub_key = key // shift
            return str(sub_key % mod_num)

    return mod



class H5:
    '''
    H5DB的类
    save_dir:<str>
    logger_path:<int>
    :return: 

    '''

    def __init__(self,
                 save_dir: str = None,
                 logger_path: str = None,
                 l1_size: int = 100,
                 l2_size: int = 2000,
                 hash_l1: callable = None,
                 hash_l2: callable = None):
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            raise ValueError('invalid path for save_dir')

        self.logger = get_logger(logger_path)
        self.l1_size = l1_size
        self.l2_size = l2_size
        if hash_l1 is not None:
            self.hash_l1 = hash_l1
        else:
            self.hash_l1 = gen_mod_hash(l1_size)

        if hash_l2 is not None:
            self.hash_l2 = hash_l2
        else:
            self.hash_l2 = gen_mod_hash_shift(l2_size, l2_size)



    @staticmethod
    def add_single_file(filename, data_pairs, hash_fuc):
        hdf5_file = h5py.File(filename, 'a')
        for vid, data in data_pairs:

            key = hash_fuc(vid)
            if key not in hdf5_file:
                hdf5_file.create_group(key)
            if vid in hdf5_file[key]:
                del hdf5_file[key][vid]
            hdf5_file[key].create_dataset(vid, data=data)

        hdf5_file.close()

    @staticmethod
    def search_single_file(filename, vids, hash_fuc, dict_manager):
        if not os.path.exists(filename):
            return
        hdf5_file = h5py.File(filename, 'r',  swmr=True)
        res = []
        for vid in vids:
            key = hash_fuc(vid)
            if key not in hdf5_file:
                res.append([vid, None])
            elif vid not in hdf5_file[key]:
                res.append([vid, None])
            else:
                res.append([vid, hdf5_file[key][vid][()]])

        hdf5_file.close()

        for vid, value in res:
            dict_manager[vid] = value


    def multiple_file_add(self,
                          data_pairs: list,
                          save_prefix: str = 'part.',
                          replacement: bool = False):
        if os.path.exists(os.path.join(self.save_dir, 'idx.bin')):
            self.idx = pickle.loads(open(os.path.join(self.save_dir, 'idx.bin'), 'rb').read())
        else:
            self.idx = set([])


        args = {}
        for vid, _ in data_pairs:
            try:
                if (vid not in self.idx) or replacement:
                    l1_key = self.hash_l1(vid)
                    save_name = save_prefix + l1_key + '.h5'
                    if save_name not in args:
                        args[save_name] = []
                    args[save_name].append([vid, _])
                    self.idx.add(vid)

            except ValueError:
                self.logger.warning('invalid type for vid: {}'.format(vid))

        pool = []

        for key in args.keys():
            fn = os.path.join(self.save_dir, key)
            num = len(args[key])
            args_ = (fn, args[key], self.hash_l2, )
            pool.append(Process(target=H5.add_single_file, args=args_))

            self.logger.info('Filename {} will write {} lines'.format(fn, num))

        for p in pool:
            p.start()
        for p in pool:
            p.join()

        self.logger.info('dumping vids to idx.bin')

        with open(os.path.join(self.save_dir, 'idx.bin'), 'wb') as f:
            f.write(pickle.dumps(self.idx))

        self.logger.info('all Processes finished!')


    def search(self,
               vids: list,
               save_prefix: str = 'part.',
               max_parallel: int = None):
        with Manager() as manager:
            dict_manager = manager.dict()
            groups = {}
            for vid in vids:
                try:
                    key = self.hash_l1(vid)
                    fn = os.path.join(self.save_dir, save_prefix + key + '.h5')
                    if fn not in groups:
                        groups[fn] = []
                    groups[fn].append(vid)
                except ValueError:
                    self.logger.info('invalid key: {}'.format(vid))

            pool = []
            for fn in groups.keys():
                sub_list = groups[fn]
                if max_parallel is None:
                    args = (fn, sub_list, self.hash_l2, dict_manager, )
                    pool.append(Process(target=H5.search_single_file, args=args))
                else:
                    batch_size = max(int(len(sub_list) / max_parallel * self.l1_size), 1)
                    for _ in range(0, len(sub_list), batch_size):
                        args = (fn, sub_list[_: _ + batch_size], self.hash_l2, dict_manager, )
                        pool.append(Process(target=H5.search_single_file, args=args))

            for p in pool:
                p.start()
            for p in pool:
                p.join()

            result = [(k, dict_manager[k]) for k in dict_manager.keys()]

        return result

    def search_single_vid(self,
                          vid: str,
                          save_prefix: str = 'part.'):

        return self.search([vid], save_prefix)



def simple_search(save_dir: str,
                  vids: list,
                  max_parallel: int = None,
                  l1_size: int = 100):

    h5 = H5(save_dir, l1_size=l1_size)
    return h5.search(vids, max_parallel=max_parallel)



def simple_add(save_dir: str,
               data_pairs: list,
               l1_size: int = 100,
               l2_size: int = 2000):
    h5 = H5(save_dir, l1_size=l1_size)
    h5.multiple_file_add(data_pairs)
