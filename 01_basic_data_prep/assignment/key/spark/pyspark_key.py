#1

path = '/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/offers.csv'
offers_df =  spark.read.option('header', 'true').csv(path)
offers_df.printSchema()

root
 |-- offer: string (nullable = true)
 |-- category: string (nullable = true)
 |-- quantity: string (nullable = true)
 |-- company: string (nullable = true)
 |-- offervalue: string (nullable = true)
 |-- brand: string (nullable = true)

 offers_df.createOrReplaceTempView('offers_df')
 spark.sql('SELECT COUNT(*) FROM offers_df').show()

+--------+
|count(1)|
+--------+
|      37|
+--------+

offers_df.count()

37

path = '/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/trainHistory.csv'
train_df =  spark.read.option('header', 'true').csv(path)
train_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- offer: string (nullable = true)
 |-- market: string (nullable = true)
 |-- repeattrips: string (nullable = true)
 |-- repeater: string (nullable = true)
 |-- offerdate: string (nullable = true)

train_df.createOrReplaceTempView('train_df')
spark.sql('SELECT COUNT(*) FROM train_df').show()

+--------+
|count(1)|
+--------+
|  160057|
+--------+

train_df.count()

160057

path = '/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/testHistory.csv'
test_df =  spark.read.option('header', 'true').csv(path)
test_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- offer: string (nullable = true)
 |-- market: string (nullable = true)
 |-- offerdate: string (nullable = true)

test_df.createOrReplaceTempView('test_df')
spark.sql('SELECT COUNT(*) FROM test_df').show()

+--------+
|count(1)|
+--------+
|  151484|
+--------+

path = '/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/transactions.csv'
trans_df =  spark.read.option('header', 'true').csv(path)
trans_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- dept: string (nullable = true)
 |-- category: string (nullable = true)
 |-- company: string (nullable = true)
 |-- brand: string (nullable = true)
 |-- date: string (nullable = true)
 |-- productsize: string (nullable = true)
 |-- productmeasure: string (nullable = true)
 |-- purchasequantity: string (nullable = true)
 |-- purchaseamount: string (nullable = true)

test_df.count()

151484

trans_df.createOrReplaceTempView('trans_df')
spark.sql('SELECT COUNT(*) FROM trans_df').show()

+---------+
| count(1)|
+---------+
|349655789|
+---------+

trans_df.count()

349655789

---

#2

train_df = train_df.drop('repeattrips')
train_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- offer: string (nullable = true)
 |-- market: string (nullable = true)
 |-- repeater: string (nullable = true)
 |-- offerdate: string (nullable = true)

---

#3

train_df = train_df.join(offers_df, train_df.offer == offers_df.offer).drop(offers_df.offer)
train_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- offer: string (nullable = true)
 |-- market: string (nullable = true)
 |-- repeater: string (nullable = true)
 |-- offerdate: string (nullable = true)
 |-- category: string (nullable = true)
 |-- quantity: string (nullable = true)
 |-- company: string (nullable = true)
 |-- offervalue: string (nullable = true)
 |-- brand: string (nullable = true)

train_df.count()

160057

test_df = test_df.join(offers_df, test_df.offer == offers_df.offer).drop(offers_df.offer)
test_df.printSchema()
root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- offer: string (nullable = true)
 |-- market: string (nullable = true)
 |-- offerdate: string (nullable = true)
 |-- category: string (nullable = true)
 |-- quantity: string (nullable = true)
 |-- company: string (nullable = true)
 |-- offervalue: string (nullable = true)
 |-- brand: string (nullable = true)

test_df.count()

151484

---

#3

trans_df = trans_df.withColumn('purchaseamount', trans_df['purchaseamount'].cast('double'))
trans_df = trans_df.withColumn('purchasequantity', trans_df['purchasequantity'].cast('double'))

trans_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- dept: string (nullable = true)
 |-- category: string (nullable = true)
 |-- company: string (nullable = true)
 |-- brand: string (nullable = true)
 |-- date: string (nullable = true)
 |-- productsize: string (nullable = true)
 |-- productmeasure: string (nullable = true)
 |-- purchasequantity: double (nullable = true)
 |-- purchaseamount: double (nullable = true)

grouped_trans_df = trans_df.groupby('id', 'category').mean('purchaseamount', 'purchasequantity')
grouped_trans_df.show()

+---------+--------+-------------------+---------------------+
|       id|category|avg(purchaseamount)|avg(purchasequantity)|
+---------+--------+-------------------+---------------------+
|100007447|    3008| 2.4250000000000003|                  1.0|
|100007447|    6323|               3.99|                  1.0|
|100010021|    4105|                2.0|                  2.0|
|100022923|    3204|                8.1|                  1.0|
|100029473|    1898|               6.84|                  1.0|
|100029473|     814|               3.31|                  1.0|
|100043455|    5128|               2.33|                  1.0|
|100043455|    9517|               1.29|                  1.0|
|100050424|    2301|               2.48|                  2.0|
|100050424|    2610|               1.99|                  1.0|
|100051316|       0|               6.99|                  1.0|
|100051316|     838|                3.0|                  3.0|
|100084808|    2928| 2.9212499999999997|                1.625|
|100084808|    3709|              1.556|                  2.2|
|100084808|    7314|              24.99|                  1.0|
|100093033|    5905|                3.1|                  1.0|
|100093033|    5907|               1.29|                  1.0|
|100133594|    2118|                1.0|                  1.0|
|100133594|     902|                3.0|                  1.0|
|100156512|    1113|               5.29|                  1.0|
+---------+--------+-------------------+---------------------+

grouped_trans_df = grouped_trans_df.withColumnRenamed('avg(purchasequantity)', 'avg_purchasequantity')
grouped_trans_df = grouped_trans_df.withColumnRenamed('avg(purchaseamount)', 'avg_purchaseamount')

---

#4

train_df = train_df.join(grouped_trans_df, (train_df.id == grouped_trans_df.id) & (train_df.category == grouped_trans_df.category), 'left').drop(grouped_trans_df.id).drop(grouped_trans_df.category).fillna(0)
train_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- offer: string (nullable = true)
 |-- market: string (nullable = true)
 |-- repeater: string (nullable = true)
 |-- offerdate: string (nullable = true)
 |-- category: string (nullable = true)
 |-- quantity: string (nullable = true)
 |-- company: string (nullable = true)
 |-- offervalue: string (nullable = true)
 |-- brand: string (nullable = true)
 |-- avg_purchaseamount: double (nullable = false)
 |-- avg_purchasequantity: double (nullable = false)

train_df.count()

160057

test_df = test_df.join(grouped_trans_df, (test_df.id == grouped_trans_df.id) & (test_df.category == grouped_trans_df.category), 'left').drop(grouped_trans_df.id).drop(grouped_trans_df.category).fillna(0)
test_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- offer: string (nullable = true)
 |-- market: string (nullable = true)
 |-- offerdate: string (nullable = true)
 |-- category: string (nullable = true)
 |-- quantity: string (nullable = true)
 |-- company: string (nullable = true)
 |-- offervalue: string (nullable = true)
 |-- brand: string (nullable = true)
 |-- avg_purchaseamount: double (nullable = false)
 |-- avg_purchasequantity: double (nullable = false)

test_df.count()

151484

---

#5

train_df_subset = train_df.filter(train_df.id < 14000000)
train_df_subset.coalesce(1).write.csv('/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/key/train_key.csv')

test_df_subset = test_df.filter(test_df.id > 4810000000)
test_df_subset.coalesce(1).write.csv('/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/key/test_key.csv')