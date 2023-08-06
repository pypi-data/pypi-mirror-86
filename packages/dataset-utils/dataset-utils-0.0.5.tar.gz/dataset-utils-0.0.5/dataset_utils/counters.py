"""
Simple way to implement counters via sqlite

sample usage:
python3 -m dataset_utils.counters increment_cli counters.sqlite completed

"""
import dataset
from dataset_utils.sqlite import connect, get_or_create, ConnectMode
import fire
import time
from typing import Union


def get_or_create_counters(db: Union[str, dataset.Database], table_name: str):
    return get_or_create(
        db, table_name,
        columns=['epoch', 'value'],
        types={'epoch': 'float', 'value': 'integer'},
        index=['epoch']
    )


class SqliteCounter(object):
    def __init__(self, db, mode=ConnectMode.JOURNAL):
        if isinstance(db, str):
            self.db = connect(db, mode=mode)
        else:
            assert isinstance(db, dataset.Database)
            self.db = db
        self.table_cache = {}

    def increment(self, counter, value=1):
        if counter in self.table_cache:
            table = self.table_cache[counter]
        else:
            table = get_or_create_counters(self.db, counter)
        table.insert({'ts': time.time(), 'value': value})

    def window_sum(self, counter, lookback):
        ts = time.time() - lookback
        out = self.db.query(f'select sum(value) from {counter} where ts >= {ts};')
        row = next(out)
        sum_val = row['sum(value)']
        return sum_val

    def prune(self):
        # TODO - implement later
        pass


def increment(dbpath: str, table_name: str, value=1):
    sc = SqliteCounter(dbpath)
    sc.increment(table_name, value=value)


def window_gte(db: str, table_name: str, lookback, value):
    sc = SqliteCounter(db, mode=ConnectMode.READ_ONLY)
    sum_val = sc.window_sum(table_name, lookback)
    assert sum_val >= value


if __name__ == '__main__':
    fire.Fire()
