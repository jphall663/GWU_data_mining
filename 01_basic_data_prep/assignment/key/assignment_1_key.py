# 2 - import from CSV

path = '/home/patrickh/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/offers.csv'
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

path = '/home/patrickh/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/trainHistory.csv'
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

path = '/home/patrickh/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/testHistory.csv'
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

test_df.count()

151484

path = '/home/patrickh/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/transactions.csv'
trans_df =  spark.read.option('header', 'true').csv(path)
trans_df = trans_df.drop('chain', 'dept', 'brand', 'date', 'productsize', 'productmeasure', 'company')
trans_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- category: string (nullable = true)
 |-- purchasequantity: string (nullable = true)
 |-- purchaseamount: string (nullable = true)

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

# 3 - drop repeattrips

train_df = train_df.drop('repeattrips', 'repeater')
train_df.printSchema()

root
 |-- id: string (nullable = true)
 |-- chain: string (nullable = true)
 |-- offer: string (nullable = true)
 |-- market: string (nullable = true)
 |-- offerdate: string (nullable = true)

---

# 4 - left join offers onto training and test data

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

# 5 - add past category transactions

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

grouped_trans_df = trans_df.groupby('id', 'category').avg('purchaseamount', 'purchasequantity')
grouped_trans_df.show()

+--------+--------+-------------------+---------------------+
|      id|category|avg(purchaseamount)|avg(purchasequantity)|
+--------+--------+-------------------+---------------------+
|   86246|    5910|             2.9425|                 0.75|
|   86252|    3008|  2.668536585365853|    1.170731707317073|
|12262064|    6311| 2.9699999999999998|                  1.0|
|12262064|    5902|              3.432|                  1.0|
|12262064|    1013|              1.995|                  1.0|
|12262064|    3612|               0.89|                  1.0|
|12277270|    5604|  5.871818181818182|                  1.0|
|12277270|    2707|  7.604285714285715|                  1.0|
|12277270|     814|                2.0|                  1.0|
|12277270|    5613|               3.99|                  1.0|
|12524696|    5552|  4.705000000000001|                  1.0|
|12682470|     418| 2.9966666666666666|                  1.0|
|13074629|    3101|  3.777272727272728|   1.0909090909090908|
|13089312|     826|               0.99|                  1.0|
|13179265|    2928| 1.0792307692307692|   1.2307692307692308|
|13179265|    9799|  5.489999999999999|                  1.0|
|13251776|    2119|               1.79|                  1.0|
|13387341|    6409|  6.259583333333334|   0.9166666666666666|
|13501141|    1703|             2.8675|                  1.0|
|13540129|    2626|               2.69|                  1.0|
+--------+--------+-------------------+---------------------+


grouped_trans_df = grouped_trans_df.withColumnRenamed('avg(purchasequantity)', 'avg_purchasequantity')
grouped_trans_df = grouped_trans_df.withColumnRenamed('avg(purchaseamount)', 'avg_purchaseamount')

train_df = train_df.join(grouped_trans_df, (train_df.id == grouped_trans_df.id) & (train_df.category == grouped_trans_df.category), 'left').drop(grouped_trans_df.id).drop(grouped_trans_df.category).fillna(0)
train_df.printSchema()

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

# 6 - past purchase of product on order

trans_offers_df = trans_df.join(offers_df, trans_df.category == offers_df.category, 'left').drop(offers_df.category)
trans_offers_df = trans_offers_df.where(trans_offers_df.offer.isNotNull())

trans_offers_df = trans_offers_df.withColumn('purchasequantity', trans_offers_df['purchasequantity'].cast('double'))
grouped_trans_offers_df = trans_offers_df.groupby('id', 'category', 'brand', 'company').sum('purchasequantity')
grouped_trans_offers_df = grouped_trans_offers_df.withColumnRenamed('sum(purchasequantity)', 'exact_item_bought')
grouped_trans_offers_df = grouped_trans_offers_df.select('*', grouped_trans_offers_df.id.alias('gto_id'), grouped_trans_offers_df.category.alias('gto_category'), grouped_trans_offers_df.brand.alias('gto_brand'), grouped_trans_offers_df.company.alias('gto_company')).drop('id', 'category', 'brand', 'company')
grouped_trans_offers_df.printSchema()

root
 |-- exact_item_bought: double (nullable = true)
 |-- gto_id: string (nullable = true)
 |-- gto_category: string (nullable = true)
 |-- gto_brand: string (nullable = true)
 |-- gto_company: string (nullable = true)

train_df = train_df.join(grouped_trans_offers_df, (train_df.id == grouped_trans_offers_df.gto_id) & (train_df.category == grouped_trans_offers_df.gto_category) & (train_df.brand == grouped_trans_offers_df.gto_brand) & (train_df.company == grouped_trans_offers_df.gto_company), 'left').drop(grouped_trans_offers_df.gto_id).drop(grouped_trans_offers_df.gto_category).drop(grouped_trans_offers_df.gto_brand).drop(grouped_trans_offers_df.gto_company).fillna(0)

train_df.show()

+----------+-----+-------+------+----------+--------+--------+---------+----------+-----+------------------+--------------------+-----------------+
|        id|chain|  offer|market| offerdate|category|quantity|  company|offervalue|brand|avg_purchaseamount|avg_purchasequantity|exact_item_bought|
+----------+-----+-------+------+----------+--------+--------+---------+----------+-----+------------------+--------------------+-----------------+
|1048253332|  214|1198271|     8|2013-03-27|    5558|       1|107120272|       1.5| 5072|               0.0|                 0.0|              0.0|
| 106372514|   17|1197502|     4|2013-03-28|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
|1064972209|  214|1208251|     8|2013-04-23|    2202|       1|104460040|         2| 3718|               0.0|                 0.0|              0.0|
|1070619072|   46|1208329|    15|2013-04-23|    2119|       1|108079383|         1| 6926| 4.517586206896551|  1.5517241379310345|             45.0|
|1080684610|  214|1197502|     8|2013-04-19|    3203|       1|106414464|      0.75|13474|              2.69|                 1.0|              1.0|
| 110147403|    4|1197502|     1|2013-03-28|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
|1106147664|  214|1208251|     8|2013-04-23|    2202|       1|104460040|         2| 3718|               0.0|                 0.0|              0.0|
|1114920745|   46|1197502|    15|2013-03-30|    3203|       1|106414464|      0.75|13474|             2.515|                 1.0|              2.0|
| 117843820|   15|1197502|     9|2013-04-02|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
|1182929300|  214|1197502|     8|2013-03-27|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
| 118749074|   15|1197502|     9|2013-03-25|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
| 120720503|    4|1197502|     1|2013-03-30|    3203|       1|106414464|      0.75|13474|              3.29|                 1.0|              1.0|
| 120827135|    4|1197502|     1|2013-03-25|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
| 121480332|    4|1208252|     1|2013-04-28|    2202|       1|104460040|         3| 3718|               0.0|                 0.0|              0.0|
| 122057467|   15|1204576|     9|2013-04-04|    5616|       1|104610040|         1|15889| 5.910357142857143|  1.1071428571428572|             31.0|
| 123254809|   20|1208251|     7|2013-04-24|    2202|       1|104460040|         2| 3718|               0.0|                 0.0|              0.0|
|1233572961|  214|1197502|     8|2013-03-29|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
| 123379717|   88|1197502|    14|2013-03-27|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
|1237291485|  214|1197502|     8|2013-04-02|    3203|       1|106414464|      0.75|13474|            2.3875|                 1.0|              4.0|
| 123812421|   14|1197502|     8|2013-03-25|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
+----------+-----+-------+------+----------+--------+--------+---------+----------+-----+------------------+--------------------+-----------------+


train_df.count()

160057

test_df = test_df.join(grouped_trans_offers_df, (test_df.id == grouped_trans_offers_df.gto_id) & (test_df.category == grouped_trans_offers_df.gto_category) & (test_df.brand == grouped_trans_offers_df.gto_brand) & (test_df.company == grouped_trans_offers_df.gto_company), 'left').drop(grouped_trans_offers_df.gto_id).drop(grouped_trans_offers_df.gto_category).drop(grouped_trans_offers_df.gto_brand).drop(grouped_trans_offers_df.gto_company).fillna(0)
test_df.count()

151484

---

# 7 - output submission files to CSV

train_df_pd = train_df.toPandas()
train_df_subset_pd = train_df_pd[(train_df_pd['avg_purchaseamount'] > 0) & (train_df_pd['avg_purchasequantity']) > 0]
train_df_subset_pd = train_df_subset_pd[train_df_subset_pd['id'] < 107014607]
train_df_subset_pd.loc[train_df_subset_pd['exact_item_bought'] > 0, 'exact_item_bought'] = 1
train_df_subset_pd = train_df_subset_pd.sort_values(by='id', ascending=False)
train_df_subset_pd.to_csv('/home/patrickh/workspace/GWU_data_mining/01_basic_data_prep/assignment/key/train_key.csv', index=False)
