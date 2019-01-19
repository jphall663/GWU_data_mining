# read in data

>>> path = 'scratch.csv'
>>> cust_df = spark.read.option('header', 'true').csv(path)
>>> cust_df.printSchema()
root
 |-- numeric1: string (nullable = true)
 |-- numeric2: string (nullable = true)
 |-- char1: string (nullable = true)
 |-- char2: string (nullable = true)
 |-- key: string (nullable = true)

 >>> cust_df.count()
 1000

 >>> cust_df.createOrReplaceTempView('cust_df')
 >>> spark.sql('SELECT COUNT(*) FROM cust_df').show()
 +--------+
 |count(1)|
 +--------+
 |    1000|
 +--------+

>>> path = 'scratch2.csv'
>>> trans_df = spark.read.option('header', 'true').csv(path)
>>> trans_df.printSchema()
root
 |-- key: string (nullable = true)
 |-- numeric3: string (nullable = true)

trans_df.count()
5000

 >>> trans_df.createOrReplaceTempView('trans_df')
 >>> spark.sql('SELECT COUNT(*) FROM trans_df').show()
 +--------+
 |count(1)|
 +--------+
 |    5000|
 +--------+

# drop columns

>>> cust_df = cust_df.drop('numeric2', 'char2')
>>> cust_df.printSchema()
root
 |-- numeric1: string (nullable = true)
 |-- char1: string (nullable = true)
 |-- key: string (nullable = true)

# convert columns to double for numeric functions

 >>> trans_df = trans_df.withColumn('numeric3', trans_df['numeric3'].cast('double'))
 >>> trans_df.printSchema()
 root
  |-- key: string (nullable = true)
  |-- numeric3: double (nullable = true)

# groupby

>>> grouped_trans_df = trans_df.groupby('key').max('numeric3')
>>> grouped_trans_df.show()
+---+-------------------+
|key|      max(numeric3)|
+---+-------------------+
|296| 1.0647960079919738|
|467|  0.507246728488537|
|675| 1.3214449254393992|
|691| 0.5217609876322263|
|829|  1.310916126295388|
|125| 1.0003281519032272|
|451| 0.2978896491275767|
|800| 1.3279887599365996|
|853| 1.3573387004663975|
|944| 0.6426301312589007|
|666| 1.9515934218160937|
|870| 1.5273080721916197|
|919|  2.111709321232935|
|926| 1.4025836781372398|
|  7| 1.3853932472374593|
| 51| 2.7536210228351967|
|124| 1.6386144192310446|
|447| 1.1035305318873843|
|591|0.09231430553027069|
|307| 0.7940950500154996|
+---+-------------------+
only showing top 20 rows

>>> grouped_trans_df.count()
1000

# rename

>>> grouped_trans_df = grouped_trans_df.withColumnRenamed('max(numeric3)', 'max_numeric3')
>>> grouped_trans_df.printSchema()
root
 |-- key: string (nullable = true)
 |-- max_numeric3: double (nullable = true)

# join

>>> joined_cust_df = cust_df.join(grouped_trans_df, cust_df.key == grouped_trans_df.key).drop(cust_df.key)
>>> joined_cust_df.printSchema()
root
 |-- numeric1: string (nullable = true)
 |-- char1: string (nullable = true)
 |-- key: string (nullable = true)
 |-- max_numeric3: double (nullable = true)

 >>> joined_cust_df.count()
 1000

 >>> joined_cust_df.show()
+--------------------+--------+---+-------------------+
|            numeric1|   char1|key|       max_numeric3|
+--------------------+--------+---+-------------------+
| -0.5437866363786446|CCCCCCCC|  0| 0.9855791456824139|
|  1.6335321929483595|BBBBBBBB|  1|0.23625117401868062|
| 0.00291794414741136|DDDDDDDD|  2| 1.6535993358257746|
|-0.06729804442995206|EEEEEEEE|  3| 2.0374484244839057|
|  0.6297253946298446|AAAAAAAA|  4|  2.703289941498199|
|  0.3231675367659894|BBBBBBBB|  5| 2.0757967800249455|
| 0.22986952407577876|FFFFFFFF|  6|  1.569895017566389|
|-0.13708940465148253|FFFFFFFF|  7| 1.3853932472374593|
|   1.057404395056542|EEEEEEEE|  8|    2.0562785413641|
| -0.4334591093154298|BBBBBBBB|  9|  0.784434164694336|
| 0.43814491396723926|DDDDDDDD| 10| 1.3079973031811907|
| -0.8036731258030813|EEEEEEEE| 11|  1.666499057767304|
|-0.11565694024047969|GGGGGGGG| 12|  0.726302697310102|
|  0.4147488002582721|GGGGGGGG| 13| 1.3856410120066784|
| -1.2389072279737852|FFFFFFFF| 14|  1.234118255742245|
| -1.0807816716458907|GGGGGGGG| 15|  1.213158520894163|
| -0.6065529938589715|DDDDDDDD| 16|0.14752573068092437|
|  0.4252504393111313|GGGGGGGG| 17| 0.8645213389801757|
|   1.426088732449592|AAAAAAAA| 18|  1.441803835958583|
| -1.0352471625774415|AAAAAAAA| 19| 1.0362781824173604|
+--------------------+--------+---+-------------------+

# subset rows

>>> joined_cust_df_subset = joined_cust_df.filter(joined_cust_df.key < 10)

>>> joined_cust_df_subset.count()
10

>>> joined_cust_df_subset.show()
+--------------------+--------+---+-------------------+
|            numeric1|   char1|key|       max_numeric3|
+--------------------+--------+---+-------------------+
| -0.5437866363786446|CCCCCCCC|  0| 0.9855791456824139|
|  1.6335321929483595|BBBBBBBB|  1|0.23625117401868062|
| 0.00291794414741136|DDDDDDDD|  2| 1.6535993358257746|
|-0.06729804442995206|EEEEEEEE|  3| 2.0374484244839057|
|  0.6297253946298446|AAAAAAAA|  4|  2.703289941498199|
|  0.3231675367659894|BBBBBBBB|  5| 2.0757967800249455|
| 0.22986952407577876|FFFFFFFF|  6|  1.569895017566389|
|-0.13708940465148253|FFFFFFFF|  7| 1.3853932472374593|
|   1.057404395056542|EEEEEEEE|  8|    2.0562785413641|
| -0.4334591093154298|BBBBBBBB|  9|  0.784434164694336|
+--------------------+--------+---+-------------------+

# convert to pandas and save

joined_cust_df_subset.toPandas().to_csv('scratch3.csv')
