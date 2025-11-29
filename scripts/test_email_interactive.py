#!/usr/bin/env python3
"""
Interactive email test - Manuel şifre girişi
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass

print("="*60)
print("📧 MeetDelux Email Test - Interactive Mode")
print("="*60)

# SMTP settings from hosting
SMTP_HOST = "smtp.turkticaret.net"
SMTP_PORT = 465  # SSL Port
FROM_EMAIL = "confirmation@meetdelux.com"

print(f"\nSMTP Host: {SMTP_HOST}")
print(f"Port: {SMTP_PORT} (SSL)")
print(f"From: {FROM_EMAIL}")
print("="*60)

# Get credentials
print("\n🔐 Lütfen email bilgilerini girin:")
username = input(f"Username [{FROM_EMAIL}]: ").strip() or FROM_EMAIL
password = getpass.getpass("Password: ")

if not password:
    print("❌ Şifre boş olamaz!")
    exit(1)

# Test email
to_email = input(f"\nTest email adresi [info@meetdelux.com]: ").strip() or "info@meetdelux.com"

print(f"\n🚀 Sending test email...")
print(f"   From: {FROM_EMAIL}")
print(f"   To: {to_email}")
print(f"   Via: {SMTP_HOST}:{SMTP_PORT}")

try:
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = "MeetDelux Email Test ✅"
    message["From"] = f"MeetDelux <{FROM_EMAIL}>"
    message["To"] = to_email

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; padding: 30px; background: #f9fafb;">
        <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
          <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 32px;">✅ Email Çalışıyor!</h1>
          </div>
          
          <div style="padding: 40px;">
            <h2 style="color: #374151; margin-top: 0;">Merhaba!</h2>
            <p style="color: #6b7280; line-height: 1.8; font-size: 16px;">
              Bu <strong>MeetDelux</strong> platformundan gönderilen bir test emailidir.
            </p>
            
            <div style="background: #f0fdf4; border-left: 4px solid #10b981; padding: 20px; margin: 30px 0; border-radius: 4px;">
              <p style="color: #065f46; margin: 0; font-weight: bold; font-size: 18px;">
                🎉 Email sisteminiz başarıyla yapılandırıldı!
              </p>
            </div>
            
            <div style="background: #f9fafb; padding: 20px; border-radius: 8px; margin: 20px 0;">
              <h3 style="color: #374151; margin-top: 0; font-size: 16px;">📊 Sistem Bilgileri:</h3>
              <table style="width: 100%; color: #6b7280; font-size: 14px;">
                <tr>
                  <td style="padding: 8px 0;"><strong>SMTP Server:</strong></td>
                  <td style="padding: 8px 0;">{SMTP_HOST}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0;"><strong>Port:</strong></td>
                  <td style="padding: 8px 0;">{SMTP_PORT} (SSL)</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0;"><strong>From:</strong></td>
                  <td style="padding: 8px 0;">{FROM_EMAIL}</td>
                </tr>
                <tr>
                  <td style="padding: 8px 0;"><strong>Test Zamanı:</strong></td>
                  <td style="padding: 8px 0;">{__import__('datetime').datetime.now().strftime("%d.%m.%Y %H:%M:%S")}</td>
                </tr>
              </table>
            </div>
            
            <p style="color: #6b7280; line-height: 1.8; font-size: 16px;">
              Artık rezervasyon onayları, hatırlatmalar ve diğer sistem bildirimleri otomatik olarak gönderilecek. ✉️
            </p>
            
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
              <p style="color: #9ca3af; font-size: 14px; text-align: center; margin: 0;">
                Bu email <strong>MeetDelux</strong> tarafından gönderilmiştir.
              </p>
              <p style="color: #9ca3af; font-size: 14px; text-align: center; margin: 10px 0 0 0;">
                <a href="https://meetdelux.com" style="color: #667eea; text-decoration: none;">www.meetdelux.com</a>
              </p>
            </div>
          </div>
        </div>
      </body>
    </html>
    """
    
    message.attach(MIMEText(html, "html"))

    # Create SSL context
    context = ssl.create_default_context()

    # Connect and send
    print("   🔐 Connecting...")
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=15) as server:
        print("   ✅ Connected")
        
        print("   🔑 Authenticating...")
        server.login(username, password)
        print("   ✅ Authentication successful")
        
        print("   📨 Sending email...")
        server.sendmail(FROM_EMAIL, to_email, message.as_string())
        print("   ✅ Email sent!")

    print("\n" + "="*60)
    print("✅ EMAIL TEST SUCCESSFUL!")
    print("="*60)
    print(f"📧 Email sent to: {to_email}")
    print(f"📮 Check your inbox (and spam folder)")
    print("\n💾 Save this password in .env file:")
    print(f"   SMTP_PASSWORD={password}")
    print("="*60)

except smtplib.SMTPAuthenticationError as e:
    print("\n" + "="*60)
    print("❌ AUTHENTICATION FAILED")
    print("="*60)
    print(f"Error: {e}")
    print("\n⚠️ Olası sebepler:")
    print("1. Şifre yanlış")
    print("2. Username yanlış (tam email adresi olmalı)")
    print("3. SMTP hesapta aktif değil")
    print("\n💡 Çözüm önerileri:")
    print("- Hosting panelinden şifreyi kontrol edin")
    print("- Şifreyi basit bir şeyle değiştirip test edin")
    print("- info@meetdelux.com hesabını deneyin")
    print("="*60)

except Exception as e:
    print("\n" + "="*60)
    print("❌ CONNECTION ERROR")
    print("="*60)
    print(f"Error: {e}")
    print("\n⚠️ Olası sebepler:")
    print("1. SMTP server'a erişilemiyor")
    print("2. Port engellenmiş")
    print("3. SSL sertifikası sorunu")
    print("="*60)
