import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List
import logging
from jinja2 import Template
import os

from app.core.config import settings

logger = logging.getLogger(__name__)

class EmailService:
    """Secure email service for sending transactional emails."""
    
    def __init__(self):
        self.smtp_server = getattr(settings, 'smtp_server', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'smtp_port', 587)
        self.smtp_username = getattr(settings, 'smtp_username', None)
        self.smtp_password = getattr(settings, 'smtp_password', None)
        self.from_email = getattr(settings, 'from_email', 'noreply@footybets.ai')
        self.from_name = getattr(settings, 'from_name', 'FootyBets.ai')
        
        # Email templates
        self.templates = {
            'verification': self._get_verification_template(),
            'password_reset': self._get_password_reset_template(),
            'welcome': self._get_welcome_template(),
            'security_alert': self._get_security_alert_template()
        }
    
    def _get_verification_template(self) -> Template:
        """Get email verification template."""
        return Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email - FootyBets.ai</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #3b82f6; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9fafb; }
                .button { display: inline-block; padding: 12px 24px; background: #3b82f6; color: white; text-decoration: none; border-radius: 6px; }
                .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
                .security-note { background: #fef3c7; border: 1px solid #f59e0b; padding: 15px; border-radius: 6px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to FootyBets.ai!</h1>
                </div>
                <div class="content">
                    <h2>Verify Your Email Address</h2>
                    <p>Hi {{ username }},</p>
                    <p>Thank you for registering with FootyBets.ai! To complete your registration and start using our AI-powered AFL predictions, please verify your email address.</p>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="{{ verification_url }}" class="button">Verify Email Address</a>
                    </p>
                    
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #6b7280;">{{ verification_url }}</p>
                    
                    <div class="security-note">
                        <strong>Security Note:</strong> This verification link will expire in 24 hours. If you didn't create an account with FootyBets.ai, please ignore this email.
                    </div>
                    
                    <p>Once verified, you'll have access to:</p>
                    <ul>
                        <li>AI-powered AFL game predictions</li>
                        <li>Historical performance analytics</li>
                        <li>Real-time game updates</li>
                        <li>Personalized betting insights</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>© 2024 FootyBets.ai. All rights reserved.</p>
                    <p>This email was sent to {{ email }}. If you have any questions, please contact our support team.</p>
                </div>
            </div>
        </body>
        </html>
        """)
    
    def _get_password_reset_template(self) -> Template:
        """Get password reset template."""
        return Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Your Password - FootyBets.ai</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #ef4444; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9fafb; }
                .button { display: inline-block; padding: 12px 24px; background: #ef4444; color: white; text-decoration: none; border-radius: 6px; }
                .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
                .security-note { background: #fef3c7; border: 1px solid #f59e0b; padding: 15px; border-radius: 6px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Password Reset Request</h1>
                </div>
                <div class="content">
                    <h2>Reset Your Password</h2>
                    <p>Hi {{ username }},</p>
                    <p>We received a request to reset your password for your FootyBets.ai account. Click the button below to create a new password:</p>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="{{ reset_url }}" class="button">Reset Password</a>
                    </p>
                    
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #6b7280;">{{ reset_url }}</p>
                    
                    <div class="security-note">
                        <strong>Security Note:</strong> This link will expire in 24 hours. If you didn't request a password reset, please ignore this email and your password will remain unchanged.
                    </div>
                    
                    <p>For your security, we recommend:</p>
                    <ul>
                        <li>Using a strong, unique password</li>
                        <li>Enabling two-factor authentication if available</li>
                        <li>Never sharing your password with anyone</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>© 2024 FootyBets.ai. All rights reserved.</p>
                    <p>This email was sent to {{ email }}. If you have any questions, please contact our support team.</p>
                </div>
            </div>
        </body>
        </html>
        """)
    
    def _get_welcome_template(self) -> Template:
        """Get welcome email template."""
        return Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to FootyBets.ai!</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #10b981; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9fafb; }
                .button { display: inline-block; padding: 12px 24px; background: #10b981; color: white; text-decoration: none; border-radius: 6px; }
                .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to FootyBets.ai!</h1>
                </div>
                <div class="content">
                    <h2>Your Account is Now Active</h2>
                    <p>Hi {{ username }},</p>
                    <p>Welcome to FootyBets.ai! Your account has been successfully verified and you're now ready to access our AI-powered AFL predictions.</p>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="{{ login_url }}" class="button">Get Started</a>
                    </p>
                    
                    <h3>What you can do now:</h3>
                    <ul>
                        <li><strong>View AI Predictions:</strong> Get detailed predictions for upcoming AFL games</li>
                        <li><strong>Track Performance:</strong> Monitor the accuracy of our AI predictions</li>
                        <li><strong>Analytics Dashboard:</strong> Access comprehensive betting analytics</li>
                        <li><strong>Personalized Insights:</strong> Receive tailored betting recommendations</li>
                    </ul>
                    
                    <h3>Getting Started Tips:</h3>
                    <ul>
                        <li>Complete your profile to get personalized recommendations</li>
                        <li>Set up notification preferences for game updates</li>
                        <li>Explore our analytics to understand prediction accuracy</li>
                        <li>Check out our FAQ for betting tips and strategies</li>
                    </ul>
                </div>
                <div class="footer">
                    <p>© 2024 FootyBets.ai. All rights reserved.</p>
                    <p>Thank you for choosing FootyBets.ai for your AFL betting insights!</p>
                </div>
            </div>
        </body>
        </html>
        """)
    
    def _get_security_alert_template(self) -> Template:
        """Get security alert template."""
        return Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Security Alert - FootyBets.ai</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #f59e0b; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9fafb; }
                .alert { background: #fef3c7; border: 1px solid #f59e0b; padding: 15px; border-radius: 6px; margin: 20px 0; }
                .button { display: inline-block; padding: 12px 24px; background: #f59e0b; color: white; text-decoration: none; border-radius: 6px; }
                .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Security Alert</h1>
                </div>
                <div class="content">
                    <h2>Unusual Activity Detected</h2>
                    <p>Hi {{ username }},</p>
                    <p>We detected unusual activity on your FootyBets.ai account:</p>
                    
                    <div class="alert">
                        <strong>Event:</strong> {{ event_type }}<br>
                        <strong>Time:</strong> {{ event_time }}<br>
                        <strong>Location:</strong> {{ location }}<br>
                        <strong>IP Address:</strong> {{ ip_address }}
                    </div>
                    
                    <p>If this was you, no action is required. However, if you don't recognize this activity:</p>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="{{ security_url }}" class="button">Review Account Security</a>
                    </p>
                    
                    <h3>Recommended Actions:</h3>
                    <ul>
                        <li>Change your password immediately</li>
                        <li>Enable two-factor authentication</li>
                        <li>Review your recent account activity</li>
                        <li>Contact support if you need assistance</li>
                    </ul>
                    
                    <p><strong>Security Tip:</strong> Never share your login credentials with anyone, and always log out from shared devices.</p>
                </div>
                <div class="footer">
                    <p>© 2024 FootyBets.ai. All rights reserved.</p>
                    <p>This is an automated security alert. If you have questions, please contact our support team.</p>
                </div>
            </div>
        </body>
        </html>
        """)
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[dict]] = None
    ) -> bool:
        """Send an email securely."""
        try:
            if not all([self.smtp_username, self.smtp_password]):
                logger.warning("SMTP credentials not configured. Email not sent.")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add attachments if any
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment['data'])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {attachment["filename"]}'
                    )
                    msg.attach(part)
            
            # Send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    @classmethod
    def send_verification_email(cls, email: str, token: str, username: str = None):
        """Send email verification email."""
        service = cls()
        verification_url = f"{getattr(settings, 'frontend_url', 'https://footybets.ai')}/verify-email/{token}"
        
        html_content = service.templates['verification'].render(
            username=username or email.split('@')[0],
            email=email,
            verification_url=verification_url
        )
        
        return service.send_email(
            to_email=email,
            subject="Verify Your Email - FootyBets.ai",
            html_content=html_content
        )
    
    @classmethod
    def send_password_reset_email(cls, email: str, token: str, username: str = None):
        """Send password reset email."""
        service = cls()
        reset_url = f"{getattr(settings, 'frontend_url', 'https://footybets.ai')}/reset-password/{token}"
        
        html_content = service.templates['password_reset'].render(
            username=username or email.split('@')[0],
            email=email,
            reset_url=reset_url
        )
        
        return service.send_email(
            to_email=email,
            subject="Reset Your Password - FootyBets.ai",
            html_content=html_content
        )
    
    @classmethod
    def send_welcome_email(cls, email: str, username: str):
        """Send welcome email."""
        service = cls()
        login_url = f"{getattr(settings, 'frontend_url', 'https://footybets.ai')}/login"
        
        html_content = service.templates['welcome'].render(
            username=username,
            email=email,
            login_url=login_url
        )
        
        return service.send_email(
            to_email=email,
            subject="Welcome to FootyBets.ai!",
            html_content=html_content
        )
    
    @classmethod
    def send_security_alert(cls, email: str, username: str, event_data: dict):
        """Send security alert email."""
        service = cls()
        security_url = f"{getattr(settings, 'frontend_url', 'https://footybets.ai')}/security"
        
        html_content = service.templates['security_alert'].render(
            username=username,
            email=email,
            security_url=security_url,
            **event_data
        )
        
        return service.send_email(
            to_email=email,
            subject="Security Alert - FootyBets.ai",
            html_content=html_content
        ) 