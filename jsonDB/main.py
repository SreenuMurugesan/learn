import json
import pandas as pa


def insert_user(name, password, access, df):
    df.loc[len(df)] = [name, password, access]
    return df


with open('db.json') as myDB:
    buffer = myDB.read()
    data = json.loads(buffer)

print("--------JSON DATA--------")
print(data)

df = pa.DataFrame(columns=['name', 'password', 'access'])
for user in data:
    temp_list = [user['name'], user['password'], user['access']]
    df.loc[len(df)] = temp_list
    temp_list.clear()

print("--------DATA FRAME--------")
print(df)

df = insert_user('rasik', 'rasik12', 3, df)
print("--------NEW USER--------")
print(df)

json_ = df.to_json(orient='records')
print("--------NEW JSON DATA--------")
print(json_)

with open('new_db.json', 'w') as myfile:
    myfile.write(json_)
