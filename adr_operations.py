import pandas as pd
import clustering as cl
# data_frame = pd.read_csv( 'cluster_hotel.csv' )
yearlist = []

def toCSV(csv_file):
    data_frame = pd.read_csv(csv_file)
    return data_frame

def monthly_transaction_avg(data_frame):
    # data_frame = pd.read_csv(source_file)
    print( 'Loading...................' )

    averageList = []
    sumList = []
    clusteraverageList = []
    clustersumList = []
    data_frame_new = data_frame[[
        'arrival_date_year', 'arrival_date_month', 'adr']]


    for index, row in data_frame_new.iterrows():
        year = row['arrival_date_year']
        if year not in yearlist:
            yearlist.append( year )

    dfList = []
    # df = "df"
    for year in yearlist:
        rows = []
        for index, row in data_frame_new.iterrows():
            y = row['arrival_date_year']
            m = row['arrival_date_month']
            adr = row['adr']
            if y == year:
                rows.append( [y, m, adr] )
        df = "df" + str( year )
        df = pd.DataFrame( rows, columns=['year', 'month', 'adr'] )

        dfList.append( df )
    for dataframes in dfList:
        averageList.append( dataframes.groupby( ['year', 'month'], sort=False ).mean() )
        sumList.append( dataframes.groupby( ['year', 'month'], sort=False ).sum() )
    return averageList, sumList


def clusterWiseMonthlyInfo(data_frame):
    print( 'Loading...................' )

    clusteraverageList = []
    clustersumList = []
    data_frame_new = data_frame[[
        'arrival_date_year', 'arrival_date_month', 'adr']]

    for index, row in data_frame_new.iterrows():
        year = row['arrival_date_year']
        if year not in yearlist:
            yearlist.append( year )

    dfList = []
    # df = "df"
    for year in yearlist:
        rows = []
        for index, row in data_frame_new.iterrows():
            y = row['arrival_date_year']
            m = row['arrival_date_month']
            adr = row['adr']
            ctr = row['Cluster']
            if y == year:
                rows.append( [y, m, adr, ctr] )
        df = "df" + str( year )
        df = pd.DataFrame( rows, columns=['year', 'month', 'adr', 'cluster'] )

        dfList.append( df )
    for dataframes in dfList:
        clusteraverageList.append( dataframes.groupby( ['cluster', 'year', 'month'], sort=False ).mean() )
        clustersumList.append( dataframes.groupby( ['cluster', 'year', 'month'], sort=False ).sum() )

    return clusteraverageList, clustersumList

output2 = monthly_transaction_avg(toCSV('correct_cluster.csv'))
output3 = monthly_transaction_avg(toCSV('correct_cluster.csv'))
def dictionryOutput():
    adrDic = {}
    adrTotal = {}

    for i in output2[0]:
        # print(i)
        adrInDic = {}
        for j in range( len( i ) ):
            adrInDic[i.index.values[j][1]] = i['adr'].iloc[j]
        adrDic[i.index.values[0][0]] = adrInDic
    for i in output2[1]:
        # print(i)
        adrInTotal = {}
        for j in range( len( i ) ):
            adrInTotal[i.index.values[j][1]] = i['adr'].iloc[j]
        adrTotal[i.index.values[0][0]] = adrInTotal
    return adrDic, adrTotal

def dictionryOutputWithParam(dictionary):
    adrDic = {}
    adrTotal = {}

    for i in dictionary:
        # print(i)
        adrInTotal = {}
        for j in range( len( i ) ):
            adrInTotal[i.index.values[j][1]] = i['adr'].iloc[j]
        adrTotal[i.index.values[0][0]] = adrInTotal
    return adrTotal

def financialYearPattern(dic1, dic2):
    # adrDic = dictionryOutput()[0]
    # adrTotalDic = dictionryOutput()[1]
    adrDic = dic1
    adrTotalDic = dic2
    seasonalDic = {}
    internalDic = {}
    seasonalTotalDic = {}
    internalTotalDic = {}
    count1 = 1
    count2 = 1

    valueList = []

    for keys, values in adrDic.items():
        for i in values.keys():
            valueList.append(values[i])

    monthCount = len(valueList)
    incCount1 = 0
    incCount2 = 0

    for keys, values in adrDic.items():
        for i in values.keys():

            if i == 'June':
                keyVal = 'season' + str( count1 )
                internalDic[i] = values[i]
                incCount1 += 1
                seasonalDic[keyVal] = internalDic
                internalDic = {}
                # internalDic = {}
                count1 = count1 + 1
            else:
                incCount1 += 1
                internalDic[i] = values[i]

            if incCount1 == monthCount:
                keyVal = 'season' + str( count1 )
                internalDic[i] = values[i]
                incCount1 += 1
                seasonalDic[keyVal] = internalDic

    for keys, values in adrTotalDic.items():
        for i in values.keys():
            if i == 'June':
                keyVal = 'season' + str( count2 )
                internalTotalDic[i] = values[i]
                incCount2 += 1
                seasonalTotalDic[keyVal] = internalTotalDic
                internalTotalDic = {}
                count2 = count2 + 1
            else:
                incCount2 += 1
                internalTotalDic[i] = values[i]

            if incCount2 == 26:
                keyVal = 'season' + str( count2 )
                internalTotalDic[i] = values[i]
                incCount2 += 1
                seasonalTotalDic[keyVal] = internalTotalDic

    return seasonalDic, seasonalTotalDic

def annualDailyRateAvg():
    avgDic = {}

    season1 = list( financialYearPattern( dictionryOutput()[0], dictionryOutput()[1] )[0]["season1"].values() )
    season2 = list( financialYearPattern( dictionryOutput()[0], dictionryOutput()[1] )[0]["season2"].values() )

    months = list(financialYearPattern( dictionryOutput()[0], dictionryOutput()[1] )[0]['season1'] )

    for i, j, month in zip( season1, season2, months ):
        avgDic[month] = (i + j) / 2

    return avgDic

def annualTotalRevAvg():
    avgDic = {}

    season1 = list( financialYearPattern(dictionryOutput()[0],dictionryOutput()[1])[1]["season1"].values())
    season2 = list(financialYearPattern(dictionryOutput()[0],dictionryOutput()[1])[1]["season2"].values())

    months = list(financialYearPattern( dictionryOutput()[0], dictionryOutput()[1] )[1]['season1'] )

    for i, j, month in zip( season1, season2, months ):
        avgDic[month] = (i + j) / 2

    return avgDic

def yearList():
    return yearlist

def GetClusterWiseDetails():
    output = cl.GetDetailsOfCluster('correct_cluster.csv', 1200000, 'all', 0)

    clusterList = {}
    clusterListA = {}
    clusterListB = {}
    clusterListC = {}

    clusterListA[2015] = '2015'
    clusterListA[2016] = '2016'
    clusterListA[2017] = '2017'

    clusterListA[2015] = output[0]['2015_Revenue_month']
    clusterListA[2016] = output[0]['2016_Revenue_month']
    clusterListA[2017] = output[0]['2017_Revenue_month']

    clusterListB[2015] = '2015'
    clusterListB[2016] = '2016'
    clusterListB[2017] = '2017'

    clusterListB[2015] = output[1]['2015_Revenue_month']
    clusterListB[2016] = output[1]['2016_Revenue_month']
    clusterListB[2017] = output[1]['2017_Revenue_month']

    clusterListC[2015] = '2015'
    clusterListC[2016] = '2016'
    clusterListC[2017] = '2017'

    clusterListC[2015] = output[3]['2015_Revenue_month']
    clusterListC[2016] = output[3]['2016_Revenue_month']
    clusterListC[2017] = output[3]['2017_Revenue_month']

    clusterList[0] = clusterListA
    clusterList[1] = clusterListB
    clusterList[3] = clusterListC

    return clusterList