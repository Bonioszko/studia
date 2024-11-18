

CREATE EXTERNAL TABLE IF NOT EXISTS league_data (
    league_id INT,
    average_age DOUBLE,
    average_wage DOUBLE,
    player_count INT
)
COMMENT 'leagues mapReduce'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
STORED AS TEXTFILE
LOCATION '${input_dir3}';

CREATE EXTERNAL TABLE IF NOT EXISTS league_ext (
    league_id INT,
    league_name STRING,
    league_level INT
)
COMMENT 'leagues'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
STORED AS TEXTFILE
LOCATION '${input_dir4}';

CREATE TABLE IF NOT EXISTS leagues_summary (
    league_id INT,
    league_name STRING,
    league_level INT,
    avg_wage DOUBLE,
    avg_age DOUBLE,
    count_players INT
)
ROW FORMAT SERDE
'org.apache.hadoop.hive.serde2.JsonSerDe'
STORED AS TEXTFILE
LOCATION '${output_dir6}';  

INSERT OVERWRITE TABLE leagues_summary
SELECT 
    league_id,
    league_name,
    league_level,
    avg_wage,
    avg_age,
    count_players
FROM (
    SELECT 
        ld.league_id,
        le.league_name,
        le.league_level,
        ld.average_wage AS avg_wage,
        ld.average_age AS avg_age,
        ld.player_count AS count_players,
        ROW_NUMBER() OVER (PARTITION BY le.league_level ORDER BY ld.average_wage DESC) AS rank
    FROM 
        league_data ld
    JOIN 
        league_ext le ON ld.league_id = le.league_id
) AS RankedLeagues
WHERE 
    rank <= 3
ORDER BY 
    league_level, rank;
