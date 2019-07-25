import datetime
import mysql.connector
import pandas as pd
import numpy as np
import json
import time
import re

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="H0rr0rland$",
    auth_plugin="mysql_native_password",
    database="saturnine"
)

cursor = mydb.cursor()


def dis(table_name):
    df = pd.read_sql('SELECT * FROM ' + table_name, con=mydb)
    np.savetxt('data.txt', df.values, fmt='%s %d %d %s %d %s %d', delimiter="\t")
    return process_text_to_json()
    

def process_text_to_json():
    data = []
    with open("data.txt") as f:
        for line in f:
            line = line.split()
            data.append([int(line[1]), int(line[2]), int(line[4]), int(line[6])])

    return data
    