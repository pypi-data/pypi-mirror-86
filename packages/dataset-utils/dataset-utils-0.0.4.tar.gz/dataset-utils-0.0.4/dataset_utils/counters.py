"""
Simple way to implement counters via sqlite
"""
import dataset
from dataset_utils.sqlite import connect_ro, get_or_create
import fire
import time


def get_or_create_counters(dbpath: str, table_name: str):
    return get_or_create(
        dbpath, table_name,
        columns=['epoch', 'count'],
        types={'epoch': 'float', 'value': 'integer'},
        index=['epoch']
    )


def ro_counters(dbpath, table_name):
    db = connect_ro(dbpath)
    table = db[table_name]
    return db, table


def prune():
    # TODO - implement later
    pass


def increment(table: dataset.Table, value=1):
    # db, table = get_or_create(db_path, table_name)
    table.insert({'ts': time.time(), 'value': value})


def increment_cli(dbpath: str, table_name: str, value=1):
    db, table = get_or_create_counters(dbpath, table_name)
    increment(table, value=value)


def assert_gte_cli(dbpath: str, table_name: str, lookback, value):
    db, table = ro_counters(dbpath, table_name)
    ts = time.time() - lookback
    out = db.query(f'select sum(value) from {table_name} where ts >= {ts};')
    row = next(out)
    print(row)


if __name__ == '__main__':
    fire.Fire()
