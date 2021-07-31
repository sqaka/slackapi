import configparser
import pandas as pd
import slack


conf = configparser.ConfigParser()
conf.read('./utils/params.ini')
url = conf['slack']['url']
token = conf['slack']['token']
client = slack.WebClient(token=token)

response = client.users_list()
members = response.data['members']

cols = 'id', 'name', 'slack_name', 'deleted'
df = pd.DataFrame(index=[], columns=cols)
for member in members:
    record = pd.Series([member['id'], member['name'],
                        member['profile']['display_name'],
                        member['deleted']],
                       index=df.columns)
    df = df.append(record, ignore_index=True)

df.to_csv('./userlist.csv', index=False)
