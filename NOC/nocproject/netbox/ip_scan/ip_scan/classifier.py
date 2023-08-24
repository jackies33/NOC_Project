


import psycopg2
from .psql_conn import postgresql_connections


def classifier_device_type(dev_type):

    psql = postgresql_connections()
    choices_device_type = psql.postgre_conn_device_type()
    dev_type_clear = int()
    for count in choices_device_type:
        if count[1] == dev_type:
            dev_type_clear = count[0]
    return dev_type_clear


