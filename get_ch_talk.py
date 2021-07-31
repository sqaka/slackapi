import configparser
from datetime import datetime
import pandas as pd
import slack


def token_init(conf):
    token = conf['slack']['token']
    client = slack.WebClient(token=token)

    return client


def get_ch_talk(conf, client):
    cols = 'channel', 'user', 'timestamp', 'text'
    df = pd.DataFrame(index=[], columns=cols)

    for i in range(11):
        channel_id = conf['channel']['ch{}'.format(i)]
        response = client.conversations_history(channel=channel_id)
        messages = response.data['messages']

        for message in messages:
            thread = client.conversations_replies(
                channel=channel_id, ts=message['ts'])
            if thread['ok'] is True:
                replies = thread.data['messages']
                for reply in replies:
                    if reply['ts'] is message['ts']:
                        pass
                    timestamp = datetime.fromtimestamp(
                        round(float(reply['ts'])))
                    record = pd.Series([channel_id,
                                        reply['user'],
                                        timestamp,
                                        reply['text']],
                                       index=df.columns)
                    df = df.append(record, ignore_index=True)

    return df


def main():
    conf = configparser.ConfigParser()
    conf.read('./utils/params.ini')
    client = token_init(conf)
    df = get_ch_talk(conf, client)
    df.to_csv('./ch_talk.csv', index=False)


if __name__ == '__main__':
    main()
