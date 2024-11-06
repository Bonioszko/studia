-- hive.hql
CREATE TABLE fifa_players_analysis (
                                       league STRING,
                                       average_age DOUBLE,
                                       average_wage DOUBLE,
                                       player_count INT
)
    COMMENT 'leagues'
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ';'
    STORED AS TEXTFILE
    LOCATION 'tmp/hive/hive/part-r-00000';

LOAD DATA INPATH '${input_path}' INTO TABLE fifa_players_analysis;

-- Analyze the data
SELECT
    AVG(average_age) AS overall_average_age,
    AVG(average_wage) AS overall_average_wage
FROM
    fifa_players_analysis;