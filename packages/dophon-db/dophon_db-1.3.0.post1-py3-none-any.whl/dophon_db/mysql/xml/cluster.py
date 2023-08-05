import re

from dophon_logger import *

from dophon_db import properties
from dophon_db.mysql import Connection
from dophon_db.mysql import Pool
from .remote.Cell import Cell
from .core import CurObj

get_logger(eval(properties.log_types)).inject_logger(globals())

obj_manager = {}

# 定义项目路径
project_path = properties.project_root

cluster_manager = {}


def get_manager():
    return cluster_manager


def get_db(path, debug: bool = False, auto_fix: bool = False):
    """

    :param path:
    :param debug:
    :param auto_fix:
    :return:
    """
    x = lambda p: p.split('::')
    if isinstance(path, str):
        from . import mode_assert
        # 切分出别名和路径
        cluster_path = mode_assert('CLUSTER')(x)(path)
        assert len(cluster_path) > 1, '无法解释的路径格式'
        if auto_fix:
            pattern = re.sub(r'\\', r'\\\\', re.sub('/', '\\/', project_path))
            if not re.search(pattern, cluster_path[1]):
                r_path = str(project_path) + str(cluster_path[1])
            else:
                r_path = str(cluster_path[1])
        else:
            r_path = cluster_path[1]
        # 返回预设连接池所生成的数据库对象
        alias_name = cluster_path[0]
        if alias_name in cluster_manager:
            return CurObj(r_path, True, debug, db=cluster_manager[alias_name])
        elif alias_name == 'x':
            # 暂定别名,由结果集定义
            undefined = CurObj(r_path, True, debug)
            db_alias = undefined.sql.alias_for
            assert db_alias, f'结果集别名不存在{db_alias}'
            setattr(undefined, '_pool', cluster_manager[db_alias])
            return undefined
        else:
            raise KeyError(f'别名不存在{alias_name}')
    elif isinstance(path, Cell):
        logger.error('暂不支持远程映射集')
    else:
        raise TypeError('结果集路径类型错误')


def init_cluster_manager():
    if hasattr(properties, 'db_cluster'):
        clusters = properties.db_cluster
        # 初始化分片连接池
        logger.info('初始化分片连接池')
        for cluster in clusters:
            pool = Pool.Pool()
            pool.init_pool(properties.pool_conn_num, Connection.Connection, conn_kwargs=cluster)
            # print(f'{cluster["alias"]}--{pool.cache_conn_kwargs}')
            # print(id(pool))
            cluster_manager[cluster['alias']] = pool
        logger.info('分片连接池初始化完毕')
