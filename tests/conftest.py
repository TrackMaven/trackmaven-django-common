def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SITE_ID=1,
        SECRET_KEY='foo',
        INSTALLED_APPS=(
            'tests',
        ),
    )

    try:
        import django
        django.setup()
    except AttributeError:
        pass
