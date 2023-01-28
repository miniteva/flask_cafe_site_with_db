from typing import Tuple, List
from sem4.database.db_context_manager import DBConnection
import datetime


def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.
    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result = tuple()
    schema = []
    with DBConnection(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema


def select_dict(db_config: dict, sql:str):
    with DBConnection(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        result=[]
        schema = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))
    return result


def insert_into(db_config: dict, sql: str):
    with DBConnection(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)


def call_proc(database: dict, proc_name: str, *args):
    with DBConnection(database) as cursor:
        if cursor is None:
            raise ValueError('Курсор не найден')
        param_list = []
        for arg in args:
            print('arg=', arg)
            param_list.append(arg)
        print('param_list=', param_list)
        res = cursor.callproc(proc_name, param_list)
    return res



