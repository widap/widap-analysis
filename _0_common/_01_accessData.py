### Access Data ###
# This script sets up access to the mySQL database with all Air Markets
# Program Data (AMPD) used in our analysis. You must have an username and
# password to access this data. You can request one by contacting
# Austin at austinpark77@gmail.com.

import mysql.connector
import pandas as pd

## Data connections
# Local
def getLocalServer(user, password, host, database):
    server = mysql.connector.connect(user=user,
                                     password=password,
                                     host=host,
                                     database=database)
    return server

# BigQuery coming soon...


## Commonly used queries
# Heat Rate Curve Data
def getHRCdata(server, orispl, unit, years='all'):
    """
    Retrieves data for heat rate curve analysis.
    Drops NULL values of power output, values where the generating unit was
    off, and non-physical values of CO2 intensity (< 0.35)
    By default, retrieves data for all years. If a subset of years is desired,
    pass the range (starting and stopping year, both inclusive) as a tuple.
    """
    query = """
            SELECT
                gload,
                heat_input,
                CAST(gload as DECIMAL(8))*CAST(op_time as DECIMAL(8)) as gen,
                (CAST(gload as DECIMAL(8))*CAST(op_time as DECIMAL(8)))/(CAST(heat_input as DECIMAL(8))*0.29307107) as efficiency
            FROM
                widap.data
            WHERE
                orispl_code = {} AND unitid = {}
            """.format(orispl, unit)

    if years != 'all':
        query += """
        AND SUBSTR(OP_DATE, 1, 4) >= {}
        AND SUBSTR(OP_DATE, 1, 4) <= {}
        """.format(*years)

    data = pd.read_sql(query, server)
    data = data[data["gload"] > 0.1]
    return data


# CO2I Curve Data
def getCO2Idata(server, orispl, unit, years='all'):
    """
    Retrieves data for CO2 intensity analysis.
    Drops NULL values of power output, values where the generating unit was
    off, and non-physical values of CO2 intensity (< 0.35)
    By default, retrieves data for all years. If a subset of years is desired,
    pass the range (starting and stopping year, both inclusive) as a tuple.
    """
    query = """
            SELECT
                gload,
                CO2_MASS / (gload * op_time) as CO2I
            FROM
                widap.data
            WHERE
                orispl_code = {} AND unitid = {}
            """.format(orispl, unit)

    if years != 'all':
        query += """
        AND SUBSTR(OP_DATE, 1, 4) >= {}
        AND SUBSTR(OP_DATE, 1, 4) <= {}
        """.format(*years)

    data = pd.read_sql(query, server)
    data = data[(data["gload"] > 0.1) & (data["CO2I"] > .35)]
    return data
