# Code for ETL operations on Country-GDP data

# Importing the required libraries

import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime


url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_name = 'Largest_banks'
table_attribs = ['Name','MC_USD_Billion']
db_name = 'Banks.db'
csv_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-PY0221EN-Coursera/labs/v2/exchange_rate.csv'
csv_path = './Largest_banks_data.csv'


def extract(url, table_attribs):
    
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    df = pd.DataFrame(columns = table_attribs)
    tables = soup.find_all('tbody')[0]
    rows = tables.find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            hyper = col[1].find_all('a')[1]
            if hyper is not None:
                data_dict = {
                    'Name': hyper.contents[0],
                    'MC_USD_Billion': col[2].contents[0]
                }
                df1 = pd.DataFrame(data_dict, index = [0])
                df = pd.concat([df, df1], ignore_index = True)
    currency_list = list(df['MC_USD_Billion'])
    currency_list = [float(''.join(x.split('\n'))) for x in currency_list]
    df['MC_USD_Billion'] = currency_list

    return df


def transform(df, csv_url):
    content_csv = pd.read_csv(csv_url)
    dic = content_csv.set_index('Currency').to_dict()['Rate']
    df['MC_GBP_Billion'] = round(df['MC_USD_Billion']*dic['GBP'],2)
    df['MC_EUR_Billion'] = round(df['MC_USD_Billion']*dic['EUR'],2)
    df['MC_INR_Billion'] = round(df['MC_USD_Billion']*dic['INR'],2)
    return df


def load_to_csv(df, csv_path):
    df.to_csv(csv_path)


def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)
    print()

def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("./code_log.txt","a") as f:
        f.write(timestamp+':'+message+'\n')

log_progress('Preliminaries complete. Initiating ETL process.')
df = extract(url, table_attribs)
log_progress('Data extraction complete. Initiating Transformation process.')

df = transform(df, csv_url)
log_progress('Data transformation complete. Initiating loading process.')
load_to_csv(df, csv_path)
log_progress('Data saved to CSV file.')

sql_connection = sqlite3.connect('Banks.db')
log_progress('SQL Connection initiated.')
load_to_db(df, sql_connection, table_name)
log_progress('Data loaded to Database as table. Running the query.')
query_statement = f"SELECT * from Largest_banks"
run_query(query_statement, sql_connection)
log_progress('Data loaded to Database as table. Running the query.')
run_query(query_statement, sql_connection)
query_statement = f"SELECT AVG(MC_GBP_Billion) FROM Largest_banks "
run_query(query_statement, sql_connection)
log_progress('Data loaded to Database as table. Running the query.')
query_statement = f"SELECT Name from Largest_banks LIMIT 5"
run_query(query_statement, sql_connection)
log_progress('Process Complete.')
sql_connection.close()

