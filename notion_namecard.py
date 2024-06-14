import requests
import logging

def Notion_Write(namecard_json, namecard_id, key, db):
    try:
        NOTION_API_URL = 'https://api.notion.com/v1/pages'
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        new_page = {
            "parent": { "database_id": db },
            "properties": {
                "UUID":{
                    "title":[
                        {
                            "text": {
                                "content": namecard_id
                            }
                        }
                    ]
                },
                "Name": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Name", "N/A")
                            }
                        }
                    ]
                },
                "Title": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Title", "N/A")
                            }
                        }
                    ]
                },
                "Address": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Address", "N/A")
                            }
                        }
                    ]
                },
                "Email": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Email", "N/A")
                            }
                        }
                    ]
                },
                "Phone": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Phone", "N/A")
                            }
                        }
                    ]
                },
                "Company": {
                    "rich_text": [
                        {
                            "text": {
                                "content": namecard_json.get("Company", "N/A")
                            }
                        }
                    ]
                }
            }
        }
        response = requests.post(NOTION_API_URL, headers=headers, json=new_page)
        if response.status_code == 200:
            logging.info("Successfully added to Notion DB")
        else:
            logging.error("Failed to add to Notion DB: %s", response.status_code)
            logging.error(response.text)
    except Exception as e:
        logging.error("Notion error: %s", e)

def Notion_Search(query, key, db):
    try:
        NOTION_SEARCH_URL = 'https://api.notion.com/v1/databases/{}/query'.format(db)
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        payload = {
            "filter": {
                "or": [
                    {
                        "property": "UUID",
                        "title": {
                            "contains": query
                        }
                    },
                    {
                        "property": "Name",
                        "rich_text": {
                            "contains": query
                        }
                    },
                    {
                        "property": "Title",
                        "rich_text": {
                            "contains": query
                        }
                    },
                    {
                        "property": "Address",
                        "rich_text": {
                            "contains": query
                        }
                    },
                    {
                        "property": "Email",
                        "rich_text": {
                            "contains": query
                        }
                    },
                    {
                        "property": "Phone",
                        "rich_text": {
                            "contains": query
                        }
                    },
                    {
                        "property": "Company",
                        "rich_text": {
                            "contains": query
                        }
                    }
                ]
            }
        }

        response = requests.post(NOTION_SEARCH_URL, headers=headers, json=payload)
        if response.status_code == 200:
            logging.info("Search successful")
            results = response.json().get('results', [])
            return results
        else:
            logging.error("Failed to search in Notion DB: %s", response.status_code)
            logging.error(response.text)
            return []
    except Exception as e:
        logging.error("Notion search error: %s", e)
        return []

def Notion_Delete(namecard_id, key, db):
    try:
        # 搜尋指定的UUID
        results = Notion_Search(namecard_id, key, db)
        if not results:
            logging.error("No entry found with UUID: %s", namecard_id)
            return False
        
        # 獲取頁面ID進行刪除
        page_id = results[0]['id']
        delete_url = f"https://api.notion.com/v1/blocks/{page_id}"
        headers = {
            "Authorization": f"Bearer {key}",
            "Notion-Version": "2022-06-28"
        }

        response = requests.delete(delete_url, headers=headers)
        if response.status_code == 200:
            logging.info("Successfully deleted entry with UUID: %s", namecard_id)
            return True
        else:
            logging.error("Failed to delete entry: %s", response.status_code)
            logging.error(response.text)
            return False
    except Exception as e:
        logging.error("Notion delete error: %s", e)
        return False

def Notion_Edit(namecard_id, field, payload, key, db):
    try:
        # 搜尋指定的UUID
        results = Notion_Search(namecard_id, key, db)
        if not results:
            logging.error("No entry found with UUID: %s", namecard_id)
            return False
        
        # 獲取頁面ID進行編輯
        page_id = results[0]['id']
        update_url = f"https://api.notion.com/v1/pages/{page_id}"
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # 建立更新的資料結構
        properties = {
            field: {
                "rich_text": [
                    {
                        "text": {
                            "content": payload
                        }
                    }
                ]
            }
        }

        data = {
            "properties": properties
        }

        response = requests.patch(update_url, headers=headers, json=data)
        if response.status_code == 200:
            logging.info("Successfully updated entry with UUID: %s", namecard_id)
            return True
        else:
            logging.error("Failed to update entry: %s", response.status_code)
            logging.error(response.text)
            return False
    except Exception as e:
        logging.error("Notion edit error: %s", e)
        return False

def Format_Notion_Results(results):
    formatted_results = []
    for result in results:
        properties = result['properties']
        formatted_result = (
            f"UUID: {properties['UUID']['title'][0]['text']['content']}\n"
            f"Name: {properties['Name']['rich_text'][0]['text']['content']}\n"
            f"Title: {properties['Title']['rich_text'][0]['text']['content']}\n"
            f"Address: {properties['Address']['rich_text'][0]['text']['content']}\n"
            f"Email: {properties['Email']['rich_text'][0]['text']['content']}\n"
            f"Phone: {properties['Phone']['rich_text'][0]['text']['content']}\n"
            f"Company: {properties['Company']['rich_text'][0]['text']['content']}"
        )
        formatted_results.append(formatted_result)
    return "\n\n".join(formatted_results)