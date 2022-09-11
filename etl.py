from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import IntegerType


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
    song_data = input_data + 'song_data/A/A/A/*.json'

    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select('song_id', 'title', 'artist_id',
                            'year', 'duration') \
                    .dropDuplicates()
    songs_table.createOrReplaceTempView('songs')

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist_id') \
                     .parquet(os.path.join(output_data, 'songs/songs.parquet'), 'overwrite')

    # extract columns to create artists table
    artists_table = df.select('artist_id', 'artist_name', 'artist_location',
                              'artist_latitude', 'artist_longitude') \
                      .withColumnRenamed('artist_name', 'name') \
                      .withColumnRenamed('artist_location', 'location') \
                      .withColumnRenamed('artist_latitude', 'latitude') \
                      .withColumnRenamed('artist_longitude', 'longitude') \
                      .dropDuplicates()
    
    artists_table.createOrReplaceTempView('artists')

    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data, 'artists/artists.parquet'), 'overwrite')


def process_log_data(spark, input_data, output_data):
    '''
    Extract, Load and Transform log data from S3, generating
    dimension tables users, artists, and songplays dimension
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

    # extract columns to create users table
    users_table = df.select('user_id','firstName', 'lastName', 'gender', 'level') \
                    .withColumnRenamed('firstName', 'first_name') \
                    .withColumnRenamed('lastName', 'last_name') \
                    .dropDuplicates()
    
    users_table.createOrReplaceTempView('users')
    
    # write artists table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users/users.parquet'), 'overwrite')

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
