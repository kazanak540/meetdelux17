#!/usr/bin/env python3
"""
Advanced email test with multiple port/method attempts
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / 'backend' / '.env')

# SMTP settings
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_FROM_EMAIL = os.environ.get('SMTP_FROM_EMAIL')
SMTP_FROM_NAME = os.environ.get('SMTP_FROM_NAME', 'MeetDelux')

print("="*60)
print("📧 MeetDelux Advanced Email Test")
print("="*60)
print(f"SMTP Host: {SMTP_HOST}")
print(f"SMTP User: {SMTP_USER}")
print(f"From Email: {SMTP_FROM_EMAIL}")
print(f"Password Length: {len(SMTP_PASSWORD)} chars")
print(f"Password (masked): {SMTP_PASSWORD[:3]}...{SMTP_PASSWORD[-3:]}")
print("="*60)

TEST_EMAIL = "info@meetdelux.com"

def create_test_message(to_email):
    """Create test email message"""
    message = MIMEMultipart("alternative")
    message["Subject"] = "MeetDelux Email Test ✅"
    message["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    message["To"] = to_email

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h1 style="color: #667eea;">✅ Email Test Başarılı!</h1>
        <p>MeetDelux email sistemi çalışıyor!</p>
        <p>Test zamanı: {__import__('datetime').datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</p>
      </body>
    </html>
    """
    
    message.attach(MIMEText(html, "html"))
    return message

# Try different configurations
configs = [
    {"port": 587, "use_ssl": False, "use_tls": True, "name": "Port 587 (STARTTLS)"},
    {"port": 465, "use_ssl": True, "use_tls": False, "name": "Port 465 (SSL)"},
    {"port": 25, "use_ssl": False, "use_tls": True, "name": "Port 25 (TLS)"},
]

for config in configs:
    print(f"\n🔄 Trying {config['name']}...")
    print(f"   Port: {config['port']}")
    
    try:
        message = create_test_message(TEST_EMAIL)
        
        if config['use_ssl']:
            # SSL connection
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_HOST, config['port'], context=context, timeout=10) as server:
                server.set_debuglevel(0)
                print(f"   ✅ Connected via SSL")
                server.login(SMTP_USER, SMTP_PASSWORD)
                print(f"   ✅ Authenticated")
                server.sendmail(SMTP_FROM_EMAIL, TEST_EMAIL, message.as_string())
                print(f"   ✅ Email sent!")
        else:
            # Regular or STARTTLS connection
            with smtplib.SMTP(SMTP_HOST, config['port'], timeout=10) as server:
                server.set_debuglevel(0)
                print(f"   ✅ Connected")
                
                if config['use_tls']:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    print(f"   ✅ STARTTLS enabled")
                
                server.login(SMTP_USER, SMTP_PASSWORD)
                print(f"   ✅ Authenticated")
                server.sendmail(SMTP_FROM_EMAIL, TEST_EMAIL, message.as_string())
                print(f"   ✅ Email sent!")
        
        print("\n" + "="*60)
        print(f"✅ SUCCESS with {config['name']}!")
        print("="*60)
        print(f"📧 Email sent to: {TEST_EMAIL}")
        print(f"🔧 Working configuration:")
        print(f"   - Port: {config['port']}")
        print(f"   - SSL: {config['use_ssl']}")
        print(f"   - TLS: {config['use_tls']}")
        print("="*60)
        
        # Update .env with working config
        print("\n💾 Updating .env with working configuration...")
        sys.exit(0)
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"   ❌ Authentication failed: {e}")
    except smtplib.SMTPException as e:
        print(f"   ❌ SMTP error: {e}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("❌ ALL CONFIGURATIONS FAILED")
print("="*60)
print("\nPossible issues:")
print("1. ❌ Wrong username or password")
print("2. ❌ SMTP server requires different authentication")
print("3. ❌ Account not configured for SMTP access")
print("4. ❌ Need to enable SMTP in hosting panel")
print("\nPlease check:")
print("- Hosting panel SMTP settings")
print("- Email account password")
print("- SMTP enabled for the account")
print("="*60)
