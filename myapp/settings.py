STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'myapp/static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')