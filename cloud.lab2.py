import json
import urllib.request
import pandas as pd
import boto3
import matplotlib.pyplot as plt

dollar_rates, euro_rates = [], []
for currency in ["usd", "eur"]:
    data = urllib.request.urlopen(f"https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&valcode={currency}&sort=exchangedate&order=asc&json").read()
    output = json.loads(data)
    for rate in output:
        if rate["cc"] == "USD":
            dollar_rates.append({"date": rate["exchangedate"], "USD": rate["rate"]})
        else:
            euro_rates.append({"date": rate["exchangedate"], "EUR": rate["rate"]})

df_dollar = pd.DataFrame(dollar_rates).set_index("date")
df_euro = pd.DataFrame(euro_rates).set_index("date")

df = pd.concat([df_dollar, df_euro], axis=1)
df.to_csv("parsed_data.csv", sep=";")

s3_client = boto3.client('s3', aws_access_key_id="", aws_secret_access_key="")

def upload(file, bucket_name):
    s3_client.upload_file(file, bucket_name, file)

def download(file, bucket_name):
    s3_client.download_file(bucket_name, file, file)

upload("parsed_data.csv", "lab2.cloud")

ax = df.plot(figsize=(15, 7), title="UAH currency", fontsize=12)
ax.set_xlabel("date")
ax.set_ylabel("Exchange rate")
plt.savefig('plot.png')

upload("plot.png", "lab2.cloud")