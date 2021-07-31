import configparser
import pandas as pd
import slack


def token_init(conf):
    token = conf['slack']['token']
    client = slack.WebClient(token=token)

    return client


def get_ch_talk(conf, client):
    cols = 'channel', 'user', 'timestamp', 'text'
    df = pd.DataFrame(index=[], columns=cols)

    for i in range(0, 11):
        channel_id = conf['channel']['ch{}'.format(i)]
        response = client.conversations_history(channel=channel_id)
        messages = response.data['messages']

        for message in messages:
            record = pd.Series([channel_id,
                                message['user'],
                                message['ts'],
                                message['text']],
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
