EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

AUTHENTICATION_BACKENDS = (
 # Needed to login by username in Django admin, regardless of `allauth`
 "django.contrib.auth.backends.ModelBackend",

 # `allauth` specific authentication methods, such as login by e-mail
 "allauth.account.auth_backends.AuthenticationBackend",
)


# SERVER_EMAIL = ''
# DEFAULT_FROM_EMAIL = ''
# ADMINS = (('Your name', 'your@email.here'),)

# EMAIL_HOST = 'your.host.ip'
EMAIL_HOST_USER = 'test@tes.com'
# EMAIL_HOST_PASSWORD = 'SMTP Password'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True