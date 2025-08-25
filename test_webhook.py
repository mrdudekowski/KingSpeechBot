#!/usr/bin/env python3
"""
Test script for KingSpeech Bot webhook
"""

import requests
import json
import os
from datetime import datetime

def test_webhook():
    """Test the webhook endpoint"""
    
    # Webhook configuration
    webhook_url = "http://localhost:5000/webhook/lead"
    secret_key = os.getenv('WEBHOOK_SECRET', 'your-secret-key-here')
    
    # Test data
    test_data = {
        "name": "Тестовый Пользователь",
        "phone": "+7 (999) 123-45-67",
        "level": "Начинающий",
        "goals": "Общий язык",
        "format": "Индивидуальный",
        "expectations": "Разнообразие слов и выражений",
        "schedule": "На следующей неделе",
        "timestamp": datetime.now().isoformat(),
        "source": "test_script"
    }
    
    # Headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {secret_key}"
    }
    
    try:
        print("🧪 Testing webhook...")
        print(f"URL: {webhook_url}")
        print(f"Data: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
        
        # Send request
        response = requests.post(
            webhook_url,
            headers=headers,
            json=test_data,
            timeout=10
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure webhook server is running on localhost:5000")
    except requests.exceptions.Timeout:
        print("❌ Timeout: Request took too long")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def test_health_endpoint():
    """Test the health check endpoint"""
    
    health_url = "http://localhost:5000/webhook/health"
    
    try:
        print("\n🏥 Testing health endpoint...")
        response = requests.get(health_url, timeout=5)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Health: {result}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Health check failed: {e}")

if __name__ == "__main__":
    print("🚀 KingSpeech Bot Webhook Test")
    print("=" * 40)
    
    # Test health endpoint first
    test_health_endpoint()
    
    # Test webhook
    test_webhook()
    
    print("\n" + "=" * 40)
    print("✨ Test completed!")
