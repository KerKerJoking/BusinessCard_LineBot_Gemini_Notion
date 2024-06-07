import requests
import logging

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