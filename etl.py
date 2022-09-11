from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, hour, dayofmonth, weekofyear, month, year, dayofweek, monotonically_increasing_id, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear
from pyspark.sql.types import IntegerType,TimestampType


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

def process_song_data(spark, input_data, output_data):
    '''
    Extract, Load and Transform song data from S3, generating
    dimension tables songs and artists, and storing the dimension
    tables in S3 as parquet files.

    INPUTS:
        spark (object)       : Spark session object
        input_data (string)  : S3 path to the original song data
        output_data (string) : S3 storage path for the dimension tables
    
    OUTPUTS:
        None
    '''
   
    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'

    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create the songs table
    songs_table = df.select('song_id', 'title', 'artist_id',
                            'year', 'duration') \
                    .dropDuplicates()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist_id') \
                     .parquet(os.path.join(output_data, 'songs/songs.parquet'), 'overwrite')

    # extract columns to create the artists table
    artists_table = df.select('artist_id', 'artist_name', 'artist_location',
                              'artist_latitude', 'artist_longitude') \
                      .withColumnRenamed('artist_name', 'name') \
                      .withColumnRenamed('artist_location', 'location') \
                      .withColumnRenamed('artist_latitude', 'latitude') \
                      .withColumnRenamed('artist_longitude', 'longitude') \
                      .dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data, 'artists/artists.parquet'), 'overwrite')

     # create temp view to be used to join on to create the fact table
    df.createOrReplaceTempView('song_data')


def process_log_data(spark, input_data, output_data):
    '''
    Extract, Load and Transform log data from S3, generating
    dimensions tables users, artists, and songplays, storing the dimension
    tables in S3 as parquet files.
    
    INPUTS:
        spark (object)       : Spark session object
        input_data (string)  : S3 path to the original song data
        output_data (string) : S3 storage path for the dimension tables
    
    OUTPUTS:
       None
    '''  
    # get filepath to log data file
    log_data = input_data + '/log_data/*/*/*.json'

    # read log data file
    df = spark.read.json(log_data)

     # filter by actions for song plays
    df = df.filter(df.page == "NextSong")

    # cast userId column
    df = df.withColumn('user_id', df.userId.cast(IntegerType()))

    # extract columns to create the users table
    users_table = df.select('user_id','firstName', 'lastName', 'gender', 'level') \
                    .withColumnRenamed('firstName', 'first_name') \
                    .withColumnRenamed('lastName', 'last_name') \
                    .dropDuplicates()
    
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users/users.parquet'), 'overwrite')

    # add time columns
    get_timestamp = udf(lambda epoch: datetime.fromtimestamp(epoch/1000),TimestampType())
    df = df.withColumn("start_time",get_timestamp("ts")) \
            .withColumn('hour',hour('start_time')) \
            .withColumn('day',dayofmonth('start_time')) \
            .withColumn('week',weekofyear('start_time')) \
            .withColumn('month',month('start_time')) \
            .withColumn('year',year('start_time')) \
            .withColumn('weekday',dayofweek('start_time')) 
    
    # extract columns to create the time table
    time_table = df.select('start_time','hour', 'day', 'week', 'month','year','weekday').dropDuplicates()

    # write time table to parquet files
    time_table.write.partitionBy('year', 'month') \
            .parquet(os.path.join(output_data, 'time/time.parquet'), 'overwrite')

    # create data set from songs data
    song_data_df = spark.sql('SELECT DISTINCT song_id, title, artist_id, artist_name, duration FROM song_data')

    # join data sets
    joined_tables = df.join(song_data_df, (df.song == song_data_df.title) & (df.artist == song_data_df.artist_name) & (df.length == song_data_df.duration), 'inner') 
    
    # extract columns to create the songsplays table
    songsplays_table = joined_tables.select(
        monotonically_increasing_id().alias('songplay_id'),
        col('start_time'),
        col('user_id'),
        col('level'),
        col('song_id'),
        col('artist_id'),
        col('sessionId').alias('session_id'),
        col('location'),
        col('userAgent').alias('user_agent'),
        col('year'),
        col('month')) 

    # write songsplays table to parquet files
    songsplays_table.write.partitionBy('year', 'month') \
        .parquet(os.path.join(output_data, 'songsplays/songsplays.parquet'), 'overwrite')

def main():
    '''
    Create spark session, run process_song_data() and process_log_data()
    to generate parquet-formatted fact table songplays and dimension
    tables users, songs, artists, and time, and to store all tables on S3
    '''
    spark = create_spark_session()
    
    # reference: https://stackoverflow.com/questions/42822483/extremely-slow-s3-write-times-from-emr-spark
    spark.sparkContext._jsc.hadoopConfiguration() \
      .set( "mapreduce.fileoutputcommitter.algorithm.version", \
            "2" \
          )
    
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://<bucket name>/"
    
    process_song_data(spark, input_data, output_data) 
    process_log_data(spark, input_data, output_data)   
    
if __name__ == "__main__":
    main()
