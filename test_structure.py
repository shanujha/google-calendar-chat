"""
Test script for calendar_chat.py
This script tests the basic structure and imports without requiring actual credentials.
"""

import sys
import os
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        import google.generativeai as genai
        from dotenv import load_dotenv
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_class_structure():
    """Test that classes can be defined (without initialization)"""
    print("\nTesting class structure...")
    try:
        # Read and parse the file
        with open('calendar_chat.py', 'r') as f:
            content = f.read()
        
        # Check for required classes
        required_classes = ['CalendarService', 'GeminiAgent', 'CalendarChatAgent']
        for cls in required_classes:
            if f"class {cls}" in content:
                print(f"✅ Found class: {cls}")
            else:
                print(f"❌ Missing class: {cls}")
                return False
        
        # Check for required methods
        required_methods = [
            'authenticate', 'list_events', 'create_event',
            'generate_response', 'parse_calendar_command',
            'process_query', 'start_chat'
        ]
        for method in required_methods:
            if f"def {method}" in content:
                print(f"✅ Found method: {method}")
            else:
                print(f"❌ Missing method: {method}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Class structure test failed: {e}")
        return False

def test_syntax():
    """Test Python syntax by compiling"""
    print("\nTesting Python syntax...")
    try:
        import py_compile
        py_compile.compile('calendar_chat.py', doraise=True)
        print("✅ Python syntax is valid")
        return True
    except py_compile.PyCompileError as e:
        print(f"❌ Syntax error: {e}")
        return False

def test_constants():
    """Test that required constants are defined"""
    print("\nTesting constants...")
    try:
        with open('calendar_chat.py', 'r') as f:
            content = f.read()
        
        if "SCOPES" in content and "calendar" in content:
            print("✅ SCOPES constant found and includes calendar")
            return True
        else:
            print("❌ SCOPES constant not properly defined")
            return False
    except Exception as e:
        print(f"❌ Constants test failed: {e}")
        return False

def test_documentation():
    """Test that required documentation files exist"""
    print("\nTesting documentation...")
    required_files = [
        'README.md',
        'requirements.txt',
        '.gitignore',
        '.env.example',
        'SETUP_CREDENTIALS.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("="*60)
    print("Running Calendar Chat Agent Tests")
    print("="*60 + "\n")
    
    tests = [
        test_imports,
        test_syntax,
        test_class_structure,
        test_constants,
        test_documentation
    ]
    
    results = []
    for test in tests:
        results.append(test())
        print()
    
    print("="*60)
    print("Test Summary")
    print("="*60)
    print(f"Total tests: {len(results)}")
    print(f"Passed: {sum(results)}")
    print(f"Failed: {len(results) - sum(results)}")
    
    if all(results):
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
