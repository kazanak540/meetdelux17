import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

def test_smtp():
    """Test SMTP connection and send test email"""
    
    smtp_configs = [
        # Try turkticaret.net configurations
        {"host": "smtp.turkticaret.net", "port": 587, "tls": True},
        {"host": "smtp.turkticaret.net", "port": 465, "ssl": True},
    ]
    
    smtp_user = os.environ.get('SMTP_USER', 'confirmation@meetdelux.com')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    
    print(f"Testing SMTP with user: {smtp_user}")
    print("=" * 50)
    
    for config in smtp_configs:
        try:
            print(f"\nTrying {config['host']}:{config['port']} (TLS: {config.get('tls', False)}, SSL: {config.get('ssl', False)})")
            
            if config.get('ssl'):
                import smtplib
                server = smtplib.SMTP_SSL(config['host'], config['port'], timeout=10)
            else:
                server = smtplib.SMTP(config['host'], config['port'], timeout=10)
                if config.get('tls'):
                    server.starttls()
            
            server.login(smtp_user, smtp_password)
            print(f"✅ SUCCESS! Connected to {config['host']}:{config['port']}")
            
            # Send test email
            msg = MIMEMultipart()
            msg['From'] = smtp_user
            msg['To'] = smtp_user  # Send to self
            msg['Subject'] = "MeetDelux SMTP Test - Başarılı!"
            
            body = """
            <html>
            <body>
                <h2>SMTP Test Başarılı!</h2>
                <p>MeetDelux email servisi düzgün çalışıyor.</p>
                <p>Kullanılan sunucu: {host}:{port}</p>
            </body>
            </html>
            """.format(host=config['host'], port=config['port'])
            
            msg.attach(MIMEText(body, 'html'))
            
            server.send_message(msg)
            print(f"✅ Test email gönderildi: {smtp_user}")
            
            server.quit()
            return True
            
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
            continue
    
    print("\n" + "=" * 50)
    print("❌ Tüm SMTP yapılandırmaları başarısız oldu.")
    print("\nLütfen hosting sağlayıcınızdan SMTP bilgilerini kontrol edin:")
    print("- SMTP sunucu adresi")
    print("- Port (587 veya 465)")
    print("- TLS/SSL ayarları")
    return False

if __name__ == "__main__":
    test_smtp()
