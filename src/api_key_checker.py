#!/usr/bin/env python3
"""
Comprehensive API Key Checker for Gemini AI
Tests various aspects of the API key functionality
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")

def print_status(status, message):
    """Print status with emoji"""
    emoji = "✅" if status else "❌"
    print(f"{emoji} {message}")

def check_api_key_exists():
    """Check if API key is loaded from environment"""
    print_header("1. API KEY EXISTENCE CHECK")
    
    if not API_KEY:
        print_status(False, "No GEMINI_API_KEY found in environment variables")
        return False
    
    if len(API_KEY) < 10:
        print_status(False, f"API key seems too short: {len(API_KEY)} characters")
        return False
    
    # Mask API key for security
    masked_key = API_KEY[:10] + "*" * (len(API_KEY) - 20) + API_KEY[-10:]
    print_status(True, f"API key loaded: {masked_key}")
    print_status(True, f"API key length: {len(API_KEY)} characters")
    return True

def check_api_connection():
    """Check if API key can authenticate"""
    print_header("2. API CONNECTION CHECK")
    
    try:
        genai.configure(api_key=API_KEY)
        print_status(True, "API configured successfully")
        return True
    except Exception as e:
        print_status(False, f"Failed to configure API: {str(e)}")
        return False

def list_available_models():
    """List all available models"""
    print_header("3. AVAILABLE MODELS CHECK")
    
    try:
        models = list(genai.list_models())
        print_status(True, f"Successfully retrieved {len(models)} models")
        
        # Show models that support text generation
        text_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                text_models.append(model.name)
        
        print(f"\n📝 Text Generation Models ({len(text_models)}):")
        for model in text_models[:10]:  # Show first 10
            print(f"   • {model}")
        
        if len(text_models) > 10:
            print(f"   ... and {len(text_models) - 10} more")
            
        return text_models
    except Exception as e:
        print_status(False, f"Failed to list models: {str(e)}")
        return []

def test_model_generation(model_name):
    """Test content generation with a specific model"""
    print(f"\n🧪 Testing model: {model_name}")
    
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello World' in exactly 2 words.")
        
        print_status(True, f"Model {model_name} working")
        print(f"   Response: {response.text.strip()}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print_status(False, f"Quota exceeded for {model_name}")
            return "quota_exceeded"
        elif "404" in error_msg:
            print_status(False, f"Model {model_name} not found")
            return False
        else:
            print_status(False, f"Error with {model_name}: {error_msg[:100]}...")
            return False

def test_multiple_models(available_models):
    """Test multiple models to find working ones"""
    print_header("4. MODEL FUNCTIONALITY TEST")
    
    # Priority order: try most reliable models first
    priority_models = [
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro-latest", 
        "models/gemini-1.5-pro",
        "models/gemini-2.0-flash",
        "models/gemini-pro-latest"
    ]
    
    working_models = []
    quota_exceeded_models = []
    
    # Test priority models first
    for model in priority_models:
        if model in available_models:
            result = test_model_generation(model)
            if result is True:
                working_models.append(model)
            elif result == "quota_exceeded":
                quota_exceeded_models.append(model)
    
    return working_models, quota_exceeded_models

def check_quota_status():
    """Check quota status by attempting a minimal request"""
    print_header("5. QUOTA STATUS CHECK")
    
    try:
        # Try with the most lightweight model
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content("Hi", 
                                        generation_config=genai.types.GenerationConfig(
                                            max_output_tokens=1
                                        ))
        print_status(True, "Quota available - API call successful")
        return True
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            print_status(False, "Quota exceeded - Free tier limits reached")
            print("💡 Solutions:")
            print("   • Wait for quota reset (usually 24 hours)")
            print("   • Upgrade to paid plan")
            print("   • Use different Google account")
            return False
        else:
            print_status(False, f"Unknown quota error: {error_msg[:100]}...")
            return False

def generate_report(working_models, quota_exceeded_models):
    """Generate final report"""
    print_header("🔍 FINAL REPORT")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Report generated: {timestamp}")
    
    if working_models:
        print_status(True, "API KEY IS WORKING! ✨")
        print(f"🟢 Working models: {len(working_models)}")
        for model in working_models:
            print(f"   ✓ {model}")
    elif quota_exceeded_models:
        print_status(False, "API KEY VALID BUT QUOTA EXCEEDED")
        print(f"🟡 Quota-limited models: {len(quota_exceeded_models)}")
        for model in quota_exceeded_models:
            print(f"   ⚠️ {model}")
        print("\n💡 Your API key is valid but you've hit the free tier limits.")
    else:
        print_status(False, "API KEY NOT WORKING")
        print("🔴 No working models found")
    
    print(f"\n📊 Summary:")
    print(f"   • API Key: {'Valid' if API_KEY else 'Missing'}")
    print(f"   • Working Models: {len(working_models) if working_models else 0}")
    print(f"   • Quota Issues: {len(quota_exceeded_models) if quota_exceeded_models else 0}")

def main():
    """Main function to run all checks"""
    print_header("🤖 GEMINI API KEY CHECKER")
    print("This tool will comprehensively test your Gemini API key...")
    
    # Step 1: Check if API key exists
    if not check_api_key_exists():
        print("\n❌ Cannot proceed without API key. Please check your .env file.")
        return
    
    # Step 2: Check API connection
    if not check_api_connection():
        print("\n❌ Cannot connect to API. Please check your API key.")
        return
    
    # Step 3: List available models
    available_models = list_available_models()
    if not available_models:
        print("\n❌ Cannot retrieve models. API key might be invalid.")
        return
    
    # Step 4: Test model functionality
    working_models, quota_exceeded_models = test_multiple_models(available_models)
    
    # Step 5: Check quota if no models worked
    if not working_models and not quota_exceeded_models:
        check_quota_status()
    
    # Step 6: Generate final report
    generate_report(working_models, quota_exceeded_models)

if __name__ == "__main__":
    main()