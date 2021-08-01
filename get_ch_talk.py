import configparser
from datetime import datetime
import errno
import os
import pandas as pd
import slack

import click

SAVE_DIR = './export/'
CONF_PATH = './utils/params.ini'


def token_init(conf):
    if not os.path.exists(CONF_PATH):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), CONF_PATH)
    conf.read(CONF_PATH)
    token = conf['slack']['token']
    client = slack.WebClient(token=token)

    return client


def get_ch_talk(conf, client, category):
    cols = 'channel', 'user', 'timestamp', 'text'
    df = pd.DataFrame(index=[], columns=cols)

    for i in range(len(conf['{}'.format(category)])):
        channel_id = conf['{}'.format(category)]['ch{}'.format(i)]
        print('{}. now aggregating in: {}'.format(i, channel_id))
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


def export_data(df, category):
    os.makedirs(SAVE_DIR, exist_ok=True)
    now = datetime.now()
    dt_txt = '{0:%m%d%H%M}'.format(now)
    df.to_csv('{}{}_{}_talklog.csv'.format(
        SAVE_DIR, dt_txt, category), index=False)


@click.command()
@click.option('--category', '-c', type=str, default='category02')
def main(category):
    conf = configparser.ConfigParser()
    client = token_init(conf)
    df = get_ch_talk(conf, client, category)
    export_data(df, category)


if __name__ == '__main__':
    main()
