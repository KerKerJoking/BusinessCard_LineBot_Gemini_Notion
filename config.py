import os
from dotenv import load_dotenv, set_key

# 加载 .env 文件
dotenv_path = '.env'
load_dotenv(dotenv_path)

def get_env_var(var_name, prompt):
    value = os.getenv(var_name)
    if value is None:
        value = input(f"{prompt}: ")
        set_key(dotenv_path, var_name, value)
    return value

GOOGLE_API_KEY = get_env_var('GOOGLE_API_KEY', 'Enter your Google API Key')
LINE_ACCESS_TOKEN = get_env_var('LINE_ACCESS_TOKEN', 'Enter your LINE Access Token')
LINE_SECRET = get_env_var('LINE_SECRET', 'Enter your LINE Secret')
NOTION_API = get_env_var('NOTION_API', 'Enter your Notion API')
NOTION_DB = get_env_var('NOTION_DB', 'Enter your Notion Database ID')