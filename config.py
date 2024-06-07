import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

GOOGLE_API_KEY = config['GOOGLE_API_KEY']
LINE_ACCESS_TOKEN = config['LINE_ACCESS_TOKEN']
LINE_SECRET = config['LINE_SECRET']
NOTION_API = config['NOTION_API']
NOTION_DB = config['NOTION_DB']