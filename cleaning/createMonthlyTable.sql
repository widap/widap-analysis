/*
Code to create a table with quartiles for each numeric type.
Python processing quartiles, then sending back to MySQL.
Used to speed up dashboard analysis by pre-computing quartiles.
*/

CREATE TABLE widap.monthly ( 
	YEAR_MO char(7), 
	STATE char(2), 
	ORISPL_CODE int(11), 
	UNITID char(16), 
	CO2_MASS_min double, 
	CO2_MASS_25 double, 
	CO2_MASS_50 double, 
	CO2_MASS_75 double, 
	CO2_MASS_max double, 
	NOX_MASS_min double, 
	NOX_MASS_25 double, 
	NOX_MASS_50 double, 
	NOX_MASS_75 double, 
	NOX_MASS_max double, 
	SO2_MASS_min double, 
	SO2_MASS_25 double, 
	SO2_MASS_50 double, 
	SO2_MASS_75 double, 
	SO2_MASS_max double, 
	heat_input_min double, 
	heat_input_25 double, 
	heat_input_50 double, 
	heat_input_75 double, 
	heat_input_max double);

/*
CREATE TABLE monthly AS
SELECT
	STATE,
    ORISPL_CODE,
    UNITID,
    CONCAT(SUBSTR(OP_DATE, 1, 4), '_', SUBSTR(OP_DATE, 6, 2)) AS 'YEAR_MONTH',
    -- GLOAD quartiles
    MIN(GLOAD) AS GLOAD_0,
    AS GLOAD_25,
    AS GLOAD_50,
    AS GLOAD_75,
    MAX(GLOAD) AS GLOAD_100,
    -- HEAT_INPUT quartiles
	MIN(HEAT_INPUT) AS HEAT_INPUT_0, /*
    AS HEAT_INPUT_25,
    AS HEAT_INPUT_50,
    AS HEAT_INPUT_75,
    MAX(HEAT_INPUT) AS HEAT_INPUT_100,
    -- CO2_MASS quartiles
	MIN(CO2_MASS) AS CO2_MASS_0, /*
    AS CO2_MASS_25,
    AS CO2_MASS_50,
    AS CO2_MASS_75,
    MAX(CO2_MASS) AS CO2_MASS_100,
    -- SO2_MASS quartiles
	MIN(SO2_MASS) AS SO2_MASS_0, /*
    AS SO2_MASS_25,
    AS SO2_MASS_50,
    AS SO2_MASS_75,
    MAX(SO2_MASS) AS SO2_MASS_100,
    -- NOX_MASS quartiles
	MIN(NOX_MASS) AS NOX_MASS_0, /*
    AS NOX_MASS_25,
    AS NOX_MASS_50,
    AS NOX_MASS_75,
    MAX(NOX_MASS) AS NOX_MASS_100
FROM widap.data
-- GROUP BY YEAR, MONTH
GROUP BY SUBSTR(OP_DATE, 1, 4), SUBSTR(OP_DATE, 6, 2)
);
*/