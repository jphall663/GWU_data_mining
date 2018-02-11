# 2 - import from CSV

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

test_df.count()

151484

path = '/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/raw/transactions.csv'
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

grouped_trans_df = trans_df.groupby('id', 'category').max('purchaseamount', 'purchasequantity')
grouped_trans_df.show()

+--------+--------+-------------------+---------------------+
|      id|category|max(purchaseamount)|max(purchasequantity)|
+--------+--------+-------------------+---------------------+
|   86246|    5910|               3.99|                  1.0|
|   86252|    3008|               6.98|                  3.0|
|12262064|    6311|               3.99|                  1.0|
|12262064|    5902|               3.79|                  1.0|
|12262064|    1013|                2.0|                  1.0|
|12262064|    3612|               0.89|                  1.0|
|12277270|    5604|               9.99|                  1.0|
|12277270|    2707|               9.99|                  1.0|
|12277270|     814|                2.0|                  1.0|
|12277270|    5613|               3.99|                  1.0|
|12524696|    5552|               5.99|                  1.0|
|12682470|     418|               5.49|                  1.0|
|13074629|    3101|               8.58|                  2.0|
|13089312|     826|               0.99|                  1.0|
|13179265|    2928|               3.78|                  2.0|
|13179265|    9799|              11.09|                  1.0|
|13251776|    2119|               1.79|                  1.0|
|13387341|    6409|              15.52|                  2.0|
|13501141|    1703|               3.79|                  1.0|
|13540129|    2626|               2.69|                  1.0|
+--------+--------+-------------------+---------------------+

grouped_trans_df = grouped_trans_df.withColumnRenamed('max(purchasequantity)', 'max_purchasequantity')
grouped_trans_df = grouped_trans_df.withColumnRenamed('max(purchaseamount)', 'max_purchaseamount')

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
 |-- max_purchaseamount: double (nullable = false)
 |-- max_purchasequantity: double (nullable = false)

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
 |-- max_purchaseamount: double (nullable = false)
 |-- max_purchasequantity: double (nullable = false)


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
|        id|chain|  offer|market| offerdate|category|quantity|  company|offervalue|brand|max_purchaseamount|max_purchasequantity|exact_item_bought|
+----------+-----+-------+------+----------+--------+--------+---------+----------+-----+------------------+--------------------+-----------------+
|1048253332|  214|1198271|     8|2013-03-27|    5558|       1|107120272|       1.5| 5072|               0.0|                 0.0|              0.0|
| 106372514|   17|1197502|     4|2013-03-28|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
|1064972209|  214|1208251|     8|2013-04-23|    2202|       1|104460040|         2| 3718|               0.0|                 0.0|              0.0|
|1070619072|   46|1208329|    15|2013-04-23|    2119|       1|108079383|         1| 6926|              6.58|                 5.0|             45.0|
|1080684610|  214|1197502|     8|2013-04-19|    3203|       1|106414464|      0.75|13474|              2.69|                 1.0|              1.0|
| 110147403|    4|1197502|     1|2013-03-28|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
|1106147664|  214|1208251|     8|2013-04-23|    2202|       1|104460040|         2| 3718|               0.0|                 0.0|              0.0|
|1114920745|   46|1197502|    15|2013-03-30|    3203|       1|106414464|      0.75|13474|              2.54|                 1.0|              2.0|
| 117843820|   15|1197502|     9|2013-04-02|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
|1182929300|  214|1197502|     8|2013-03-27|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
| 118749074|   15|1197502|     9|2013-03-25|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
| 120720503|    4|1197502|     1|2013-03-30|    3203|       1|106414464|      0.75|13474|              3.29|                 1.0|              1.0|
| 120827135|    4|1197502|     1|2013-03-25|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
| 121480332|    4|1208252|     1|2013-04-28|    2202|       1|104460040|         3| 3718|               0.0|                 0.0|              0.0|
| 122057467|   15|1204576|     9|2013-04-04|    5616|       1|104610040|         1|15889|             11.58|                 3.0|             31.0|
| 123254809|   20|1208251|     7|2013-04-24|    2202|       1|104460040|         2| 3718|               0.0|                 0.0|              0.0|
|1233572961|  214|1197502|     8|2013-03-29|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
| 123379717|   88|1197502|    14|2013-03-27|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
|1237291485|  214|1197502|     8|2013-04-02|    3203|       1|106414464|      0.75|13474|              3.08|                 1.0|              4.0|
| 123812421|   14|1197502|     8|2013-03-25|    3203|       1|106414464|      0.75|13474|               0.0|                 0.0|              0.0|
+----------+-----+-------+------+----------+--------+--------+---------+----------+-----+------------------+--------------------+-----------------+

train_df.count()

160057

test_df = test_df.join(grouped_trans_offers_df, (test_df.id == grouped_trans_offers_df.gto_id) & (test_df.category == grouped_trans_offers_df.gto_category) & (test_df.brand == grouped_trans_offers_df.gto_brand) & (test_df.company == grouped_trans_offers_df.gto_company), 'left').drop(grouped_trans_offers_df.gto_id).drop(grouped_trans_offers_df.gto_category).drop(grouped_trans_offers_df.gto_brand).drop(grouped_trans_offers_df.gto_company).fillna(0)

+----------+-----+-------+------+----------+--------+--------+----------+----------+-----+------------------+--------------------+-----------------+
|        id|chain|  offer|market| offerdate|category|quantity|   company|offervalue|brand|max_purchaseamount|max_purchasequantity|exact_item_bought|
+----------+-----+-------+------+----------+--------+--------+----------+----------+-----+------------------+--------------------+-----------------+
|1026984567|   46|1221658|    15|2013-06-22|    7205|       2| 103700030|         3| 4294|              4.96|                 1.0|             10.0|
| 103580546|   95|1221658|    39|2013-06-29|    7205|       2| 103700030|         3| 4294|              3.98|                 2.0|             30.0|
|1047953754|   46|1221663|    15|2013-06-21|    7205|       1| 103700030|       1.5| 4294|               4.7|                 2.0|             35.0|
|1095959789|   46|1230218|    15|2013-07-26|     706|       1| 104127141|         1|26189|               0.0|                 0.0|              0.0|
| 115842948|   88|1221665|    14|2013-06-24|    7205|       1| 103700030|       1.5| 4294|               0.0|                 0.0|              0.0|
| 116021835|   95|1213242|    39|2013-05-21|    5824|       1| 105190050|         2|26456|               8.8|                 2.0|              4.0|
| 116517444|   15|1219903|     9|2013-06-29|     799|       1|1076211171|       1.5|17286|               0.0|                 0.0|              0.0|
| 119994909|   15|1203439|     9|2013-05-11|    5122|       1| 107106878|       1.5|17311|             14.49|                 1.0|              1.0|
| 120855534|   95|1230218|    39|2013-07-25|     706|       1| 104127141|         1|26189|              4.99|                 1.0|              3.0|
| 120941072|    4|1219903|     1|2013-06-29|     799|       1|1076211171|       1.5|17286|               0.0|                 0.0|              0.0|
| 121168778|    4|1221666|     1|2013-06-23|    7205|       1| 103700030|       1.5| 4294|              6.98|                 2.0|             50.0|
| 121488298|   88|1221658|    14|2013-06-20|    7205|       2| 103700030|         3| 4294|              7.38|                 2.0|             65.0|
| 121559060|   14|1221658|     8|2013-06-25|    7205|       2| 103700030|         3| 4294|              6.98|                 2.0|             75.0|
| 121689455|   18|1219903|    11|2013-06-30|     799|       1|1076211171|       1.5|17286|               0.0|                 0.0|              0.0|
| 121757152|   18|1213242|    11|2013-05-23|    5824|       1| 105190050|         2|26456|              2.99|                 1.0|              1.0|
| 123213372|   14|1221663|     8|2013-06-24|    7205|       1| 103700030|       1.5| 4294|              3.69|                 3.0|             35.0|
| 123842203|   18|1221658|    11|2013-06-25|    7205|       2| 103700030|         3| 4294|              5.79|                 4.0|             60.0|
| 125200917|    4|1190530|     1|2013-05-10|    9115|       1| 108500080|         5|93904|             39.99|                 1.0|             26.0|
| 125921628|   15|1221658|     9|2013-06-21|    7205|       2| 103700030|         3| 4294|              5.69|                 1.0|             35.0|
| 125944134|   14|1221663|     8|2013-06-20|    7205|       1| 103700030|       1.5| 4294|              4.49|                 2.0|             45.0|
+----------+-----+-------+------+----------+--------+--------+----------+----------+-----+------------------+--------------------+-----------------+

test_df.count()

151484

---

# 7 - output submission files to CSV

train_df_subset = train_df.filter(train_df.id < 14000000)
train_df_subset_pd = train_df_subset.toPandas()
train_df_subset_pd.loc[train_df_subset_pd.exact_item_bought > 0, 'exact_item_bought'] = 1
train_df_subset_pd = train_df_subset_pd.sort_values(by='id', ascending=False)
train_df_subset_pd.to_csv('/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/key/train_key.csv', index=False)

test_df_subset = test_df.filter(test_df.id > 4810000000)
test_df_subset_pd = test_df_subset.toPandas()
test_df_subset_pd.loc[test_df_subset_pd.exact_item_bought > 0, 'exact_item_bought'] = 1
test_df_subset_pd = test_df_subset_pd.sort_values(by='id', ascending=False)
test_df_subset_pd.to_csv('/Users/phall/workspace/GWU_data_mining/01_basic_data_prep/assignment/key/test_key.csv', index=False)
