# Notification System - Quick Setup Guide

## ✅ What Has Been Implemented

1. **Notification Model** - Stores all notifications in the database
2. **Notification Service** - Handles sending emails and creating notifications
3. **Email Templates** - HTML and plain text templates for various notifications
4. **Welcome Email** - Automatically sent when users register
5. **Admin Interface** - Manage notifications in Django admin
6. **Email Configuration** - Ready for both development and production

## 🚀 Quick Start

### Step 1: Run Migrations

```bash
python manage.py makemigrations notification
python manage.py migrate
```

### Step 2: Configure Email (Development)

For development, emails will print to the console. No configuration needed!

### Step 3: Configure Email (Production)

Add to your `.env` file:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@ecommerce.com
```

### Step 4: Test It!

1. Register a new user via the API
2. Check the console (development) or email inbox (production)
3. Check Django admin to see the notification record

## 📧 Available Notification Methods

### 1. Welcome Email (Automatic)
- Sent automatically when user registers
- No action needed!

### 2. Order Notifications
```python
from notification.services import NotificationService

# When order is placed
NotificationService.send_order_placed_email(user, order)

# When order is shipped  
NotificationService.send_order_shipped_email(user, order)
```

### 3. Payment Notifications
```python
from notification.services import NotificationService

NotificationService.send_payment_received_email(user, payment)
```

### 4. Password Reset
```python
from notification.services import NotificationService

reset_link = f"https://yourapp.com/reset-password/{token}"
NotificationService.send_password_reset_email(user, reset_link)
```

### 5. Custom Notifications
```python
from notification.services import NotificationService

NotificationService.create_notification(
    user=user,
    notification_type='promotion',
    title='Special Offer!',
    message='Get 20% off!',
    send_email=True
)
```

## 🎨 Customizing Email Templates

Email templates are in `templates/notification/emails/`:

- Edit HTML templates for styling
- Edit TXT templates for plain text version
- Match your brand colors (currently using #783240)

## 📊 Viewing Notifications

### Django Admin
- Go to `/admin/notification/notification/`
- View all notifications
- Filter by type, read status, etc.

### For Users (Future)
You can create API endpoints to let users view their notifications:

```python
# Example API endpoint
GET /api/notifications/
GET /api/notifications/unread/
POST /api/notifications/{id}/mark-read/
```

## 🔧 Integration Examples

### In Order Views
```python
# In order/views.py
from notification.services import NotificationService

def create_order(request):
    order = Order.objects.create(...)
    NotificationService.send_order_placed_email(request.user, order)
    return Response(...)
```

### In Payment Views
```python
# In payment/views.py
from notification.services import NotificationService

def process_payment(request):
    payment = Payment.objects.create(...)
    NotificationService.send_payment_received_email(request.user, payment)
    return Response(...)
```

## 📝 Notification Types

- `welcome` - Welcome email
- `order_placed` - Order confirmation
- `order_shipped` - Shipping notification
- `order_delivered` - Delivery notification
- `payment_received` - Payment confirmation
- `password_reset` - Password reset
- `account_activated` - Account activation
- `account_deactivated` - Account deactivation
- `promotion` - Promotional emails
- `system` - System notifications

## ⚠️ Important Notes

1. **Development Mode**: Emails print to console by default
2. **Production**: Configure SMTP settings in `.env`
3. **Gmail**: Use App Password, not regular password
4. **Error Handling**: Failed emails are logged but don't break the flow
5. **Async**: Consider Celery for production to send emails asynchronously

## 🎯 Next Steps

1. ✅ Run migrations
2. ✅ Test welcome email
3. ✅ Configure production email settings
4. ✅ Integrate with order/payment views
5. ✅ Customize email templates
6. ⏳ Add API endpoints for user notifications
7. ⏳ Add Celery for async email sending
8. ⏳ Add notification preferences

## 📚 Full Documentation

See `notification/README.md` for complete documentation.

