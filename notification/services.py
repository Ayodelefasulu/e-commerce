"""
Notification service for sending emails and creating notifications
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Notification
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class NotificationService:
    """
    Service class for handling notifications
    """
    
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new user"""
        try:
            subject = 'Welcome to Our E-commerce Platform!'
            context = {
                'user': user,
                'username': user.username,
                'email': user.email,
            }
            
            # Render email template
            html_message = render_to_string('notification/emails/welcome.html', context)
            plain_message = render_to_string('notification/emails/welcome.txt', context)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            # Create notification record
            notification = Notification.objects.create(
                user=user,
                notification_type='welcome',
                title='Welcome to Our Platform!',
                message=f'Welcome {user.username}! Thank you for joining us.',
                email_sent=True,
            )
            notification.mark_email_sent()
            
            logger.info(f"Welcome email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending welcome email to {user.email}: {str(e)}")
            # Still create notification even if email fails
            Notification.objects.create(
                user=user,
                notification_type='welcome',
                title='Welcome to Our Platform!',
                message=f'Welcome {user.username}! Thank you for joining us.',
                email_sent=False,
            )
            return False
    
    @staticmethod
    def send_order_placed_email(user, order):
        """Send email when order is placed"""
        try:
            subject = f'Order Confirmation - Order #{order.id}'
            context = {
                'user': user,
                'order': order,
            }
            
            html_message = render_to_string('notification/emails/order_placed.html', context)
            plain_message = render_to_string('notification/emails/order_placed.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            notification = Notification.objects.create(
                user=user,
                notification_type='order_placed',
                title=f'Order #{order.id} Placed',
                message=f'Your order #{order.id} has been placed successfully.',
                email_sent=True,
            )
            notification.mark_email_sent()
            
            logger.info(f"Order placed email sent to {user.email} for order #{order.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending order email to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_order_shipped_email(user, order):
        """Send email when order is shipped"""
        try:
            subject = f'Your Order #{order.id} Has Been Shipped!'
            context = {
                'user': user,
                'order': order,
            }
            
            html_message = render_to_string('notification/emails/order_shipped.html', context)
            plain_message = render_to_string('notification/emails/order_shipped.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            notification = Notification.objects.create(
                user=user,
                notification_type='order_shipped',
                title=f'Order #{order.id} Shipped',
                message=f'Your order #{order.id} has been shipped.',
                email_sent=True,
            )
            notification.mark_email_sent()
            
            logger.info(f"Order shipped email sent to {user.email} for order #{order.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending shipping email to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_payment_received_email(user, payment):
        """Send email when payment is received"""
        try:
            subject = f'Payment Received - ${payment.amount}'
            context = {
                'user': user,
                'payment': payment,
            }
            
            html_message = render_to_string('notification/emails/payment_received.html', context)
            plain_message = render_to_string('notification/emails/payment_received.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            notification = Notification.objects.create(
                user=user,
                notification_type='payment_received',
                title=f'Payment Received - ${payment.amount}',
                message=f'We have received your payment of ${payment.amount}.',
                email_sent=True,
            )
            notification.mark_email_sent()
            
            logger.info(f"Payment email sent to {user.email} for payment ${payment.amount}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending payment email to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def send_password_reset_email(user, reset_link):
        """Send password reset email"""
        try:
            subject = 'Password Reset Request'
            context = {
                'user': user,
                'reset_link': reset_link,
            }
            
            html_message = render_to_string('notification/emails/password_reset.html', context)
            plain_message = render_to_string('notification/emails/password_reset.txt', context)
            
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            
            notification = Notification.objects.create(
                user=user,
                notification_type='password_reset',
                title='Password Reset Request',
                message='You have requested to reset your password.',
                email_sent=True,
            )
            notification.mark_email_sent()
            
            logger.info(f"Password reset email sent to {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending password reset email to {user.email}: {str(e)}")
            return False
    
    @staticmethod
    def create_notification(user, notification_type, title, message, send_email=False):
        """Generic method to create a notification"""
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
        )
        
        if send_email:
            try:
                subject = title
                context = {
                    'user': user,
                    'notification': notification,
                }
                
                html_message = render_to_string('notification/emails/generic.html', context)
                plain_message = render_to_string('notification/emails/generic.txt', context)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                
                notification.mark_email_sent()
                logger.info(f"Notification email sent to {user.email}")
                
            except Exception as e:
                logger.error(f"Error sending notification email to {user.email}: {str(e)}")
        
        return notification

