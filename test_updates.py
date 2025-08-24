#!/usr/bin/env python3
"""
Test bot updates
"""

import requests
import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import TELEGRAM_BOT_TOKEN

def get_updates():
    """Get updates from Telegram"""
    print("Getting updates from Telegram...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            updates = data['result']
            print(f"Found {len(updates)} updates")
            
            for i, update in enumerate(updates):
                print(f"\nUpdate {i+1}:")
                print(f"  Update ID: {update['update_id']}")
                
                if 'message' in update:
                    msg = update['message']
                    print(f"  Message from: {msg['from']['first_name']} (@{msg['from'].get('username', 'no_username')})")
                    print(f"  Chat ID: {msg['chat']['id']}")
                    print(f"  Text: {msg.get('text', 'no text')}")
                    print(f"  Date: {msg['date']}")
                    
                elif 'callback_query' in update:
                    cb = update['callback_query']
                    print(f"  Callback from: {cb['from']['first_name']}")
                    print(f"  Data: {cb['data']}")
                    
            return updates
        else:
            print(f"❌ Error: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error getting updates: {e}")
        return []

def send_message(chat_id, text):
    """Send message to specific chat"""
    print(f"Sending message to {chat_id}: {text}")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Message sent successfully!")
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Bot Updates ===")
    
    # Get current updates
    updates = get_updates()
    
    if updates:
        # Try to send message to the last chat
        last_update = updates[-1]
        if 'message' in last_update:
            chat_id = last_update['message']['chat']['id']
            send_message(chat_id, "Тестовое сообщение от API! 🎉")
    else:
        print("\nNo updates found. Send /start to your bot first!")
        print("Then run this script again to test.")
