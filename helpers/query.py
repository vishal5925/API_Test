from contextlib import closing

import cx_Oracle

import confighelper


def execute(sql, **kwargs):
    is_update = sql.strip()[:6].upper() in ('UPDATE', 'DELETE', 'INSERT')
    is_select = sql.strip()[:6].upper() in ('SELECT')

    with closing(cx_Oracle.connect(confighelper.instance().oracle_db_connection_string)) as conn:
        with closing(conn.cursor()) as cursor:
            if is_update:
                __execute_update(sql, cursor, conn, **kwargs)
            elif is_select:
                return __execute_select(sql, cursor, **kwargs)
            else :
                __execute_procedure(sql, cursor, **kwargs)


def __execute_update(sql, cursor, conn, **kwargs):
    cursor.execute("set role bss_full identified by bss_full")
    cursor.execute(sql, **kwargs)
    conn.commit()


def __execute_select(sql, cursor, **kwargs):
    #cursor.execute("set role bss_full identified by bss_full")
    cursor.execute(sql, **kwargs)
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def __execute_procedure(sql, cursor, **kwargs):
    cursor.execute("set role bss_full identified by bss_full")
    cursor.callproc(sql)
