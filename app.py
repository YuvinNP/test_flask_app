from flask import Flask, render_template, url_for, request

app = Flask( __name__ )

# labels = []
#
# count = 0
# for keys, values in de.dictionryOutput()[0].items():
#     for i in values.keys():
#         # print(i)
#         if i == "June":
#             labels.append(i)
#             count += 1
#             break
#         else:
#             labels.append(i)
#     if count > 0:
#         break
#
#
# # season1 = list( de.financialYearPattern()[0]["season1"].values() )
# # season2 = list( de.financialYearPattern()[0]["season2"].values() )
# # season3 = list( de.financialYearPattern()[0]["season3"].values() )
#
# season1 = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[0]["season1"].values() )
# season2 = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[0]["season2"].values() )
# season3 = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[0]["season3"].values() )
#
# season1Total = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[1]["season1"].values())
# season2Total = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[1]["season2"].values())
# season3Total = list( de.financialYearPattern(de.dictionryOutput()[0], de.dictionryOutput()[1])[1]["season3"].values())
#
# # season1Cluster0 = list(de.financialYearPattern(de.GetClusterWiseDetails()[0], de.dictionryOutput()[1])[0]["season1"].values())
# #
# # print(season1Cluster0)
# avgValues = list(de.annualDailyRateAvg().values())
# avgTotal = list(de.annualTotalRevAvg().values())
# yearlist = de.yearList()
#
# print(de.GetClusterWiseDetails())

@app.route('/')
def index():
    return 'hello...!'

if __name__ == '__main__':
    app.run(debug=True)
