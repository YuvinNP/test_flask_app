from flask import Flask , render_template, request
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pickle
import datetime as dt
import Call as cl
import adr_operations as de
app =Flask(__name__)
B_model = pickle.load(open('RF_model.pkl','rb'))
S_model = pickle.load(open('RF_Seg_model.pkl','rb'))

output = cl.GetDetailsOfCluster("cltData.csv",1200000,'custom',2)

########################################################################################
################################Segment Comparison Charts####################################



#Getting output dictionary from classification.py
output = cl.GetDetailsOfCluster("correct_cluster.csv",1200000,'all',0)
output3 = cl.GetDetailsOfCluster("correct_cluster.csv",1200000,'custom',3)

#######################################TOTAL REVENUE - BAR CHART
trlabels = [2015,2016,2017]

#Segment 01
trvalues = []

trvalues.append(output[0]['2015_total_revenue'])
trvalues.append(output[0]['2016_total_revenue'])
trvalues.append(output[0]['2017_total_revenue'])

#Segment 02
trvalues2 = []

trvalues2.append(output[1]['2015_total_revenue'])
trvalues2.append(output[1]['2016_total_revenue'])
trvalues2.append(output[1]['2017_total_revenue'])

#Segment 03
trvalues3 = []

trvalues3.append(output3[3]['2015_total_revenue'])
trvalues3.append(output3[3]['2016_total_revenue'])
trvalues3.append(output3[3]['2017_total_revenue'])




######################################COUNTRIES - PIE CHART

#Segment 1
cdlabels = []
cdvalues = []

for i,j in output[0]['country'].items():
    cdlabels.append(i)
    cdvalues.append(j)


#Segment 2
cdlabels2 = []
cdvalues2 = []

for i,j in output[1]['country'].items():
    cdlabels2.append(i)
    cdvalues2.append(j)


#Segment 3
cdlabels3 = []
cdvalues3 = []

for i,j in output3[3]['country'].items():
    cdlabels3.append(i)
    cdvalues3.append(j)




##########################################SEASONAL MONTHS - BAR CHART
smlabels = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August', 'September',
    'October', 'November', 'December']

#Segment 1
smvalues = []

for i in smlabels:
    if i not in output[0]['month_name'].keys():
        smvalues.append(0)
    else:
        smvalues.append(output[0]['month_name'][i])

#Segment 2
smvalues2 = []

for i in smlabels:
    if i not in output[1]['month_name'].keys():
        smvalues2.append(0)
    else:
        smvalues2.append(output[1]['month_name'][i])


#Segment 3
smvalues3 = []

for i in smlabels:
    if i not in output3[3]['month_name'].keys():
        smvalues3.append(0)
    else:
        smvalues3.append(output3[3]['month_name'][i])






##########################################LOYALTY - PIE CHART

#Segment 1
lolabels = []
lovalues = []
loyal = []
for i,j in output[0]['loyalty'].items():
    lolabels.append(i)
    loyal.append(j)
for k in loyal:
    lovalues.append(k*100/sum(loyal))

#Segment 2
lolabels2 = []
lovalues2 = []
loyal2 = []
for i,j in output[1]['loyalty'].items():
    lolabels2.append(i)
    loyal2.append(j)
for k in loyal2:
    lovalues2.append(k*100/sum(loyal2))


#Segment 3
lolabels3 = []
lovalues3 = []
loyal3 = []
for i,j in output3[3]['loyalty'].items():
    lolabels3.append(i)
    loyal3.append(j)
for k in loyal3:
    lovalues3.append(k*100/sum(loyal3))




###########################################ROI VALUES - BAR CHART
roilabels = [2015,2016,2017]

#Segment 1
roivalues = []

roivalues.append(output[0]['ROI_percentage_2015'])
roivalues.append(output[0]['ROI_percentage_2016'])
roivalues.append(output[0]['ROI_percentage_2017'])

#Segment 2
roivalues2 = []

roivalues2.append(output[1]['ROI_percentage_2015'])
roivalues2.append(output[1]['ROI_percentage_2016'])
roivalues2.append(output[1]['ROI_percentage_2017'])

#Segment 3
roivalues3 = []

roivalues3.append(output3[3]['ROI_percentage_2015'])
roivalues3.append(output3[3]['ROI_percentage_2016'])
roivalues3.append(output3[3]['ROI_percentage_2017'])




##############################FOOOD CATEGORIES - HORIZONTAL BAR CHART

#Segment 1
foodlabels = []
foodvalues = []

for i,j in output[0]['food'].items():
    if i == 'Special Requests':
        foodlabels.append('SR')
    else:
        foodlabels.append(i)
    foodvalues.append(j)


#Segment 2
foodlabels2 = []
foodvalues2 = []

for i,j in output[1]['food'].items():
    if i == 'Special Requests':
        foodlabels2.append('SR')
    else:
        foodlabels2.append(i)
    foodvalues2.append(j)


#Segment 3
foodlabels3 = []
foodvalues3 = []

for i,j in output3[3]['food'].items():
    if i == 'Special Requests':
        foodlabels3.append('SR')
    else:
        foodlabels3.append(i)
    foodvalues3.append(j)



##########################################EMPLOYEE SKILL

#Segment 1
dic1 = output[0]['employee_skill']

#Segment 2
dic12 = output[1]['employee_skill']

#Segment 3
dic13 = output3[3]['employee_skill']




##########################################CANCELLED DATES

#Segment 1
cdates = output[0]['canceldetails'][0]

#Segment 1
cdates2 = output[1]['canceldetails'][0]

#Segment 3
cdates3 = output3[3]['canceldetails'][0]



######################################
#######################################FUNCTION IMPLEMENTATION

#yuvins code

labels = []

count = 0
for keys, values in de.dictionryOutput()[0].items():
    for i in values.keys():
        # print(i)
        if i == "June":
            labels.append(i)
            count += 1
            break
        else:
            labels.append(i)
    if count > 0:
        break



colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


season1 = list( de.financialYearPattern()[0]["season1"].values() )
season2 = list( de.financialYearPattern()[0]["season2"].values() )
season3 = list( de.financialYearPattern()[0]["season3"].values() )

season1Total = list( de.financialYearPattern()[1]["season1"].values())
season2Total = list( de.financialYearPattern()[1]["season2"].values())
season3Total = list( de.financialYearPattern()[1]["season3"].values())

avgValues = list(de.annualDailyRateAvg().values())
avgTotal = list(de.annualTotalRevAvg().values())
yearlist = de.yearList()

#yuvin code end
@app.route('/')
@app.route('/Workspace')
def index():
    return render_template('welcome.html')

@app.route("/predict", methods=['POST','GET'])
def predict():
    x_pred=[]
    featurs=['lead_time','previous_cancellations','previous_bookings_not_canceled','booking_changes','agent','days_in_waiting_list','adr','required_car_parking_spaces','total_of_special_requests']
    for i in featurs:
        x_pred.append(float(request.form.get(i)))
    x=pd.DataFrame([x_pred])
    ariving_date = int(request.form.get('lead_time'))
    adults=int(request.form.get('adults'))
    babys = int(request.form.get('babys'))
    children = int(request.form.get('children'))
    date = request.form.get('booking_date')
    number_of_nights=int(request.form.get('number_of_days'))
    adr=float(request.form.get('adr'))

    date_time_obj = dt.datetime.strptime(date, '%Y-%m-%d')
    Recency=(getLatestTime(2018,1,1)-date_time_obj).days
    Frequency=babys+children+adults
    Monetary=adr*number_of_nights

    B_pred=B_model.predict(x)
    B_output= round(B_pred[0])

    x = pd.DataFrame([[Recency, Frequency, Monetary]])
    S_pred = S_model.predict(x)
    S_output = round(S_pred[0])


    output = cl.GetDetailsOfCluster("cltData.csv", 1200000, 'custom', S_output)
    details={}
    details['food']=max(output[S_output]['food'],key=output[S_output]['food'].get)
    details['room']=max(output[S_output]['roomcount'],key=output[S_output]['roomcount'].get)
    output=cl.FinancialOfferCalculations([2015,2017],['January','August','July'],40)['segment_discount_percentage']
    details['discount']=''
    if (S_output in output.keys()):
        details['discount']=str(round(output[S_output]))+'%'
    else:
        details['discount']='No Discount'
    details['lead_time']=ariving_date
    if(ariving_date>25 ):
        details['text']='The Guest passed the maximum No of arrival days in this segment ,Try to book before 25 no of days'
    else:
        details['text']=''

    if B_pred ==1:
        return render_template('bad.html', out=details)
    else:
        return render_template('good.html', out=details, child=children, adu=adults)


@app.route('/Dashbord', methods=['POST', 'GET'])
def showLineChart():
    line_labels = labels
    print(line_labels)
    line_avg_total = avgTotal
    season1_line = ''
    line_avg = avgValues
    season1_total = season1Total
    season2_total = season2Total
    season3_total = season3Total
    var_yearlist = ['F-Year 1', 'F-Year 2', 'F-Year 3']

    if request.method == 'POST':
        content1 = request.form['cyear']
        content2 = request.form['pyear']
        line_comparison = content1 + " vs " + content2
        if content1 == 'F-Year 1':
            season1_line = season1
        elif content1 == 'F-Year 2':
            season1_line = season2
        else:
            season1_line = season3

        if content2 == 'season1':
            season2_line = season1
        elif content2 == 'season2':
            season2_line = season2
        else:
            season2_line = season2
        return render_template('charts.html', title='Bitcoin Monthly Price in USD', max=200, labels=line_labels, values2 = season1_line, values3 = season2_line, avgValues = line_avg, yearlist = var_yearlist, comparison = line_comparison )
        # return (content1+content2)
    else:
        season1_line = season1
        season2_line = season2
        season3_line = season3

        return render_template('charts.html', title='Bitcoin Monthly Price in USD', max=200, labels=line_labels,
                               values2 = season1_line, values3 = season2_line, values4 = season3_line,
                               avgValues = line_avg, avgTotal = line_avg_total, yearlist = var_yearlist,
                               season1Total = season1_total, season2Total = season2_total, season3Total = season3_total )

@app.route('/Discount')
def getDiscount():
    return render_template('Discount_meter.html')


@app.route('/Customer_Segmentation')
def Countrypie():
    #Segment 1
    bar_label_1 = trlabels
    bar_value_1 = trvalues
    bar_label_2 = smlabels
    bar_value_2 = smvalues
    bar_label_3 = roilabels
    bar_value_3 = roivalues
    hor_label_1 = foodlabels
    hor_value_1 = foodvalues
    pie_label_1 = cdlabels
    pie_value_1 = cdvalues
    pie_label_2 = lolabels
    pie_value_2 = lovalues
    cdays = cdates
    dic2 = dic1

    #Segment 2
    bar_label_12 = trlabels
    bar_value_12 = trvalues2
    bar_label_22 = smlabels
    bar_value_22 = smvalues2
    bar_label_32 = roilabels
    bar_value_32 = roivalues2
    hor_label_12 = foodlabels2
    hor_value_12 = foodvalues2
    pie_label_12 = cdlabels2
    pie_value_12 = cdvalues2
    pie_label_22 = lolabels2
    pie_value_22 = lovalues2
    cdays2 = cdates2
    dic22 = dic12


    #Segment 3
    bar_label_13 = trlabels
    bar_value_13 = trvalues3
    bar_label_23 = smlabels
    bar_value_23 = smvalues3
    bar_label_33 = roilabels
    bar_value_33 = roivalues3
    hor_label_13 = foodlabels3
    hor_value_13 = foodvalues3
    pie_label_13 = cdlabels3
    pie_value_13 = cdvalues3
    pie_label_23 = lolabels3
    pie_value_23 = lovalues3
    cdays3 = cdates3
    dic23 = dic13


    return render_template('seg_charts.html', title='Segment Chart Description', max=13500,

                           #Segment 01
                           clabels=pie_label_1, cvalues = pie_value_1,
                           tlabels=bar_label_1, tvalues = bar_value_1,
                           smlabels=bar_label_2, smvalues = bar_value_2,
                           loylabels=pie_label_2, loyvalues = pie_value_2,
                           rolabels=bar_label_3, rovalues = bar_value_3,
                           flabels=hor_label_1, fvalues = hor_value_1,
                           cdays = cdays, dic3 = dic2,


                           #Segment 2
                           clabels2=pie_label_12, cvalues2=pie_value_12,
                           tlabels2=bar_label_12, tvalues2=bar_value_12,
                           smlabels2=bar_label_22, smvalues2=bar_value_22,
                           loylabels2=pie_label_22, loyvalues2=pie_value_22,
                           rolabels2=bar_label_32, rovalues2=bar_value_32,
                           flabels2=hor_label_12, fvalues2=hor_value_12,
                           cdays2=cdays2, dic32=dic22,

                           # Segment 03
                           clabels3=pie_label_13, cvalues3=pie_value_13,
                           tlabels3=bar_label_13, tvalues3=bar_value_13,
                           smlabels3=bar_label_23, smvalues3=bar_value_23,
                           loylabels3=pie_label_23, loyvalues3=pie_value_23,
                           rolabels3=bar_label_33, rovalues3=bar_value_33,
                           flabels3=hor_label_13, fvalues3=hor_value_13,
                           cdays3=cdays3, dic33=dic23,
                           )


def getLatestTime(year, month, day):
    # get the newest date
    newdate = dt.datetime(year, month, day)

    return newdate



if __name__ == "__main__":
    app.run(debug=True)

