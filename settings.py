import os
import json

from django.conf import settings


def configure_settings():
    """
    Configures settings for manage.py and for run_tests.py.
    """
    if not settings.configured:

        # Check env for settings stored as json (used for github actions)
        if os.environ.get('DB_SETTINGS'):
            db_config = json.loads(os.environ.get('DB_SETTINGS'))

        else:
            # Determine the database settings depending on if a test_db var is set in CI mode or not
            test_db = os.environ.get('DB', 'postgres')
            if test_db == 'postgres':
                db_config = {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'newrelic_plugin_agent',
                    'USER': 'postgres',
                    'PASSWORD': '',
                    'HOST': 'db'
                }
            elif test_db == 'sqlite':
                db_config = {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': 'newrelic_plugin_agent',
                }
            else:
                raise RuntimeError('Unsupported test DB {0}'.format(test_db))


        settings.configure(
            SECRET_KEY='*',
            DEFAULT_AUTO_FIELD='django.db.models.AutoField',
            TEST_RUNNER='django_nose.NoseTestSuiteRunner',
            NOSE_ARGS=['--nocapture', '--nologcapture', '--verbosity=1'],
            DATABASES={
                'default': db_config,
            },
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'newrelic_plugin_agent',
                'newrelic_plugin_agent.tests',
            ),
            DEBUG=False,
            DDF_FILL_NULLABLE_FIELDS=False,
            MIDDLEWARE=(
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware'
            ),
            TEMPLATES=[
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                        ],
                    }
                }
            ],
        )
