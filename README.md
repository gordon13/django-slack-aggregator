# django-slack-aggregator

Django app used to aggregate slack messages by tags

# Installation
virtualenv env

env\scripts\pip.exe install -r requirements.txt

Note: It will also need a config file called config.cfg with the following format:
[connection_settings]
token: <slack API token>