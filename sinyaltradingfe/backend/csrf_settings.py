from django.conf import settings

# Add CSRF_TRUSTED_ORIGINS
settings.CSRF_TRUSTED_ORIGINS = ['https://pyscalp.com', 'https://www.pyscalp.com', 'http://pyscalp.com', 'http://www.pyscalp.com']

# Add CORS_ALLOWED_ORIGINS if not already set
if not hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
    settings.CORS_ALLOWED_ORIGINS = ['https://pyscalp.com', 'https://www.pyscalp.com', 'http://pyscalp.com', 'http://www.pyscalp.com']
elif not settings.CORS_ALLOWED_ORIGINS:
    settings.CORS_ALLOWED_ORIGINS = ['https://pyscalp.com', 'https://www.pyscalp.com', 'http://pyscalp.com', 'http://www.pyscalp.com']

# Add CORS_ALLOW_CREDENTIALS
settings.CORS_ALLOW_CREDENTIALS = True
