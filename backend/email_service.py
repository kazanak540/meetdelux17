import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = os.environ.get('SMTP_HOST', 'smtp.turkticaret.net')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 465))
        self.smtp_use_ssl = os.environ.get('SMTP_USE_SSL', 'True').lower() == 'true'
        self.smtp_user = os.environ.get('SMTP_USER', 'confirmation@meetdelux.com')
        self.smtp_password = os.environ.get('SMTP_PASSWORD')
        self.from_email = os.environ.get('SMTP_FROM_EMAIL', 'confirmation@meetdelux.com')
        self.from_name = os.environ.get('SMTP_FROM_NAME', 'MeetDelux')
        self.app_url = os.environ.get('APP_URL', 'https://www.meetdelux.com')
        
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: Optional[str] = None):
        """Send an email using SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Bcc'] = self.from_email  # BCC to self for monitoring
            
            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(part1)
            
            part2 = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(part2)
            
            # Send email using SSL
            if self.smtp_use_ssl:
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                    server.send_message(msg)
                
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def send_welcome_email(self, user_email: str, user_name: str, verification_token: Optional[str] = None):
        """Send welcome email to new user"""
        subject = "MeetDelux'a Hoş Geldiniz! 🎉"
        
        verification_section = ""
        if verification_token:
            verification_link = f"{self.app_url}/verify-email?token={verification_token}"
            verification_section = f"""
            <div style="background: #fff3cd; padding: 20px; border-left: 4px solid #ffc107; margin: 20px 0;">
                <p style="margin: 0 0 10px 0; font-weight: bold; color: #856404;">⚠️ Email Adresinizi Doğrulayın</p>
                <p style="margin: 0 0 15px 0; color: #856404;">Hesabınızı aktifleştirmek için lütfen aşağıdaki butona tıklayın:</p>
                <a href="{verification_link}" style="display: inline-block; padding: 12px 30px; background: #ffc107; color: #000; text-decoration: none; border-radius: 5px; font-weight: bold;">Email Adresimi Doğrula</a>
            </div>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; padding: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">MeetDelux'a Hoş Geldiniz!</h1>
                </div>
                <div class="content">
                    <p>Merhaba <strong>{user_name}</strong>,</p>
                    <p>MeetDelux ailesine katıldığınız için teşekkür ederiz! Türkiye'nin en prestijli seminer salonu platformuna hoş geldiniz.</p>
                    
                    {verification_section}
                    
                    <p><strong>Neler yapabilirsiniz?</strong></p>
                    <ul>
                        <li>Türkiye'nin en lüks otellerinde seminer salonları keşfedin</li>
                        <li>Online rezervasyon yapın</li>
                        <li>Güvenli ödeme sistemi ile ödeyin</li>
                        <li>Rezervasyonlarınızı yönetin</li>
                    </ul>
                    
                    <p>Sorularınız için bize ulaşabilirsiniz.</p>
                    <p>İyi günler dileriz!</p>
                </div>
                <div class="footer">
                    <p>MeetDelux - Türkiye'nin En Prestijli Seminer Salonu Platformu</p>
                    <p>Bu email otomatik olarak gönderilmiştir.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_login_notification(self, user_email: str, user_name: str, login_time: datetime, ip_address: str = "Bilinmiyor"):
        """Send login notification email"""
        subject = "MeetDelux Giriş Bildirimi 🔐"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #667eea; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 15px; margin: 15px 0; border-left: 4px solid #667eea; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Giriş Bildirimi</h2>
                </div>
                <div class="content">
                    <p>Merhaba <strong>{user_name}</strong>,</p>
                    <p>Hesabınıza yeni bir giriş yapıldı:</p>
                    
                    <div class="info-box">
                        <p style="margin: 5px 0;"><strong>Tarih/Saat:</strong> {login_time.strftime('%d.%m.%Y %H:%M')}</p>
                        <p style="margin: 5px 0;"><strong>IP Adresi:</strong> {ip_address}</p>
                    </div>
                    
                    <p>Bu giriş sizseniz, herhangi bir işlem yapmanıza gerek yok.</p>
                    <p>Eğer bu giriş size ait değilse, lütfen derhal şifrenizi değiştirin ve bizimle iletişime geçin.</p>
                </div>
                <div class="footer">
                    <p>MeetDelux Güvenlik Ekibi</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_booking_confirmation(self, user_email: str, user_name: str, booking_details: dict):
        """Send booking confirmation email"""
        subject = "Rezervasyonunuz Alındı ✅"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .booking-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border: 2px solid #667eea; }}
                .detail-row {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
                .total {{ font-size: 20px; font-weight: bold; color: #667eea; margin-top: 15px; padding-top: 15px; border-top: 2px solid #667eea; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">🎉 Rezervasyonunuz Alındı!</h1>
                </div>
                <div class="content">
                    <p>Sayın <strong>{user_name}</strong>,</p>
                    <p>Rezervasyonunuz başarıyla alınmıştır. Otel yönetimi rezervasyonunuzu inceleyecek ve en kısa sürede onaylayacaktır.</p>
                    
                    <div class="booking-box">
                        <h3 style="margin-top: 0;">Rezervasyon Detayları</h3>
                        <div class="detail-row">
                            <strong>Rezervasyon No:</strong> {booking_details.get('booking_id', 'N/A')}
                        </div>
                        <div class="detail-row">
                            <strong>Otel:</strong> {booking_details.get('hotel_name', 'N/A')}
                        </div>
                        <div class="detail-row">
                            <strong>Salon:</strong> {booking_details.get('room_name', 'N/A')}
                        </div>
                        <div class="detail-row">
                            <strong>Tarih:</strong> {booking_details.get('date', 'N/A')}
                        </div>
                        <div class="detail-row">
                            <strong>Saat:</strong> {booking_details.get('time', 'N/A')}
                        </div>
                        <div class="detail-row">
                            <strong>Katılımcı Sayısı:</strong> {booking_details.get('participants', 'N/A')} kişi
                        </div>
                        <div class="total">
                            <strong>Toplam Tutar:</strong> {booking_details.get('total_price', 'N/A')}
                        </div>
                    </div>
                    
                    <p>Rezervasyonunuz onaylandığında tarafınıza bilgilendirme yapılacaktır.</p>
                    <p>İyi günler dileriz!</p>
                </div>
                <div class="footer">
                    <p>MeetDelux - Türkiye'nin En Prestijli Seminer Salonu Platformu</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_booking_approved(self, user_email: str, user_name: str, booking_details: dict):
        """Send booking approval notification"""
        subject = "Rezervasyonunuz Onaylandı! 🎊"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .success-icon {{ font-size: 60px; text-align: center; margin: 20px 0; }}
                .booking-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">Harika Haber!</h1>
                    <p style="margin: 10px 0 0 0;">Rezervasyonunuz Onaylandı</p>
                </div>
                <div class="content">
                    <div class="success-icon">✅</div>
                    <p>Sayın <strong>{user_name}</strong>,</p>
                    <p>Rezervasyonunuz otel yönetimi tarafından onaylanmıştır. Artık etkinliğinizi gerçekleştirebilirsiniz!</p>
                    
                    <div class="booking-box">
                        <h3 style="margin-top: 0;">Onaylanan Rezervasyon</h3>
                        <p><strong>Rezervasyon No:</strong> {booking_details.get('booking_id', 'N/A')}</p>
                        <p><strong>Otel:</strong> {booking_details.get('hotel_name', 'N/A')}</p>
                        <p><strong>Salon:</strong> {booking_details.get('room_name', 'N/A')}</p>
                        <p><strong>Tarih:</strong> {booking_details.get('date', 'N/A')}</p>
                        <p><strong>Saat:</strong> {booking_details.get('time', 'N/A')}</p>
                    </div>
                    
                    <p>Etkinliğinizde başarılar dileriz!</p>
                </div>
                <div class="footer">
                    <p>MeetDelux - Türkiye'nin En Prestijli Seminer Salonu Platformu</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_booking_rejected(self, user_email: str, user_name: str, booking_details: dict, reason: str = ""):
        """Send booking rejection notification"""
        subject = "Rezervasyon Durumu Hakkında Bilgilendirme"
        
        reason_section = ""
        if reason:
            reason_section = f'<p style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107;"><strong>Red Nedeni:</strong> {reason}</p>'
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #ef4444; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .booking-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Rezervasyon Durumu</h2>
                </div>
                <div class="content">
                    <p>Sayın <strong>{user_name}</strong>,</p>
                    <p>Maalesef rezervasyonunuz otel yönetimi tarafından onaylanamamıştır.</p>
                    
                    {reason_section}
                    
                    <div class="booking-box">
                        <p><strong>Rezervasyon No:</strong> {booking_details.get('booking_id', 'N/A')}</p>
                        <p><strong>Otel:</strong> {booking_details.get('hotel_name', 'N/A')}</p>
                        <p><strong>Tarih:</strong> {booking_details.get('date', 'N/A')}</p>
                    </div>
                    
                    <p>Alternatif tarih ve salonlar için platformumuzu incelemeye devam edebilirsiniz.</p>
                    <a href="{self.app_url}/rooms" class="button">Salon Ara</a>
                </div>
                <div class="footer">
                    <p>MeetDelux - Türkiye'nin En Prestijli Seminer Salonu Platformu</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_hotel_registration_pending(self, user_email: str, user_name: str, hotel_name: str):
        """Send hotel registration pending notification"""
        subject = f"{hotel_name} - Kaydınız Alındı, Onay Bekleniyor"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #667eea; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">Başvurunuz Alındı!</h1>
                </div>
                <div class="content">
                    <p>Sayın <strong>{user_name}</strong>,</p>
                    <p><strong>{hotel_name}</strong> otel kaydınız başarıyla alınmıştır.</p>
                    
                    <p>Otel bilgileriniz admin ekibimiz tarafından incelenecek ve en kısa sürede değerlendirilecektir.</p>
                    
                    <p><strong>Sonraki Adımlar:</strong></p>
                    <ul>
                        <li>Admin onayı bekleniyor</li>
                        <li>Onay aldığınızda email ile bilgilendirileceksiniz</li>
                        <li>Onay sonrası hemen seminer salonları eklemeye başlayabilirsiniz</li>
                    </ul>
                    
                    <p>Teşekkür ederiz!</p>
                </div>
                <div class="footer">
                    <p>MeetDelux Yönetim Ekibi</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_hotel_approved(self, user_email: str, user_name: str, hotel_name: str):
        """Send hotel approval notification"""
        subject = f"Harika Haber! {hotel_name} Yayına Alındı! 🎉"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .success-icon {{ font-size: 60px; text-align: center; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #10b981; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">Tebrikler!</h1>
                </div>
                <div class="content">
                    <div class="success-icon">🎊</div>
                    <p>Sayın <strong>{user_name}</strong>,</p>
                    <p><strong>{hotel_name}</strong> otelininiz admin onayından geçmiştir ve artık MeetDelux platformunda yayındadır!</p>
                    
                    <p><strong>Artık yapabilecekleriniz:</strong></p>
                    <ul>
                        <li>Seminer salonları ekleyin</li>
                        <li>Fiyatlandırma yapın</li>
                        <li>Rezervasyonları yönetin</li>
                        <li>Müşterilerle iletişime geçin</li>
                    </ul>
                    
                    <a href="{self.app_url}/dashboard" class="button">Dashboard'a Git</a>
                    
                    <p>Başarılar dileriz!</p>
                </div>
                <div class="footer">
                    <p>MeetDelux Yönetim Ekibi</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_hotel_rejected(self, user_email: str, user_name: str, hotel_name: str, reason: str = ""):
        """Send hotel rejection notification"""
        subject = f"{hotel_name} - Başvuru Durumu"
        
        reason_section = ""
        if reason:
            reason_section = f'<p style="background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 20px 0;"><strong>Red Nedeni:</strong> {reason}</p>'
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #ef4444; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Başvuru Durumu</h2>
                </div>
                <div class="content">
                    <p>Sayın <strong>{user_name}</strong>,</p>
                    <p>Maalesef <strong>{hotel_name}</strong> otel başvurunuz şu an için onaylanamamıştır.</p>
                    
                    {reason_section}
                    
                    <p>Bilgilerinizi güncelleyerek tekrar başvuru yapabilirsiniz.</p>
                    <p>Daha fazla bilgi için bizimle iletişime geçebilirsiniz.</p>
                </div>
                <div class="footer">
                    <p>MeetDelux Yönetim Ekibi</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_new_booking_to_hotel(self, hotel_email: str, hotel_name: str, booking_details: dict):
        """Send new booking notification to hotel manager"""
        subject = "Yeni Rezervasyon Aldınız! 📋"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #667eea; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .booking-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border: 2px solid #667eea; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">Yeni Rezervasyon!</h1>
                </div>
                <div class="content">
                    <p>Merhaba,</p>
                    <p><strong>{hotel_name}</strong> için yeni bir rezervasyon aldınız.</p>
                    
                    <div class="booking-box">
                        <h3 style="margin-top: 0;">Rezervasyon Detayları</h3>
                        <p><strong>Rezervasyon No:</strong> {booking_details.get('booking_id', 'N/A')}</p>
                        <p><strong>Müşteri:</strong> {booking_details.get('customer_name', 'N/A')}</p>
                        <p><strong>Email:</strong> {booking_details.get('customer_email', 'N/A')}</p>
                        <p><strong>Telefon:</strong> {booking_details.get('customer_phone', 'N/A')}</p>
                        <p><strong>Salon:</strong> {booking_details.get('room_name', 'N/A')}</p>
                        <p><strong>Tarih:</strong> {booking_details.get('date', 'N/A')}</p>
                        <p><strong>Saat:</strong> {booking_details.get('time', 'N/A')}</p>
                        <p><strong>Katılımcı:</strong> {booking_details.get('participants', 'N/A')} kişi</p>
                        <p><strong>Toplam:</strong> {booking_details.get('total_price', 'N/A')}</p>
                    </div>
                    
                    <p>Lütfen rezervasyonu inceleyin ve onaylayın.</p>
                    <a href="{self.app_url}/dashboard" class="button">Rezervasyonu İncele</a>
                </div>
                <div class="footer">
                    <p>MeetDelux Bildirim Sistemi</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(hotel_email, subject, html_content)
    
    def send_booking_reminder(self, user_email: str, user_name: str, booking_details: dict):
        """Send booking reminder (1 day before)"""
        subject = "Yarın Etkinliğiniz Var! ⏰"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .reminder-icon {{ font-size: 60px; text-align: center; margin: 20px 0; }}
                .booking-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; border: 2px solid #f59e0b; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1 style="margin: 0;">Etkinlik Hatırlatması</h1>
                </div>
                <div class="content">
                    <div class="reminder-icon">⏰</div>
                    <p>Sayın <strong>{user_name}</strong>,</p>
                    <p>Yarın etkinliğiniz var! Unutmayın:</p>
                    
                    <div class="booking-box">
                        <h3 style="margin-top: 0;">Etkinlik Detayları</h3>
                        <p><strong>Otel:</strong> {booking_details.get('hotel_name', 'N/A')}</p>
                        <p><strong>Salon:</strong> {booking_details.get('room_name', 'N/A')}</p>
                        <p><strong>Tarih:</strong> {booking_details.get('date', 'N/A')}</p>
                        <p><strong>Saat:</strong> {booking_details.get('time', 'N/A')}</p>
                        <p><strong>Adres:</strong> {booking_details.get('address', 'N/A')}</p>
                    </div>
                    
                    <p><strong>Öneriler:</strong></p>
                    <ul>
                        <li>Lütfen 15 dakika önceden hazır olun</li>
                        <li>Gerekli ekipmanlarınızı kontrol edin</li>
                        <li>Trafik durumunu göz önünde bulundurun</li>
                    </ul>
                    
                    <p>İyi etkinlikler dileriz!</p>
                </div>
                <div class="footer">
                    <p>MeetDelux Hatırlatma Servisi</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_content)
    
    def send_admin_new_hotel_notification(self, hotel_details: dict):
        """Send new hotel notification to admin"""
        admin_email = "admin@meetdelux.com"  # Admin email
        subject = f"Yeni Otel Kaydı: {hotel_details.get('hotel_name', 'N/A')}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #667eea; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; }}
                .hotel-box {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Yeni Otel Kaydı</h2>
                </div>
                <div class="content">
                    <p>Yeni bir otel kaydı yapıldı ve onay bekliyor:</p>
                    
                    <div class="hotel-box">
                        <p><strong>Otel Adı:</strong> {hotel_details.get('hotel_name', 'N/A')}</p>
                        <p><strong>Şehir:</strong> {hotel_details.get('city', 'N/A')}</p>
                        <p><strong>Yönetici:</strong> {hotel_details.get('manager_name', 'N/A')}</p>
                        <p><strong>Email:</strong> {hotel_details.get('manager_email', 'N/A')}</p>
                        <p><strong>Telefon:</strong> {hotel_details.get('phone', 'N/A')}</p>
                    </div>
                    
                    <p>Lütfen admin panelinden oteli inceleyin ve onaylayın.</p>
                    <a href="{self.app_url}/dashboard" class="button">Admin Paneline Git</a>
                </div>
                <div class="footer">
                    <p>MeetDelux Admin Bildirim Sistemi</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(admin_email, subject, html_content)


# Create singleton instance
email_service = EmailService()
