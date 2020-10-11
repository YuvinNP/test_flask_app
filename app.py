from flask import Flask, render_template, url_for, request
import adr_operations as de
import clustering as cl

app = Flask( __name__ )

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


# season1 = list( de.financialYearPattern()[0]["season1"].values() )
# season2 = list( de.financialYearPattern()[0]["season2"].values() )
# season3 = list( de.financialYearPattern()[0]["season3"].values() )

season1 = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[0]["season1"].values() )
season2 = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[0]["season2"].values() )
season3 = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[0]["season3"].values() )

season1Total = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[1]["season1"].values())
season2Total = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[1]["season2"].values())
season3Total = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[1]["season3"].values())

# season1Cluster0 = list(de.financialYearPattern(de.GetClusterWiseDetails()[0], de.dictionryOutput()[1])[0]["season1"].values())
#
# print(season1Cluster0)
avgValues = list(de.annualDailyRateAvg().values())
avgTotal = list(de.annualTotalRevAvg().values())
yearlist = de.yearList()

print(de.GetClusterWiseDetails())

@app.route('/line', methods=['POST', 'GET'])
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
        return render_template('index.html', title='Bitcoin Monthly Price in USD', max=200, labels=line_labels, values2 = season1_line, values3 = season2_line, avgValues = line_avg, yearlist = var_yearlist, comparison = line_comparison )
        # return (content1+content2)
    else:
        season1_line = season1
        season2_line = season2
        season3_line = season3

        return render_template('index.html', title='Bitcoin Monthly Price in USD', max=200, labels=line_labels,
                               values2 = season1_line, values3 = season2_line, values4 = season3_line,
                               avgValues = line_avg, avgTotal = line_avg_total, yearlist = var_yearlist,
                               season1Total = season1_total, season2Total = season2_total, season3Total = season3_total )


if __name__ == '__main__':
    app.run(debug=True)
