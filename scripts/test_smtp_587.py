#!/usr/bin/env python3
"""
Test SMTP with port 587 (STARTTLS)
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = "smtp.turkticaret.net"
SMTP_PORT = 587
SMTP_USER = "confirmation@meetdelux.com"
SMTP_PASSWORD = "Kazanak11."
FROM_EMAIL = "confirmation@meetdelux.com"
TO_EMAIL = "info@meetdelux.com"

print("="*60)
print("📧 Testing Port 587 (STARTTLS)")
print("="*60)
print(f"Host: {SMTP_HOST}")
print(f"Port: {SMTP_PORT}")
print(f"User: {SMTP_USER}")
print(f"From: {FROM_EMAIL}")
print(f"To: {TO_EMAIL}")
print("="*60)

try:
    message = MIMEMultipart()
    message["Subject"] = "MeetDelux Email Test ✅"
    message["From"] = f"MeetDelux <{FROM_EMAIL}>"
    message["To"] = TO_EMAIL
    
    html = """
    <html>
      <body style="font-family: Arial; padding: 20px;">
        <h1 style="color: #667eea;">✅ Email Çalışıyor!</h1>
        <p>Port 587 (STARTTLS) ile başarıyla gönderildi!</p>
      </body>
    </html>
    """
    message.attach(MIMEText(html, "html"))
    
    print("\n🔄 Connecting to SMTP server...")
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
    server.set_debuglevel(1)  # Show debug info
    
    print("\n🔐 Starting TLS...")
    context = ssl.create_default_context()
    server.starttls(context=context)
    
    print("\n🔑 Logging in...")
    server.login(SMTP_USER, SMTP_PASSWORD)
    
    print("\n📨 Sending email...")
    server.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
    
    print("\n✅ Closing connection...")
    server.quit()
    
    print("\n" + "="*60)
    print("✅ EMAIL SENT SUCCESSFULLY!")
    print("="*60)
    print(f"📧 Check: {TO_EMAIL}")
    print("="*60)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
