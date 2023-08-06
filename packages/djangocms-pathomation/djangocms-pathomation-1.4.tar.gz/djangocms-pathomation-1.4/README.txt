=====
djangocms-pathomation
=====

Add live slide viewing capabilities to your own website built on Django CMS


Quick start
-----------

1. Add "pathomation.apps.PathomationConfig" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'pathomation.apps.PathomationConfig'
    ]

2. Make sure that you add the following to your settings.py file in your project folder:

    STATIC_URL = '/static/'

3. Run ``python manage.py migrate`` to create the necessary models.

4. Go to administration -> Pathomation -> Settings -> My Pathomation connection settings and fill in your credentials and save.

5. To make sure your credentials are correct. You can always test the connection, by clicking on the "Test connection" button

