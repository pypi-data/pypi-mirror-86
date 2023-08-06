import pandas as pd
from pyspark.sql import SparkSession



def pd_read_map(map_csv_path, delimiter=";"):
    """ Read mapping csv from hdfs as dict, consist of source (string to replace)
        and destination (string for replace with) column
        
        from:    
        +-----------+--------------+
        | source    | destination  |
        +-----------+--------------+
        | perempuan | wanita       |
        | laki-laki | pria         |
        +-----------+--------------+
        
        to:
        {"perempuan":"wanita", "laki-laki":"pria"}

        Args:
            map_csv_path (String): map csv hdfs path
            delimiter (String): delimiter of csv file. default ";"

        Return:
            Mapping dictionary
    """
    # APP
    spark = SparkSession.builder.appName("pd_read_map").getOrCreate()
    mapx = spark.read.option("delimiter", delimiter)\
                     .option("header",True)\
                     .csv(map_csv_path)
    mapx = pd.Series(
        mapx.toPandas().destionation.values,
        index=mapx.toPandas().source
    ).to_dict()

    return spark.sparkContext.broadcast(mapx)   
