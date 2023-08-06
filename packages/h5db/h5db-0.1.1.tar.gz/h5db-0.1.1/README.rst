
安装
----

pip install -U h5db

目前测试版本为python3，python2不支持

入门
----

读写数据
^^^^^^^^

例如需要储存和读取下面一个词典

.. code-block:: python

   import h5db
   import numpy as np


   # make sure save_dir exist 
   save_dir = './data'
   save_dat = [['1', np.random.random([10, 1024])], ['2', np.random.random([4, 1024])]]
   h5db.simple_add(save_dir, save_dat)
   print(h5db.simple_search(save_dir, ['1', '2']))

说明
^^^^


#. 
   h5db默认使用简单hash函数将key分成100个部分，存储到100个对应的h5文件，搜索的时候会同时开启100个进程进行搜索，最后返回一个dict类型: {key: value}, 如果没有搜索到，则value是None；

#. 
   对于可以转换成int的类型的key, 默认的hash函数为 int(key) % 100, 对于str类型的key，默认用其sha1值的10位数 % 100；

#. 
   目前主要支持{str: np.ndarray} 和 {str: str}这两种数据类型，其他复杂类型未测试

详细用法
--------

主要的类是H5

.. code-block:: python

   class H5:
       '''
       H5DB的类
       save_dir: h5文件储存目录
       logger_path: logger储存目录
       l1_size: 一级分类个数
       l2_size: 二级分类个数（h5文件中的groups)
       hash_l1: 可以自定义一级hash函数
       hash_l2：可以自定义二级hash函数
       '''

       def __init__(self,
                    save_dir: str = None,
                    logger_path: str = None,
                    l1_size: int = 100,
                    l2_size: int = 2000,
                    hash_l1: callable = None,
                    hash_l2: callable = None):

可以自定义key的hash函数，也可以使用默认的hash函数，默认的hash函数可以见gen_mod_hash和gen_mod_hash_shift

主要作用的两个函数

.. code-block:: python


       def multiple_file_add(self,
                             data_pairs: list,
                             save_prefix: str = 'part.',
                             replacement: bool = False):

replacement：遇到重复的key，value对，是否进行覆盖

默认使用multiprocessing.Manager.dict进行多进程沟通，也可以自己修改代码使用其他框架。
