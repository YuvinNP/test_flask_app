import pandas as pd
import numpy as np
from collections import Counter

# initialize global dataframes
Df_dataset = pd.DataFrame()
Df_dataset_top_cluster = pd.DataFrame()
top_cluster = []


def importCSV(path):
    global Df_dataset
    # read the csv
    Df_dataset = pd.read_csv(path)


def GetTopClusters():
    global Df_dataset

    global Df_dataset_top_cluster

    global top_cluster

    # get the Df_dataset to another dataframe
    df_cal = Df_dataset.copy(deep=True)

    # function to get the top 3 segmentations
    # take all the platinum having rows
    Df_dataset_final_platinum = df_cal.loc[df_cal['RFM_Loyalty_Level'] == 'Platinum'].sort_values('id', ascending=False)

    # get the each segment platnum count
    Df_dataset_final_platinum = Df_dataset_final_platinum.groupby(['Cluster'])['id'].aggregate(
        'count').reset_index().sort_values('id', ascending=False)

    # if the total ids greater than 1000 then take those as main clusters
    # loop the dataframe and check for the above condition
    # get the cluster numbers to list
    top_cluster = [gid['Cluster'] for index, gid in Df_dataset_final_platinum.iterrows() if gid['id'] > 1000]

    # get all the rows which have cluster number in the above
    Df_dataset_top_cluster = df_cal.loc[(df_cal['Cluster'].isin(top_cluster))].sort_values('Cluster', ascending=True)

    # now we have the required segment data


def CustomCluster(clusterno):
    global Df_dataset

    global Df_dataset_top_cluster

    global top_cluster

    # get the Df_dataset to another dataframe
    df_cal = Df_dataset.copy(deep=True)

    # get the cluster numbers to list
    top_cluster = [clusterno]
    # get all the rows which have cluster number in the above
    Df_dataset_top_cluster = df_cal.loc[(df_cal['Cluster'].isin(top_cluster))].sort_values('Cluster', ascending=True)


# get the country language and employee skill of each clusters
# cluster number needed if it is a customer cluster details needed

def GetDetailsOfCluster(path, roi, processtype, clusternumber):
    global Df_dataset_top_cluster

    global Df_dataset

    global top_cluster

    # import the dataset
    importCSV(path)

    if (processtype == 'all'):
        # get the top clusters
        GetTopClusters()

    elif (processtype == 'custom'):
        CustomCluster(clusternumber)

    # to save all the date
    clusterdict = {}

    # to save employee requirement satisfy
    # to check whether is employee for main countries
    employeelanguage = ['FRA', 'GBR']

    # to filter unwanted months by getting mean and getting needed months
    meanmonth = 0

    # ROI calculation
    ROI = roi

    for cluster in top_cluster:

        # use this to remove unwanted months which have low frequencies of guest
        meanmonthcount = 0;

        # to store the lead time
        meancanceldays = 0

        # to store the  loyalty count of each segment
        loyalty_dict = {}

        # to store the is cancel data
        cancel_data_dict = {}

        # to save the year's each month revenue and total revenue
        # cal Monetary of each year by month
        yr_15 = {}
        yr_15_total = 0
        yr_15_roi_percentage = 0

        yr_16 = {}
        yr_16_total = 0
        yr_16_roi_percentage = 0

        yr_17 = {}
        yr_17_total = 0
        yr_17_roi_percentage = 0

        # for food
        Eachclusterfoodcount = {}

        # for room type
        Eachclusterroomcount_dict = {}

        # for employees
        Eachclustercountrycount = {}

        # combine dictionary
        combine_dict = {}

        # to save employee requirement satisfy
        employee_ava_dict = {}

        # to save each segment month visiting and the count
        Eachclustermonthcount = {}

        # copy the dataframe data for further calculations
        df_temp = Df_dataset_top_cluster.loc[Df_dataset_top_cluster['Cluster'] == cluster][
            ['meal', 'country', 'arrival_date_month', 'arrival_date_year', 'Monetary', 'RFM_Loyalty_Level',
             'is_canceled', 'id', 'lead_time', 'reserved_room_type']].copy(deep=True)

        # get all the loyalty level
        temployalty = df_temp['RFM_Loyalty_Level'].tolist()

        # get the is cancel column  detail to get the percentage of cancel and coming
        tempiscancel = df_temp.groupby(['is_canceled'])[['id']].aggregate('count').sort_values('id', ascending=False)[
            'id'].tolist()

        # getting the data in ascending order of id
        # there for first index in 0 and next is 1
        cancelindex = 0;
        for cancel in tempiscancel:
            cancel_data_dict[cancelindex] = cancel
            cancelindex = cancelindex + 1

        # store the number of rows
        noofrows = len(temployalty)

        # get the cancel and uncancel means, we used this array to store the o and 1s
        tempcancelleadtime = df_temp.loc[df_temp['is_canceled'] == 1]['lead_time'].tolist()

        # cal mean lead days to cancel
        if (len(tempcancelleadtime) != 0):
            meancanceldays = sum(tempcancelleadtime) / len(tempcancelleadtime)

        # get all the meals
        tempfood = df_temp['meal'].tolist()

        # get the countries
        tempcountry = df_temp['country'].tolist()
        countrynames = list(set(tempcountry))

        # get the months
        tempmonth = df_temp['arrival_date_month'].tolist()
        monthname = list(set(tempmonth))

        # get the room types
        temproom = df_temp['reserved_room_type'].tolist()

        # get the Monetary
        tempmonetary = df_temp.groupby(['arrival_date_year', 'arrival_date_month'])['Monetary'].aggregate(
            'sum').reset_index().sort_values('arrival_date_year', ascending=False)

        # replace undefined with special requests
        tempfood = list(map(lambda st: str.replace(st, "Undefined", "Special Requests"), tempfood))

        # used to loop to make time less
        foodname = list(set(tempfood))

        # count each food frequencies
        for foodele in foodname:
            Eachclusterfoodcount[foodele] = tempfood.count(foodele)

        # count each month frequencies
        for monthele in monthname:
            # get the month count
            monthcounter = tempmonth.count(monthele)
            Eachclustermonthcount[monthele] = monthcounter
            meanmonthcount = meanmonthcount + monthcounter

        # now get the mean and remove unwanted months
        meanmonth = meanmonthcount / len(monthname)

        # loop and kemove those keys which are less than mean
        for removeindex in list(Eachclustermonthcount.keys()):

            if (Eachclustermonthcount[removeindex] < meanmonth):
                del Eachclustermonthcount[removeindex]

                # to keep track of only main countries
        countcountries = 0

        for countryele in countrynames:

            count = tempcountry.count(countryele)

            # if countcountries == 3 that means stops practicaly in a hotel we can have 3 segments
            if (countcountries == 3):
                break
                # there should be 1000 atleast coustomers for each country to make it considerable
            if (count > 1000):
                Eachclustercountrycount[countryele] = count
                countcountries = countcountries + 1

            # check for the lack of employee for each country language
        for coun in Eachclustercountrycount.keys():

            # check whether country language incldued
            if coun in employeelanguage:
                employee_ava_dict[coun] = 'Yes'
            else:
                employee_ava_dict[coun] = 'No'

        # count each loyalty frequency
        loyalty_dict = Counter(temployalty)

        # count each room frequency
        Eachclusterroomcount_dict = Counter(temproom)

        # iterate the dataframe
        for index, row in tempmonetary.iterrows():

            # get each years month revenue based on the year
            if (row['arrival_date_year'] == 2015):

                yr_15[row['arrival_date_month']] = row['Monetary']
                yr_15_total = yr_15_total + row['Monetary']

            elif (row['arrival_date_year'] == 2016):

                yr_16[row['arrival_date_month']] = row['Monetary']
                yr_16_total = yr_16_total + row['Monetary']

            else:

                yr_17[row['arrival_date_month']] = row['Monetary']
                yr_17_total = yr_17_total + row['Monetary']

        yr_15_roi_percentage = int((yr_15_total / ROI) * 100)
        yr_16_roi_percentage = int((yr_16_total / ROI) * 100)
        yr_17_roi_percentage = int((yr_17_total / ROI) * 100)

        # combine the above dictionaries
        combine_dict = {'food': Eachclusterfoodcount.copy(),
                        'country': Eachclustercountrycount.copy(),
                        'employee_skill': employee_ava_dict.copy(),
                        'month_name': Eachclustermonthcount.copy(),
                        'loyalty': loyalty_dict.copy(),
                        'roomcount': Eachclusterroomcount_dict.copy(),
                        '2015_Revenue_month': yr_15.copy(),
                        '2016_Revenue_month': yr_16.copy(),
                        '2017_Revenue_month': yr_17.copy(),
                        '2015_total_revenue': yr_15_total,
                        '2016_total_revenue': yr_16_total,
                        '2017_total_revenue': yr_17_total,
                        'ROI_percentage_2015': yr_15_roi_percentage,
                        'ROI_percentage_2016': yr_16_roi_percentage,
                        'ROI_percentage_2017': yr_17_roi_percentage,
                        'meancanceldays': meancanceldays,
                        'canceldetails': cancel_data_dict.copy()
                        }

        # save each of those data to main dictionary

        clusterdict[cluster] = combine_dict

    return clusterdict





def CalTotalGivenTimeRange(year, monthrange, cluster):
    global Df_dataset_top_cluster

    # to store each month count , help to get the mean
    monthcount = {}

    # to store the each month monetary
    monthmonetary = {}

    # group  by year
    df_full = Df_dataset_top_cluster.loc[Df_dataset_top_cluster['Cluster'].isin(cluster)].groupby(
        ['arrival_date_year', 'arrival_date_month'])['Monetary'].aggregate('sum').reset_index().sort_values(
        'arrival_date_year', ascending=False).copy(deep=True)

    # now get the required year data

    for yr in year:

        # get the respective
        df_year_filer = df_full.loc[df_full['arrival_date_year'] == yr].sort_values('arrival_date_year',
                                                                                    ascending=True).copy(deep=True)

        # now loop and get each month monetary
        for index, row in df_year_filer.iterrows():

            if (row['arrival_date_month'] in monthrange):

                # check for the exist of the dictionry
                if (row['arrival_date_month'] in monthmonetary):

                    # add to the monetary count of the month
                    monthmonetary[row['arrival_date_month']] = monthmonetary[row['arrival_date_month']] + row[
                        'Monetary']

                    # add to the month count
                    monthcount[row['arrival_date_month']] = monthcount[row['arrival_date_month']] + 1

                else:

                    # create to the monetary count of the month
                    monthmonetary[row['arrival_date_month']] = row['Monetary']

                    # create to the month count
                    monthcount[row['arrival_date_month']] = 1

    # now get the mean of each month
    meanmonths = {key: value / monthcount[key] for key, value in monthmonetary.items()}

    return meanmonths

import operator


def FinancialOfferCalculations(year, monthrange, maxdiscountPercentage):
    # to store each segment volumne
    requirecount_dict = {}

    # to store each segment earning
    requireearn_dict = {}

    # to store each segmnet discount
    discount_seg = {}

    # to store each segment discoutn loss by taking fom total revenue
    discount_loss = {}

    # to store discoutn loss per person
    discount_loss_per_guest = {}

    # to store revenue each month
    revenue_month = {}

    # to temporalu to store each segment month frequency and get count
    tempmonthcount = {}

    # combine dictionary to get all the output to single dictioanry
    combine_dict = {}

    # get the details of the cluster
    output = GetDetailsOfCluster("cltData.csv", 1200000, 'all', 0)

    # get each segment mean guest volume
    for key in list(output.keys()):

        # initialize intial count as 0
        requirecount_dict[key] = 0

        # check month dictionary of the respective segment
        monthdict = output[key]['month_name'].copy()

        # loop the monthdict and get the total volume for given time range
        for mon_name in monthrange:

            # check if month name exits in the month dictionary otherwise it will give error
            if mon_name in monthdict:
                # updte the count of each segmnet
                requirecount_dict[key] = requirecount_dict[key] + monthdict[mon_name]

    # no purpose of having no guests in the given range
    if (0 in requirecount_dict):
        del requirecount_dict[0]

        # get sum of all values of the segment whuch will use the below code to cal the dicount percentage
    sumsegcount = sum(list(requirecount_dict.values()))

    # get the discount for each segment
    discount_seg = {seg: (val / sumsegcount) * maxdiscountPercentage for seg, val in requirecount_dict.items()}

    # now get the loss for each segment because of the discount
    # before that get the total revue of each given month for each segment from CalTotalGivenTimeRange fucntion
    for clus in list(requirecount_dict.keys()):
        temprevenue_month = CalTotalGivenTimeRange(year, monthrange, [clus])
        revenue_month[clus] = sum(list(temprevenue_month.values()))

    # now calculate the loss for each cluster from the discount
    # loop the each segment and cal
    for clus in list(revenue_month.keys()):
        # now cal the loss and insert to new dictionary
        discount_loss[clus] = revenue_month[clus] * discount_seg[clus]
        discount_loss_per_guest[clus] = discount_loss[clus] / sumsegcount

    # combine the output
    combine_dict = {'segment_discount_percentage': discount_seg.copy(),
                    'segment_loss_from_discount': discount_loss.copy(),
                    'recover_amount_per_guest': discount_loss_per_guest.copy(),
                    'sum_of_guest': sumsegcount,
                    'mean_guest_count': requirecount_dict.copy()

                    }

    # output the discount , loss from discount, loss dicount to cover from person
    # what cross selling to insert in the recommendation
    return combine_dict

FinancialOfferCalculations([2015,2017],['January','August','July'],40)