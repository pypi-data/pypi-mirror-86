"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from datetime import datetime
from typing import List, Dict

import pandas as pd
from ibats_utils.mess import datetime_2_str
from vnpy.app.portfolio_strategy import StrategyTemplate as StrategyTemplateBase
from vnpy.trader.constant import Direction, Offset
from vnpy.trader.object import BarData

from quant_vnpy.backtest.cta_strategy.run import get_output_file_path
from quant_vnpy.config import logging
from quant_vnpy.db.orm import StrategyStatusEnum, StrategyStatusMonitorThread


class StrategyTemplate(StrategyTemplateBase):

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.logger = logging.getLogger(strategy_name)
        self.send_order_list = []
        self.current_bars = None
        self.bar_count = 0
        self._strategy_status = StrategyStatusEnum.Created
        self._strategy_status_monitor = StrategyStatusMonitorThread(
            self.__class__.__name__ if self.strategy_name is None else self.strategy_name,
            self._get_strategy_status, self._set_strategy_status)
        self._lock = self._strategy_status_monitor.lock

    def _set_strategy_status(self, status: StrategyStatusEnum):
        if self._lock is not None:
            self._lock.acquire()

        try:
            if self._strategy_status == status:
                return
            if status == StrategyStatusEnum.Running and self._strategy_status != StrategyStatusEnum.Created:
                self.on_start()
        finally:
            if self._lock is not None:
                self._lock.release()

    def _get_strategy_status(self) -> StrategyStatusEnum:
        return self._strategy_status

    def on_init(self) -> None:
        super().on_init()
        self.bar_count = 0
        self._set_strategy_status(StrategyStatusEnum.Initialized)
        self._strategy_status_monitor.start()

    def on_start(self) -> None:
        super().on_start()
        self._set_strategy_status(StrategyStatusEnum.Running)
        self.put_event()

    def on_bars(self, bars: Dict[str, BarData]) -> None:
        super().on_bars(bars)
        self.current_bars = bars
        self.bar_count += 1

    def send_order(self,
                   vt_symbol: str,
                   direction: Direction,
                   offset: Offset,
                   price: float,
                   volume: float,
                   lock: bool = False
                   ) -> List[str]:
        current_pos = self.get_pos(vt_symbol)
        order_datetime = self.current_bars[vt_symbol].datetime if vt_symbol in self.current_bars else None
        if offset == Offset.OPEN:
            self.write_log(
                f"{vt_symbol:>11s} {direction.value} {offset.value:4s} {price:.1f} "
                f"{current_pos:+d} {volume:+d} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {vt_symbol} {direction.value} {offset.value:4s} {price:.1f} "
                f"{current_pos:+d} {volume:+d}"
            )
        else:
            self.write_log(
                f"{vt_symbol:>11s} {direction.value} {offset.value:4s} {price:.1f} "
                f"      {current_pos:+d} {volume:+d} "
                if order_datetime is None else
                f"{datetime_2_str(order_datetime)} {vt_symbol} {direction.value} {offset.value:4s} {price:.1f} "
                f"      {current_pos:+d} {volume:+d}"
            )

        if order_datetime is None:
            order_datetime = datetime.now()

        self.send_order_list.append({
            "datetime": order_datetime,
            "vt_symbol": vt_symbol, "direction": direction.value,
            "offset": offset.value, "price": price, "volume": volume
        })
        return super(StrategyTemplate, self).send_order(vt_symbol, direction, offset, price, volume, lock)

    def on_stop(self):
        super().on_stop()
        order_df = pd.DataFrame([{
            "datetime": _.datetime,
            "symbol": _.symbol,
            "direction": _.direction.value,
            "offset": _.offset.value,
            "price": _.price,
            "volume": _.volume,
            "order_type": _.type.value,
        } for _ in self.send_order_list])
        file_path = get_output_file_path(
            "data", "orders.csv",
            root_folder_name=self.strategy_name,
        )
        order_df.to_csv(file_path)
        self.logger.info('运行期间下单情况明细：\n%s', order_df)
        self._strategy_status = StrategyStatusEnum.Stopped
        self.put_event()

    def write_log(self, msg: str):
        msg = f"{self.strategy_name} {msg}"
        super().write_log(msg)
        self.logger.info(msg)


if __name__ == "__main__":
    pass
