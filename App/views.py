from this import d
from django.shortcuts import render
from django.http import HttpResponse
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
import json

# Create your views here

from .models import Rules
import pandas as pd

class Data:
    def __init__(self):
        countries_info = pd.read_csv("/home/jagannath/Desktop/development/DBS/App/countries_info.csv")
        countries_info["residential_country_cd"] = countries_info["ENTITY_KEY"]
        customer_info = pd.read_csv("/home/jagannath/Desktop/development/DBS/App/customer_info.csv")
        customer_account_info = pd.read_csv("/home/jagannath/Desktop/development/DBS/App/customer_account_info.csv")
        customer_account_info["party_key"] = customer_account_info["primary_party_key"] 

        # Checking high risk customers
        high_risk_country_customers = pd.merge(customer_info, countries_info, how='inner', on=['residential_country_cd'])

        # high risk customers are 0 

        df = pd.merge(customer_info, customer_account_info, how='inner', on=['party_key'])
        df[" Account_Key"] = df["account_key"]
        customer_transactions = pd.read_csv("/home/jagannath/Desktop/development/DBS/App/customer_transactions.csv")
        customer_transactions.head()

        main = pd.merge(df, customer_transactions, how="inner")
        main.drop(columns = ['primary_party_key', "account_key"], inplace=True)
        main['month'] = main[" Transaction_Date"].apply(lambda x: list(x.split('/'))[2]+'/'+list(x.split('/'))[1])
        main['day'] = main[" Transaction_Date"].apply(lambda x: list(x.split('/'))[0])


        group_by = main.groupby(["month", "party_key"])
        ans = []
        for i in group_by:
            # print(i[0])
            df = pd.DataFrame(i[1])
            # df["type"]
            # print(df.head())
            a = list(i[0]);
            in_cust = df[df[' Transaction Type'] == 'INN'][' Transaction_Amount(in $)'].sum()
            out_cust = df[df[' Transaction Type'] == 'OUT'][' Transaction_Amount(in $)'].sum()
            tot_transactions = df[' Transaction_Amount(in $)'].count()
            a.append(in_cust)
            a.append(out_cust,)
            a.append(tot_transactions)
            # print(in_cust, out_cust, tot_transactions, a)
            ans.append(a)

        self.final_month = pd.DataFrame(ans, columns = ["month", "id", "INN", "OUT", "TOTAL"])


        day_transaction_counts = main.groupby(["month", "day", "party_key"])
        ans = []
        for i in day_transaction_counts:
            a = list(i[0])
            a.append(i[1][" Transaction Type"].count())
            ans.append(a)
            # print(a)

        self.final_day = pd.DataFrame(ans, columns = ["month", "day", "id", "count"])

        
        self.countries = pd.merge(customer_info, countries_info, how='left', on=['residential_country_cd'])[["party_key","residential_country_cd"]]
 
 
def processsing():
    data = Data()
    rules = Rules.objects.all()
    month = data.final_month.to_numpy()  # month, id, inn, out, total
    day = data.final_day.to_numpy()  # month, day, id, total
    country = data.countries.to_numpy() # id, country
    

    m = {}
    for i in range(len(country)):
        m[country[i][0]] = [country[i][0], country[i][1]]
    
    #condtion 1

    for i in range(len(month)):
        if(month[i][4] < rules[0].high_risk_start and month[i][4] >= rules[0].high_risk_end):
            m[month[i][1]].append('H1')
        elif (month[i][4] < rules[0].medium_risk_start and month[i][4] >= rules[0].medium_risk_end):
            m[month[i][1]].append('M1')
        else:
            m[month[i][1]].append('L1')

    #condtion 2

    for i in range(len(month)):
        if(month[i][2] < rules[1].high_risk_start and month[i][2] >= rules[1].high_risk_end):
            m[month[i][1]].append('H2')
        elif (month[i][2] < rules[1].medium_risk_start and month[i][2] >= rules[1].medium_risk_end):
            m[month[i][1]].append('M2')
        else:
            m[month[i][1]].append('L2')
        
    #condtion 3

    for i in range(len(month)):
        if(month[i][3] < rules[2].high_risk_start and month[i][3] >= rules[2].high_risk_end):
            m[month[i][1]].append('H3')
        elif (month[i][3] < rules[2].medium_risk_start and month[i][3] >= rules[2].medium_risk_end):
            m[month[i][1]].append('M3')
        else:
            m[month[i][1]].append('L3')

    #condtion 4

    for i in range(len(day)):
        if(day[i][3] < rules[3].high_risk_start and day[i][3] >= rules[3].high_risk_end):
            m[day[i][2]].append('H4')
        elif (day[i][3] < rules[3].medium_risk_start and day[i][3] >= rules[3].medium_risk_end):
            m[day[i][2]].append('M4')
        else:
            m[day[i][2]].append('L4')

    for i in m:
        if len(m[i])<3: continue
        s = m[i][2]+m[i][3]+m[i][4]+m[i][5]
        if 'H1' in s:
            m[i].append('High')
            m[i].append('H1')
        elif 'H2' in s:
            m[i].append('High')
            m[i].append('H2')
        elif 'H3' in s:
            m[i].append('High')
            m[i].append('H3')
        elif 'H4' in s:
            m[i].append('High')
            m[i].append('H4')
        elif 'M1' in s:
            m[i].append('Medium')
            m[i].append('M1')
        elif 'M2' in s:
            m[i].append('Medium')
            m[i].append('M2')
        elif 'M3' in s:
            m[i].append('Medium')
            m[i].append('M3')
        elif 'M4' in s:
            m[i].append('Medium')
            m[i].append('M4')        
        elif 'L1' in s:
            m[i].append('Low')
            m[i].append('L1')
        elif 'L2' in s:
            m[i].append('Low')
            m[i].append('L2')
        elif 'L3' in s:
            m[i].append('Low')
            m[i].append('L3')
        elif 'L4' in s:
            m[i].append('Low')
            m[i].append('L4')

    final = []
    for i in m:
        if(type(m[i][0]) == float): continue
        if len(m[i])<3: 
            final.append([m[i][0], m[i][1], 'NO', 'No Transaction'])
        else:
            final.append([m[i][0], m[i][1], m[i][-2], m[i][-1]])

    df = pd.DataFrame(final, columns = ["id", 'country', 'risk', 'reason'])
    count_plot = sns.countplot(x=df[df["risk"]!='NO']['risk'])
    fig = count_plot.get_figure()
    fig.savefig("/home/jagannath/Desktop/development/DBS/App/static/countPlot")
    # plt.show()

    return final



def home(request):

    if request.method == 'POST':
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print("body", body)
        obj1 = Rules.objects.get(id=1)
        obj2 = Rules.objects.get(id=2)
        obj3 = Rules.objects.get(id=3)
        obj4 = Rules.objects.get(id=4)
        obj1.high_risk_end = int(body['H1'])
        obj1.medium_risk_start = int(body['M1'])
        obj1.low_risk_end = int(body['L1'])
        obj1.save()
        obj2.high_risk_end = int(body['H2'])
        obj2.medium_risk_end = int(body['M2'])
        obj2.low_risk_start = int(body['L2'])
        obj2.save()
        obj3.high_risk_end = int(body['H3'])
        obj3.medium_risk_end = int(body['M3'])
        obj3.low_risk_start = int(body['L3'])
        obj3.save()
        obj4.high_risk_end = int(body['H4'])
        obj4.medium_risk_end = int(body['M4'])
        obj4.low_risk_start = int(body['L4'])
        obj4.save()
        # rules[0].high_risk_start = int(body['H2']);
    d = {}
    
    d['data'] = processsing()
    d['rules'] = Rules.objects.all()


    return render(request, "index.html", d)