"""
This function is mean to clean up the mistakes in 38 rows. The mistake involved
a newline character (\n) not being interpreted correctly by the csv. Some
information from rows wasn't moved to the next line, resulting in messy rows for
year X and missing rows for the year X + 1. Both errors are addressed here.

The main assumption is that all data remained the same for the subsequent year,
except in the YEAR column.

NOTE:
1. You must supply your own database access credentials.
2. The script should only be run once, because it keeps adds rows every run.
"""


# coding: utf-8
import mysql.connector
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def getLocalServer(user, password, host, database):
    server = mysql.connector.connect(user=user,
                                     password=password,
                                     host=host,
                                     database=database)
    return server


def deleteRow(server, year, orispl, unit):
    query = """
            DELETE
            FROM   plants
            WHERE  YEAR = {}
                   AND ORISPL_CODE = {}
                   AND UNITID = '{}'
            """.format(str(year), orispl, str(unit))
    cursor = server.cursor()
    cursor.execute(query)  # execute query
    server.commit()  # accept the change
    return


def deleteIncompleteRows(server, rows_df):
    for i, row in rows_df.iterrows():
        orispl, unit, year = row[3:6]
        deleteRow(server, year, orispl, unit)

def main(user, password, host, database):
    server = getLocalServer(user, password, host, database)  # connect to db
    toInsert = pd.read_csv('rowsToAdd.csv', encoding="ISO-8859-1")  # read in cleaned data
    deleteIncompleteRows(server, toInsert)  # delete messed up rows if they exist

    # add back rows for this year and the next
    engine = create_engine("mysql://{}:{}@localhost/widap".format(user, password))  # different type of connection
    con = engine.connect()
    toInsert.to_sql(name='plants', con=con, if_exists='append', index=False)
    toInsert['YEAR'] += 1  # use same data for next year
    toInsert.to_sql(name='plants', con=con, if_exists='append', index=False)


user="apark2"
password="Mindinmsight@1"
host="127.0.0.1"
database="widap"
main(user, password, host, database)
