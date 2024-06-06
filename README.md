# NameCard_Bot
The NameCard_Bot is a Python-based application that integrates with LINE Messaging API and Google Gemini API to extract information from business card images.
NameCard_Bot: A LINE Bot for Extracting and Storing Business Card Information
Overview
The NameCard_Bot is a Python-based application that integrates with LINE Messaging API and Google Gemini API to extract information from business card images. The extracted information is then stored in a Notion database. This bot handles both text and image messages, responding to text messages directly and processing image messages to extract structured data.

Key Features
LINE Messaging API Integration: The bot uses LINE Messaging API to receive and respond to messages.
Google Gemini API Integration: It leverages Google Gemini's capabilities to extract information from business card images.
Notion API Integration: The extracted information is stored in a Notion database for easy access and management.
Components
1. main.py
This is the main entry point of the application. It sets up the Flask server and defines the route for handling POST requests from LINE.

2. config.py
This file contains the configuration and API keys necessary for connecting to the Google Gemini API, LINE Messaging API, and Notion API. Make sure to exclude this file from your version control system to keep your API keys secure.

3. config.json
A JSON file used to store sensitive configuration details such as API keys. This file should also be excluded from version control.

4. image Directory
A directory to store image files temporarily during processing.

Workflow
Receiving Messages: The bot receives messages via the LINE Messaging API. Depending on the message type (text or image), it processes the message accordingly.
Processing Text Messages: If the message is a text message, the bot uses the Google Gemini API to generate a response and sends it back to the user.
Processing Image Messages: If the message is an image, the bot saves the image locally, sends it to the Google Gemini API for processing, extracts the information, and stores the extracted information in a Notion database.
Storing Data in Notion: The extracted information is formatted and sent to the Notion API to create a new entry in the specified database.
Usage
Setup: Ensure you have all the necessary API keys and configure them in config.json.
Run the Application: Start the Flask server by running the main.py script.
Interact via LINE: Add the bot to your LINE contacts and start sending messages. The bot will respond to text messages and process image messages to extract and store business card information.
Example
sh
複製程式碼
# Navigate to your project directory
cd path/to/NameCard_Bot

# Run the application
python main.py
You can now interact with your bot via LINE, and it will handle text and image messages accordingly.

This explanation should provide a clear understanding of what your NameCard_Bot does and how it works. Let me know if you need further details or modifications!
