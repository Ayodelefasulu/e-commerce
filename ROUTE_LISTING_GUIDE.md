# How to List All Routes in Django

In Django, there are several ways to list all your routes, similar to Laravel's `php artisan route:list`.

## Method 1: Using django-extensions (Recommended - Most Similar to Laravel)

This is the closest equivalent to Laravel's `route:list` command.

### Installation:

```bash
pip install django-extensions
```

### Add to settings.py:

```python
INSTALLED_APPS = [
    # ... other apps
    'django_extensions',
]
```

### Usage:

```bash
python manage.py show_urls
```

**Output example:**
```
/api/users/register/                    user.views.RegisterView          register
/api/users/login/                       user.views.LoginView             login
/api/users/                             user.views.UserListCreateView     user-list
/api/users/<uuid:uuid>/                 user.views.UserDetailView         user-detail
/api/token/                             rest_framework_simplejwt.views.TokenObtainPairView  token_obtain_pair
/api/token/refresh/                     rest_framework_simplejwt.views.TokenRefreshView     token_refresh
/admin/                                 django.contrib.admin.site.urls    admin
```

### Options:

```bash
# Show with more details
python manage.py show_urls --format=pretty

# Show only specific app
python manage.py show_urls --format=pretty --settings=yourproject.settings

# Show with decorators
python manage.py show_urls --format=pretty --decorator
```

---

## Method 2: Using Django Shell (Built-in)

You can use Django's shell to inspect URLs programmatically:

```bash
python manage.py shell
```

Then in the shell:

```python
from django.urls import get_resolver

def show_urls(urlconf=None, prefix=''):
    resolver = get_resolver(urlconf)
    if hasattr(resolver, 'url_patterns'):
        for pattern in resolver.url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # This is an include
                show_urls(pattern.urlconf_name, prefix + str(pattern.pattern))
            else:
                # This is a regular pattern
                print(f"{prefix}{pattern.pattern} -> {pattern.callback}")

show_urls()
```

---

## Method 3: Custom Management Command

Create a custom management command for a cleaner solution:

### Create the command file:

```bash
mkdir -p your_app/management/commands
touch your_app/management/__init__.py
touch your_app/management/commands/__init__.py
touch your_app/management/commands/show_routes.py
```

### Add to `your_app/management/commands/show_routes.py`:

```python
from django.core.management.base import BaseCommand
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver


class Command(BaseCommand):
    help = 'List all URL patterns in the project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            type=str,
            default='table',
            choices=['table', 'json', 'pretty'],
            help='Output format',
        )

    def handle(self, *args, **options):
        resolver = get_resolver()
        patterns = self._extract_patterns(resolver.url_patterns)
        
        if options['format'] == 'json':
            import json
            self.stdout.write(json.dumps(patterns, indent=2))
        elif options['format'] == 'pretty':
            for pattern in patterns:
                self.stdout.write(
                    f"{pattern['url']:50} {pattern['view']:50} {pattern['name']}"
                )
        else:  # table format
            self.stdout.write(f"{'URL':<50} {'View':<50} {'Name'}")
            self.stdout.write('-' * 150)
            for pattern in patterns:
                self.stdout.write(
                    f"{pattern['url']:<50} {pattern['view']:<50} {pattern['name']}"
                )

    def _extract_patterns(self, patterns, prefix=''):
        result = []
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                # This is an include
                nested_patterns = self._extract_patterns(
                    pattern.url_patterns,
                    prefix + str(pattern.pattern)
                )
                result.extend(nested_patterns)
            elif isinstance(pattern, URLPattern):
                # This is a regular pattern
                url = prefix + str(pattern.pattern)
                view = self._get_view_name(pattern.callback)
                name = pattern.name or ''
                result.append({
                    'url': url,
                    'view': view,
                    'name': name
                })
        return result

    def _get_view_name(self, callback):
        if hasattr(callback, 'view_class'):
            return f"{callback.view_class.__module__}.{callback.view_class.__name__}"
        elif hasattr(callback, '__name__'):
            return f"{callback.__module__}.{callback.__name__}"
        else:
            return str(callback)
```

### Usage:

```bash
python manage.py show_routes
python manage.py show_routes --format=pretty
python manage.py show_routes --format=json
```

---

## Method 4: Quick Python Script

Create a simple script `list_routes.py` in your project root:

```python
#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

def extract_urls(urlpatterns, prefix=''):
    """Extract all URL patterns from the resolver."""
    result = []
    for pattern in urlpatterns:
        if isinstance(pattern, URLResolver):
            # This is an include
            nested = extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
            result.extend(nested)
        elif isinstance(pattern, URLPattern):
            # This is a regular pattern
            url = prefix + str(pattern.pattern)
            view = pattern.callback
            if hasattr(view, 'view_class'):
                view_name = f"{view.view_class.__module__}.{view.view_class.__name__}"
            else:
                view_name = f"{view.__module__}.{view.__name__}"
            name = pattern.name or ''
            result.append((url, view_name, name))
    return result

if __name__ == '__main__':
    resolver = get_resolver()
    urls = extract_urls(resolver.url_patterns)
    
    print(f"{'URL':<50} {'View':<60} {'Name'}")
    print('-' * 150)
    for url, view, name in sorted(urls):
        print(f"{url:<50} {view:<60} {name}")
```

Run it:
```bash
python list_routes.py
```

---

## Method 5: Using Django REST Framework (if using DRF)

If you're using Django REST Framework with routers:

```bash
python manage.py shell
```

```python
from django.urls import get_resolver
from rest_framework.routers import DefaultRouter

# List all DRF router endpoints
# This will show ViewSet routes
```

---

## Quick Comparison with Laravel

| Laravel | Django Equivalent |
|---------|-------------------|
| `php artisan route:list` | `python manage.py show_urls` (with django-extensions) |
| `php artisan route:list --path=api` | `python manage.py show_urls \| grep api` |
| `php artisan route:list --method=GET` | `python manage.py show_urls \| grep GET` |

---

## Recommended Solution for Your Project

Since you're using Django REST Framework, I recommend:

1. **Install django-extensions** (easiest and most Laravel-like):
   ```bash
   pip install django-extensions
   ```

2. **Add to requirements.txt**:
   ```
   django-extensions==3.2.3
   ```

3. **Add to INSTALLED_APPS in settings.py**:
   ```python
   INSTALLED_APPS = [
       # ... existing apps
       'django_extensions',
   ]
   ```

4. **Use it**:
   ```bash
   python manage.py show_urls
   ```

This gives you the closest experience to Laravel's `route:list` command!

