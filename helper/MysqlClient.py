import pymysql
import logging
from helper.RentalCarException import *
from enum import Enum
import inspect
from contextlib import closing
import os
from helper.Constant import *

class EnumQueryType(Enum):
    SELECT_FIRST = 0
    SELECT_ALL = 1
    SELECT_SCALAR = 2
    INSERT = 101
    UPDATE = 102
    DELETE = 103


class MysqlClient():
    """Class for implementing mysql database"""
    __host = None
    __user = None
    __password = None
    __db = None
    __port = None
    __charset = None
    __autocommit = None

    def __init__(self):
        self.__host = DATABASE.HOST
        self.__user = DATABASE.USERNAME
        self.__password = DATABASE.PASSWORD
        self.__db = DATABASE.DATABASE
        self.__port = DATABASE.PORT
        self.__charset = DATABASE.CHARSET
        self.__autocommit = DATABASE.AUTOCOMMIT

    def connect(self):
        try:
            return pymysql.connect(host=self.__host, user=self.__user, passwd=self.__password,
                                   db=self.__db, port=int(self.__port), charset=self.__charset,
                                   autocommit=self.__autocommit, cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            logging.error("Failed to Connect Mysql Database | host = %S", self.__host, exc_info=1)
            raise DatabaseException("Failed to Connect Mysql Database")

    def execute_fetch_scalar(self, query, data, raise_no_data_error):
        """Executes provided query and returns single scalar value as output
        :param query: SQL query to be executed
        :param data: collection of parameters to be used along with query as list or tuple
        :param raise_no_data_error: bool, if True raises Metastore exception in case query returns empty output
        :return: singleton value as output of the query
        """
        return self.__execute_query(query, data, EnumQueryType.SELECT_SCALAR, inspect.stack()[1][3],
                                    raise_no_data_error)

    def execute_fetch_first_dict(self, query, data, raise_no_data_error):
        """Executes provided query and returns one row output as dictionary
        :param query: SQL query to be executed
        :param data: collection of parameters to be used along with query as list or tuple
        :param raise_no_data_error: bool, if True raises Metastore exception in case query returns empty output
        :return: dict with column names as keys and content as values for single row
        """
        return self.__execute_query(query, data, EnumQueryType.SELECT_FIRST, inspect.stack()[1][3],
                                    raise_no_data_error)

    def execute_fetch_all_dict(self, query, data, raise_no_data_error):
        """Executes provided query and returns outputs all rows as dictionary
        :param query: SQL query to be executed
        :param data: collection of parameters to be used along with query as list or tuple
        :param raise_no_data_error: bool, if True raises Metastore exception in case query returns empty output
        :return: dict with column names as keys and content as values for all rows
        """
        return self.__execute_query(query, data, EnumQueryType.SELECT_ALL, inspect.stack()[1][3],
                                    raise_no_data_error)

    def execute_insert(self, query, data, raise_no_data_error):
        """Executes insert operation and returns count of affected rows
        :param query: INSERT INTO query to be executed
        :param data: collection of parameters to be used along with query as list or tuple
        :param raise_no_data_error: bool, if True raises Metastore exception in case query returns empty output
        :return: int count of affected rows
        """
        return self.__execute_query(query, data, EnumQueryType.INSERT, inspect.stack()[1][3], raise_no_data_error)

    def execute_update(self, query, data, raise_no_affected_row_error):
        """Executes update operation and returns count of affected rows
        :param query: UPDATE query to be executed
        :param data: collection of parameters to be used along with query as list or tuple
        :param raise_no_affected_row_error: bool, if True raises Metastore exception in case query returns empty output
        :return: int count of affected rows
        """
        return self.__execute_query(query, data, EnumQueryType.UPDATE, inspect.stack()[1][3],
                                    raise_no_affected_row_error)

    def execute_delete(self, query, data, raise_no_data_error):
        """Executes delete operation and returns count of affected rows
        :param query: delete query to be executed
        :param data: collection of parameters to be used along with query as list or tuple
        :param raise_no_data_error: bool, if True raises Metastore exception in case query returns empty output
        :return: int count of affected rows
        """
        return self.__execute_query(query, data, EnumQueryType.DELETE, inspect.stack()[1][3], raise_no_data_error)

    def __execute_query(self, query, data, enum_query_type, calling_function, raise_no_affected_rows_error):
        """Private method that executes provided query and returns count of affected rows
        :param query: SQL query to be executed
        :param data: ollection of parameters to be used along with query as list or tuple
        :param enum_query_type: object of class EnumQueryType based on kind of query to be executed
        :param calling_function: Name of the method from where this private method is being accessed
        :param raise_no_affected_rows_error: bool, if True raises Metastore exception in case query returns empty output
        :return: int count of affected rows
        """
        try:
            with closing(self.connect()) as con:
                with closing(con.cursor()) as cur:
                    cur.execute(query, data)
                    if enum_query_type == EnumQueryType.SELECT_SCALAR:
                        result = cur.fetchone()
                        if result is not None:
                            result = next(iter(result.values()))
                    elif enum_query_type == EnumQueryType.SELECT_FIRST:
                        result = cur.fetchone()
                    elif enum_query_type == EnumQueryType.SELECT_ALL:
                        result = cur.fetchall()
                    elif enum_query_type == EnumQueryType.INSERT or enum_query_type == EnumQueryType.UPDATE or enum_query_type == EnumQueryType.DELETE:
                        result = cur.rowcount
                    rowcount = cur.rowcount

            if raise_no_affected_rows_error:
                if result is None or rowcount == 0:
                    logging.warning('No data found | caller_function: %s | query: %s | parameters %s',
                                    calling_function, query, str(data))
                    raise NoDataException('No data found')

            return result
        except NoDataException as nde:
            raise nde
        except Exception as ex:
            logging.error('Mysql exception | caller_function: %s | query: %s | parameters %s',
                          calling_function, query, str(data), exc_info=1)
            raise DatabaseException('Database exception %s', ex)

    def execute_transaction(self, query_dict):
        """Executes provided collection of queries as SQL transaction. Results are committed only if all queries execute
        successfully.
        :param query_dict: dict containing SQL query as keys and parameters as values
        :return: None
        """
        try:
            con = self.connect()
            logging.info('Begin transaction')
            cur = con.cursor()
            for key, value in query_dict.items():
                cur.execute(key, value)
                logging.info('Rows affected: %s | caller_function: %s | query: %s | parameters %s',
                             cur.rowcount, inspect.stack()[1][3], key, str(value))
            con.commit()
            cur.close()
            con.close()
            logging.info('Commit transaction')
            return True
        except Exception as ex:
            logging.error('Mysql exception | caller_function: %s | query_dict: %s'
                          , inspect.stack()[1][3], str(query_dict), exc_info=1)
            if con.open():
                con.rollback()
                cur.close()
                con.close()
            raise DatabaseException('Database exception %s', ex)