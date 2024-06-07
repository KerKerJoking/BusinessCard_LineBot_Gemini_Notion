import json
import PIL.Image
import google.generativeai as genai
import logging

def Gemini_Namecard(img_path,key):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        ImagePrompt = "Here is a business card, and you are a business card secretary. Please organize the following information into JSON for me. If something is unclear, fill it with N/A. Only the JSON is needed:\n\nName, Title, Address, Email, Phone, Company.\n\nThe format for the Phone content should be #886-0123-456-789,1234. Ignore ,1234 if there is no extension.\n\nFor the same information in different languages, please put them in the same field separated by commas."
        img = PIL.Image.open(img_path)
        logging.info("Image opened: %s", img_path)
        response = model.generate_content([ImagePrompt, img], stream=True)
        response.resolve()
        raw_response = response.text
        if raw_response.startswith("```json"):
            raw_response = raw_response[7:]
        if raw_response.endswith("```"):
            raw_response = raw_response[:-3]
        data = json.loads(raw_response)
        return data
    except Exception as e:
        logging.error("Gemini error: %s", e)
        return {"error": "Gemini got something wrong!"}
