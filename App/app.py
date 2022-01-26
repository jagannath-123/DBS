import pandas as pd

class Data:
    def __init__(self):
        countries_info = pd.read_csv("countries_info.csv")
        countries_info["residential_country_cd"] = countries_info["ENTITY_KEY"]
        customer_info = pd.read_csv("customer_info.csv")
        customer_account_info = pd.read_csv("customer_account_info.csv")
        customer_account_info["party_key"] = customer_account_info["primary_party_key"] 

        # Checking high risk customers
        high_risk_country_customers = pd.merge(customer_info, countries_info, how='inner', on=['residential_country_cd'])

        # high risk customers are 0 

        df = pd.merge(customer_info, customer_account_info, how='inner', on=['party_key'])
        df[" Account_Key"] = df["account_key"]
        customer_transactions = pd.read_csv("customer_transactions.csv")
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
 