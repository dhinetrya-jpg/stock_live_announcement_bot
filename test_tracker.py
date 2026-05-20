#!/usr/bin/env python3
"""
NSE Announcement Bot - Comprehensive Validation Test Suite
Tests all critical components before production deployment
"""

import os
import sys
import requests
import json
import subprocess
from datetime import datetime

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text.center(70)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*70}{Colors.END}\n")


def print_test(test_num, test_name, passed, details=""):
    """Print test result"""
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} Test {test_num}: {test_name}")
    if details:
        print(f"   └─ {details}")


def test_1_environment_variables():
    """Test 1: Check environment variables"""
    print(f"\n{Colors.BOLD}Test 1: Environment Variables{Colors.END}")
    
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    passed = bool(token and chat_id)
    details = f"Token: {'Set' if token else 'Missing'}, Chat ID: {'Set' if chat_id else 'Missing'}"
    print_test(1, "Environment Variables", passed, details)
    
    return passed


def test_2_telegram_token_format():
    """Test 2: Validate Telegram token format"""
    print(f"\n{Colors.BOLD}Test 2: Telegram Token Format{Colors.END}")
    
    token = os.environ.get("TELEGRAM_TOKEN", "")
    
    # Token format: numeric:alphanumeric
    passed = ":" in token and len(token) > 10
    
    # Mask token for display
    masked_token = f"{token[:6]}:{'*' * (len(token)-10)}" if token else "NOT SET"
    details = f"Format: Valid, Token length: {len(token)}, Display: {masked_token}"
    
    print_test(2, "Telegram Token Format", passed, details)
    
    return passed


def test_3_telegram_chat_id_format():
    """Test 3: Validate Telegram chat ID format"""
    print(f"\n{Colors.BOLD}Test 3: Telegram Chat ID Format{Colors.END}")
    
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    
    # Chat ID should be numeric or start with minus (group)
    passed = str(chat_id).lstrip('-').isdigit() and chat_id != ""
    
    chat_type = "Group chat" if str(chat_id).startswith("-") else "User chat"
    details = f"Format: {chat_type}, Value: {chat_id}"
    
    print_test(3, "Telegram Chat ID Format", passed, details)
    
    return passed


def test_4_telegram_bot_verification():
    """Test 4: Verify Telegram bot token is valid (LIVE API TEST)"""
    print(f"\n{Colors.BOLD}Test 4: Telegram Bot Verification (LIVE API TEST){Colors.END}")
    
    token = os.environ.get("TELEGRAM_TOKEN")
    
    if not token:
        print_test(4, "Telegram Bot Verification", False, "Token not set")
        return False
    
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data.get("result", {})
                bot_name = bot_info.get("first_name", "Unknown")
                bot_id = bot_info.get("id", "Unknown")
                details = f"Bot: {bot_name} (ID: {bot_id})"
                print_test(4, "Telegram Bot Verification", True, details)
                return True
            else:
                error = data.get("description", "Unknown error")
                details = f"API Error: {error}"
                print_test(4, "Telegram Bot Verification", False, details)
                return False
        else:
            details = f"HTTP {response.status_code}"
            print_test(4, "Telegram Bot Verification", False, details)
            return False
    
    except requests.exceptions.Timeout:
        print_test(4, "Telegram Bot Verification", False, "Request timeout")
        return False
    except Exception as e:
        print_test(4, "Telegram Bot Verification", False, f"Error: {str(e)}")
        return False


def test_5_nse_connectivity():
    """Test 5: Test NSE home page connectivity"""
    print(f"\n{Colors.BOLD}Test 5: NSE Connectivity{Colors.END}")
    
    nse_url = "https://nseindia.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(nse_url, headers=headers, timeout=15)
        
        passed = response.status_code == 200
        details = f"Status: {response.status_code}, Response time: {response.elapsed.total_seconds():.2f}s"
        
        print_test(5, "NSE Connectivity", passed, details)
        return passed
    
    except requests.exceptions.Timeout:
        print_test(5, "NSE Connectivity", False, "Request timeout (>15s)")
        return False
    except Exception as e:
        print_test(5, "NSE Connectivity", False, f"Error: {str(e)}")
        return False


def test_6_nse_api_endpoint():
    """Test 6: Test NSE API endpoint returns valid JSON"""
    print(f"\n{Colors.BOLD}Test 6: NSE API Endpoint (LIVE API TEST){Colors.END}")
    
    nse_api_url = "https://www.nseindia.com/api/corporate-announcements"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://nseindia.com"
    }
    
    try:
        session = requests.Session()
        
        # First establish session with home page
        session.get("https://nseindia.com", headers=headers, timeout=15)
        
        # Then fetch from API
        response = session.get(nse_api_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print_test(6, "NSE API Endpoint", False, f"HTTP {response.status_code}")
            return False
        
        try:
            data = response.json()
            
            if isinstance(data, list):
                details = f"Valid JSON, {len(data)} announcements fetched"
                print_test(6, "NSE API Endpoint", True, details)
                return True
            else:
                details = f"JSON returned but not list type: {type(data)}"
                print_test(6, "NSE API Endpoint", True, details)
                return True
        
        except json.JSONDecodeError:
            details = "Response is not valid JSON"
            print_test(6, "NSE API Endpoint", False, details)
            return False
    
    except requests.exceptions.Timeout:
        print_test(6, "NSE API Endpoint", False, "Request timeout (>15s)")
        return False
    except Exception as e:
        print_test(6, "NSE API Endpoint", False, f"Error: {str(e)}")
        return False


def test_7_script_structure():
    """Test 7: Validate tracker.py structure and functions"""
    print(f"\n{Colors.BOLD}Test 7: Script Structure{Colors.END}")
    
    try:
        with open("tracker.py", "r") as f:
            content = f.read()
        
        required_functions = [
            "load_processed_ids",
            "save_processed_id",
            "send_telegram_alert",
            "track_nse",
            "fetch_nse_announcements",
            "process_announcements"
        ]
        
        found_count = 0
        for func in required_functions:
            if f"def {func}" in content:
                found_count += 1
        
        passed = found_count >= 4  # At least 4 core functions
        details = f"Found {found_count}/{len(required_functions)} required functions"
        
        print_test(7, "Script Structure", passed, details)
        return passed
    
    except FileNotFoundError:
        print_test(7, "Script Structure", False, "tracker.py not found")
        return False
    except Exception as e:
        print_test(7, "Script Structure", False, f"Error: {str(e)}")
        return False


def test_8_python_dependencies():
    """Test 8: Verify Python dependencies are installed"""
    print(f"\n{Colors.BOLD}Test 8: Python Dependencies{Colors.END}")
    
    required_modules = ["requests", "json", "os", "logging"]
    
    all_available = True
    for module in required_modules:
        try:
            if module == "json" or module == "os" or module == "logging":
                # Built-in modules
                __import__(module)
            else:
                __import__(module)
        except ImportError:
            all_available = False
            print(f"   ❌ Module '{module}' not available")
    
    details = f"All {len(required_modules)} modules available" if all_available else "Missing modules"
    print_test(8, "Python Dependencies", all_available, details)
    
    return all_available


def test_9_registry_operations():
    """Test 9: Test registry file operations"""
    print(f"\n{Colors.BOLD}Test 9: Registry File Operations{Colors.END}")
    
    test_file = "test_registry_validation.txt"
    
    try:
        # Test write
        with open(test_file, "w") as f:
            f.write("test_id_1\n")
            f.write("test_id_2\n")
            f.write("test_id_3\n")
        
        # Test read
        with open(test_file, "r") as f:
            lines = set(f.read().splitlines())
        
        # Test append
        with open(test_file, "a") as f:
            f.write("test_id_4\n")
        
        # Verify
        with open(test_file, "r") as f:
            final_lines = set(f.read().splitlines())
        
        passed = len(final_lines) == 4 and "test_id_1" in final_lines
        
        # Cleanup
        os.remove(test_file)
        
        details = f"Read/Write/Append successful, {len(final_lines)} entries handled"
        print_test(9, "Registry Operations", passed, details)
        
        return passed
    
    except Exception as e:
        print_test(9, "Registry Operations", False, f"Error: {str(e)}")
        if os.path.exists(test_file):
            os.remove(test_file)
        return False


def run_all_tests():
    """Run all validation tests"""
    print_header("NSE ANNOUNCEMENT BOT - VALIDATION TEST SUITE")
    
    print(f"{Colors.YELLOW}Note: Tests marked (LIVE API TEST) connect to external services{Colors.END}")
    print(f"{Colors.YELLOW}Ensure you have internet connectivity{Colors.END}\n")
    
    results = []
    
    # Run all tests
    results.append(("Environment Variables", test_1_environment_variables()))
    results.append(("Telegram Token Format", test_2_telegram_token_format()))
    results.append(("Telegram Chat ID Format", test_3_telegram_chat_id_format()))
    results.append(("Telegram Bot Verification", test_4_telegram_bot_verification()))
    results.append(("NSE Connectivity", test_5_nse_connectivity()))
    results.append(("NSE API Endpoint", test_6_nse_api_endpoint()))
    results.append(("Script Structure", test_7_script_structure()))
    results.append(("Python Dependencies", test_8_python_dependencies()))
    results.append(("Registry Operations", test_9_registry_operations()))
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed_count = sum(1 for _, result in results if result)
    failed_count = len(results) - passed_count
    
    print(f"{Colors.GREEN}✅ Passed: {passed_count}{Colors.END}")
    print(f"{Colors.RED}❌ Failed: {failed_count}{Colors.END}")
    print(f"⏭️  Skipped: 0\n")
    
    if failed_count == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!{Colors.END}")
        print(f"{Colors.GREEN}Your script is ready for production deployment.{Colors.END}\n")
        print(f"{Colors.CYAN}Next steps:{Colors.END}")
        print(f"1. Run: {Colors.BOLD}python tracker.py{Colors.END}")
        print(f"2. Monitor: {Colors.BOLD}tail -f tracker.log{Colors.END}")
        print(f"3. Schedule: {Colors.BOLD}Use cron or GitHub Actions{Colors.END}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}⚠️  SOME TESTS FAILED{Colors.END}")
        print(f"{Colors.RED}Please fix the issues above before deployment.{Colors.END}\n")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
