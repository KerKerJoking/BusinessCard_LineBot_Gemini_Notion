import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

GOOGLE_API_KEY = config['GOOGLE_API_KEY']
line_access_token = config['line_access_token']
line_secret = config['line_secret']
Notion_api = config['Notion_api']
Notion_DB = config['Notion_DB']