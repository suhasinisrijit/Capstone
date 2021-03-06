
import pandas as pd
import pyspark as ps
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array

from pyspark import SparkContext
sc = SparkContext("local", "MyApp")
print("Spark Context Created");

adclicksDF = pd.read_csv('~/Capstone/GameData/flamingo-data/ad-clicks.csv')
adclicksDF = adclicksDF.rename(columns=lambda x: x.strip()) #remove whitespaces from headers
adclicksDF.head(n=5)

adclicksDF['adCount'] = 1
adclicksDF.head(n=5)

print("Checkpoint 1");

buyclicksDF = pd.read_csv('~/Capstone/GameData/flamingo-data/buy-clicks.csv')
buyclicksDF = buyclicksDF.rename(columns=lambda x: x.strip()) #removes whitespaces from headers
buyclicksDF.head(n=5)
userPurchases = buyclicksDF[['userId','price']] #select only userid and price
userPurchases.head(n=5)
useradClicks = adclicksDF[['userId','adCount']]
useradClicks.head(n=5) #as we saw before, this line displays first five lines

adsPerUser = useradClicks.groupby('userId').sum()
adsPerUser = adsPerUser.reset_index()
adsPerUser.columns = ['userId', 'totalAdClicks'] #rename the columns

adsPerUser.tail(n=5)

revenuePerUser = userPurchases.groupby('userId').sum()
revenuePerUser = revenuePerUser.reset_index()
revenuePerUser.columns = ['userId', 'revenue'] #rename the columns


revenuePerUser.head(n=5)


combinedDF = adsPerUser.merge(revenuePerUser, on='userId') #userId, adCount, price

combinedDF.head(n=5) #display how the merged table looks
trainingDF = combinedDF[['totalAdClicks','revenue']]
trainingDF.head(n=5)
trainingDF.shape

print("Checkpoint 2");

sqlContext = SQLContext(sc)
pDF = sqlContext.createDataFrame(trainingDF)
parsedData = pDF.rdd.map(lambda line: array([line[0], line[1]])) #totalAdClicks, revenue

my_kmmodel = KMeans.train(parsedData, 2, maxIterations=10, runs=10, initializationMode="random")

print(my_kmmodel.centers)


