## readme

- please put `params.ini` in ./utils/

### using venv

- `python3 -m venv .slackapi`
- `source .slackapi/bin/activate`
- `pip3 install --upgrade pip`
- `pip3 install -r requirements.txt`
- run `get_ch_talk.py (-c ini_category)` to get talklogs

## directry

```
slackapi
├── README.md
├── requirements.txt
│
├── get_ch_talk.py
├── get_userlist.py
│
├── export
│   └── (output files)
└── utils
    ├── (please put params.ini)
    └── sample.ini
```
