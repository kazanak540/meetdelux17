#!/usr/bin/env python3
"""
Real email test with actual SMTP credentials
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
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
SMTP_FROM_EMAIL = os.environ.get('SMTP_FROM_EMAIL')
SMTP_FROM_NAME = os.environ.get('SMTP_FROM_NAME', 'MeetDelux')

print("="*60)
print("📧 MeetDelux Email Test")
print("="*60)
print(f"SMTP Host: {SMTP_HOST}")
print(f"SMTP Port: {SMTP_PORT}")
print(f"SMTP User: {SMTP_USER}")
print(f"From Email: {SMTP_FROM_EMAIL}")
print(f"From Name: {SMTP_FROM_NAME}")
print("="*60)

# Check if all settings are present
if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD]):
    print("❌ SMTP settings not configured properly!")
    print("Please check your .env file")
    sys.exit(1)

# Test email recipient
TEST_EMAIL = input("\n📮 Test email göndermek istediğiniz email adresi: ").strip()

if not TEST_EMAIL:
    TEST_EMAIL = "info@meetdelux.com"
    print(f"Varsayılan email kullanılıyor: {TEST_EMAIL}")

print(f"\n🚀 Sending test email to: {TEST_EMAIL}")
print("⏳ Please wait...")

try:
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "MeetDelux Email Test ✅"
    message["From"] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    message["To"] = TEST_EMAIL

    # Plain text version
    text = """
    Merhaba!
    
    Bu MeetDelux platformundan gönderilen bir test emailidir.
    
    Email sisteminiz başarıyla çalışıyor! ✅
    
    Test Detayları:
    - SMTP Host: {host}
    - Port: {port}
    - From: {from_email}
    
    İyi günler!
    MeetDelux Ekibi
    """.format(
        host=SMTP_HOST,
        port=SMTP_PORT,
        from_email=SMTP_FROM_EMAIL
    )

    # HTML version
    html = """
    <html>
      <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center;">
          <h1 style="color: white; margin: 0;">✅ Email Test Başarılı!</h1>
        </div>
        
        <div style="background: #f9fafb; padding: 30px; margin-top: 20px; border-radius: 10px;">
          <h2 style="color: #374151;">Merhaba!</h2>
          <p style="color: #6b7280; line-height: 1.6;">
            Bu <strong>MeetDelux</strong> platformundan gönderilen bir test emailidir.
          </p>
          <p style="color: #10b981; font-weight: bold; font-size: 18px;">
            🎉 Email sisteminiz başarıyla çalışıyor!
          </p>
          
          <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h3 style="color: #374151; margin-top: 0;">Test Detayları:</h3>
            <ul style="color: #6b7280; line-height: 2;">
              <li><strong>SMTP Host:</strong> {host}</li>
              <li><strong>Port:</strong> {port}</li>
              <li><strong>From:</strong> {from_email}</li>
              <li><strong>Gönderim Zamanı:</strong> {time}</li>
            </ul>
          </div>
          
          <p style="color: #6b7280; line-height: 1.6;">
            Artık rezervasyon onayları, hatırlatmalar ve diğer bildirimler otomatik olarak gönderilecek.
          </p>
        </div>
        
        <div style="text-align: center; margin-top: 30px; padding: 20px; color: #9ca3af; font-size: 14px;">
          <p>Bu email MeetDelux tarafından gönderilmiştir.</p>
          <p>
            <a href="https://meetdelux.com" style="color: #667eea; text-decoration: none;">www.meetdelux.com</a>
          </p>
        </div>
      </body>
    </html>
    """.format(
        host=SMTP_HOST,
        port=SMTP_PORT,
        from_email=SMTP_FROM_EMAIL,
        time=__import__('datetime').datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    )

    # Attach both versions
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # Create secure SSL context
    context = ssl.create_default_context()

    # Send email
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        print(f"🔐 Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print(f"✅ Login successful!")
        
        server.sendmail(SMTP_FROM_EMAIL, TEST_EMAIL, message.as_string())
        print(f"✅ Email sent successfully to {TEST_EMAIL}!")

    print("\n" + "="*60)
    print("✅ EMAIL TEST SUCCESSFUL!")
    print("="*60)
    print(f"📧 Check your inbox: {TEST_EMAIL}")
    print("📨 Don't forget to check SPAM folder if not in inbox")
    print("="*60)

except Exception as e:
    print("\n" + "="*60)
    print("❌ EMAIL TEST FAILED!")
    print("="*60)
    print(f"Error: {str(e)}")
    print("\nPossible issues:")
    print("1. Wrong SMTP credentials")
    print("2. SMTP server blocking connection")
    print("3. Firewall blocking port 465")
    print("4. Need to enable 'Less secure apps' in email settings")
    print("="*60)
    sys.exit(1)
