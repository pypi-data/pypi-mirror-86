"""
@author  : MG
@Time    : 2020/11/24 11:05
@File    : object.py
@contact : mmmaaaggg@163.com
@desc    : 用于创建数据库表结构
"""
import enum
import threading
import time

import peewee
from peewee import (
    CharField,
    SmallIntegerField,
    Model,
)
# Peewee provides an alternate database implementation
# for using the mysql-connector driver.
# The implementation can be found in playhouse.mysql_ext.
from playhouse.mysql_ext import MySQLConnectorDatabase
from vnpy.trader.setting import get_settings

from quant_vnpy.config import logging

logger = logging.getLogger()


class StrategyStatusEnum(enum.IntEnum):
    Created = 0
    Initialized = 1
    RunPending = 2
    Running = 3
    StopPending = 4
    Stopped = 5


def init_db():
    settings = get_settings("database.")
    keys = {"database", "user", "password", "host", "port"}
    settings = {k: v for k, v in settings.items() if k in keys}
    db = MySQLConnectorDatabase(**settings)
    return db


database = init_db()


class StrategyStatus(Model):
    """
    策略状态信息
    * strategy_name 策略名称
    * status 策略状态
    """
    strategy_name: str = CharField(primary_key=True)
    status: int = SmallIntegerField()

    class Meta:
        database = database
        legacy_table_names = False
        indexes = ((("strategy_name",), True),)
        table_settings = "ENGINE = MEMORY"


def init_models():
    try:
        StrategyStatus.create_table()  # 创建表  # engine='MEMORY'
    except peewee.OperationalError:
        logger.warning("StrategyStatus table already exists!")

    # db.connect()
    # db.create_tables([StrategyStatus])

    return StrategyStatus


def is_db_table_available():
    try:
        return StrategyStatus.table_exists()
    except:
        return False


def set_db_strategy_status(strategy_name, status: int):
    return StrategyStatus.insert(strategy_name=strategy_name, status=status).on_conflict(
        preserve=[StrategyStatus.strategy_name],
        update={StrategyStatus.status: status}
    ).execute()


def get_db_strategy_status(strategy_name) -> int:
    ss: StrategyStatus = StrategyStatus.get_or_none(StrategyStatus.strategy_name == strategy_name)
    if ss is None:
        return -1
    else:
        return ss.status


def _test_record_strategy_status():
    strategy_name = 'asdf11'
    status = StrategyStatusEnum.Running
    set_db_strategy_status(strategy_name=strategy_name, status=status.value)
    ss: StrategyStatus = StrategyStatus.get_or_none(StrategyStatus.strategy_name == strategy_name)
    print(ss, ss.status)
    ss.status = StrategyStatusEnum.Stopped.value
    ss.update()
    print(ss, ss.status)


class StrategyStatusMonitorThread(threading.Thread):
    def __init__(self, name, get_status_func, set_status_func):
        super().__init__(name=name)
        self.daemon = True
        self.get_status_func = get_status_func
        self.set_status_func = set_status_func
        self.lock = threading.Lock()
        self.run_task = is_db_table_available()

    def run(self) -> None:
        if not self.run_task:
            logger.warning("%s thread is not running because run_task == false")
        # 首次启动初始化状态
        status_int_curr = self.get_status_func().value
        set_db_strategy_status(strategy_name=self.name, status=status_int_curr)
        # 记录最新状态并开始循环
        status_int_last = status_int_curr
        while self.run_task:
            time.sleep(1)
            try:
                with self.lock:
                    # 获取当前策略最新状态，检查是否与上一个状态存在变化，否则更新
                    status_int_curr = self.get_status_func().value
                    # 检查数据库状态与上一状态是否一致，否则更新当前策略状态
                    status_int_db = get_db_strategy_status(self.name)

                if status_int_curr != status_int_last:
                    # 检查是否与上一个状态存在变化，否则更新
                    set_db_strategy_status(self.name, status=status_int_curr)
                    status_int_last = status_int_curr
                elif status_int_db != status_int_curr:
                    # 检查数据库状态与上一状态是否一致，否则更新当前策略状态
                    self.set_status_func(StrategyStatusEnum(status_int_db))
                    status_int_last = status_int_db
            except:
                logger.exception("%s Monitor Error", self.name)


def _test_monitor():
    class Stg:
        def __init__(self, name):
            self.name = name
            self.status: StrategyStatusEnum = StrategyStatusEnum.Created
            self.lock: [threading.Lock] = None

        def set_status(self, status: StrategyStatusEnum):
            if self.lock is not None:
                self.lock.acquire()
                print("It's locked")
            try:
                self.status = status
            finally:
                if self.lock is not None:
                    self.lock.release()
                    print("It's released")

        def get_status(self) -> StrategyStatusEnum:
            return self.status

    stg = Stg('test_monitor')
    monitor = StrategyStatusMonitorThread(stg.name, stg.get_status, stg.set_status)
    stg.lock = monitor.lock
    monitor.start()
    time.sleep(2)
    # 初始化状态同步
    assert get_db_strategy_status(stg.name) == stg.status.value == StrategyStatusEnum.Stopped.Created
    stg.status = StrategyStatusEnum.Stopped
    time.sleep(2)
    # 修改策略状态，自动同步数据库
    assert get_db_strategy_status(stg.name) == stg.status.value == StrategyStatusEnum.Stopped.value
    set_db_strategy_status(stg.name, StrategyStatusEnum.Running)
    time.sleep(2)
    # 修改数据库，自动同步当前策略状态
    assert get_db_strategy_status(stg.name) == stg.status.value == StrategyStatusEnum.Running

    monitor.run_task = False
    monitor.join()


if __name__ == "__main__":
    # init_models()
    # _test_record_strategy_status()
    _test_monitor()
