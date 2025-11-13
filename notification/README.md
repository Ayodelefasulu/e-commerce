# Notification System

A comprehensive notification system for the e-commerce platform that handles email notifications and in-app notifications.

## Features

- ✅ Welcome email on user registration
- ✅ Order notifications (placed, shipped, delivered)
- ✅ Payment notifications
- ✅ Password reset emails
- ✅ Generic notification system
- ✅ In-app notification storage
- ✅ Email templates (HTML and plain text)
- ✅ Automatic notifications via signals

## Setup

### 1. Run Migrations

```bash
python manage.py makemigrations notification
python manage.py migrate
```

### 2. Configure Email Settings

Add to your `.env` file:

```env
# For development (emails print to console)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# For production (use SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@ecommerce.com
```

### 3. Gmail Setup (if using Gmail)

1. Enable 2-Step Verification on your Google account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password in `EMAIL_HOST_PASSWORD`

## Usage

### Sending Welcome Email

The welcome email is automatically sent when a user registers via the `RegisterView`. This is handled in `user/views.py`.

### Sending Order Notifications

```python
from notification.services import NotificationService

# When order is placed
NotificationService.send_order_placed_email(user, order)

# When order is shipped
NotificationService.send_order_shipped_email(user, order)
```

### Sending Payment Notifications

```python
from notification.services import NotificationService

NotificationService.send_payment_received_email(user, payment)
```

### Sending Password Reset Email

```python
from notification.services import NotificationService

reset_link = f"https://yourapp.com/reset-password/{token}"
NotificationService.send_password_reset_email(user, reset_link)
```

### Creating Generic Notifications

```python
from notification.services import NotificationService

# Create notification with email
NotificationService.create_notification(
    user=user,
    notification_type='promotion',
    title='Special Offer!',
    message='Get 20% off on all products!',
    send_email=True
)

# Create notification without email
NotificationService.create_notification(
    user=user,
    notification_type='system',
    title='System Update',
    message='We have updated our platform.',
    send_email=False
)
```

## Notification Types

Available notification types in the system:

- `welcome` - Welcome email for new users
- `order_placed` - Order confirmation
- `order_shipped` - Order shipping notification
- `order_delivered` - Order delivery notification
- `payment_received` - Payment confirmation
- `password_reset` - Password reset request
- `account_activated` - Account activation
- `account_deactivated` - Account deactivation
- `promotion` - Promotional emails
- `system` - System notifications

## Email Templates

Email templates are located in `templates/notification/emails/`:

- `welcome.html` / `welcome.txt` - Welcome email
- `order_placed.html` / `order_placed.txt` - Order confirmation
- `order_shipped.html` / `order_shipped.txt` - Shipping notification
- `payment_received.html` / `payment_received.txt` - Payment confirmation
- `password_reset.html` / `password_reset.txt` - Password reset
- `generic.html` / `generic.txt` - Generic notification template

You can customize these templates to match your brand.

## Admin Interface

Notifications can be managed in the Django admin:

- View all notifications
- Filter by type, read status, email sent status
- Search by user, title, or message
- View notification details

## API Integration

To add notification endpoints to your API:

```python
# In notification/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
```

## Best Practices

1. **Use Celery for Async Emails**: For production, use Celery to send emails asynchronously to avoid blocking requests.

2. **Error Handling**: The notification service includes error handling and logging. Failed emails are logged but don't break the main flow.

3. **Email Queue**: Consider using a task queue (Celery) for sending emails in production to handle high volumes.

4. **Template Customization**: Customize email templates to match your brand colors and style.

5. **Testing**: Test email sending in development using the console backend before switching to SMTP.

## Future Enhancements

- [ ] SMS notifications
- [ ] Push notifications
- [ ] Notification preferences (user can choose what to receive)
- [ ] Email unsubscription
- [ ] Notification batching
- [ ] Celery integration for async processing

