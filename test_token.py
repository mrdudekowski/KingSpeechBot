#!/usr/bin/env python3
"""
Test bot token
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get token
token = os.getenv("TELEGRAM_BOT_TOKEN")
print(f"Token found: {'Yes' if token else 'No'}")
if token:
    print(f"Token starts with: {token[:10]}...")
    print(f"Token length: {len(token)}")
else:
    print("No token found in .env file")
    
# Check if .env file exists
if os.path.exists('.env'):
    print(".env file exists")
    with open('.env', 'r') as f:
        content = f.read()
        print("Content:")
        print(content)
else:
    print(".env file not found")
    print("Creating .env file with test token...")
    with open('.env', 'w') as f:
        f.write("TELEGRAM_BOT_TOKEN=7719450947:AAGba3EoAW6d7ch7-gnri2NHmZBanqSs4gs\n")
        f.write("SPREADSHEET_ID=YOUR_ACTUAL_SHEETS_ID\n")
        f.write("SHEET_NAME=KingSpeechLeads\n")
        f.write("MANAGER_CHAT_ID=0\n")
    print(".env file created")
