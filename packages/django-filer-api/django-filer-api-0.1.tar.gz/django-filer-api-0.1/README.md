
=====
### API for django-filer
=====

This app implement django-filer packages with api

For More Info on Django Filer:
[https://django-filer.readthedocs.io/en/latest/](https://django-filer.readthedocs.io/en/latest/)

Quick start
-----------

1. Add "api" to your INSTALLED_APPS setting like this::
```
    INSTALLED_APPS = [
        ...
        'filer_api',
    ]
```
2 - include dependencies:
```
        INSTALLED_APPS = [
        ...
        'rest_framework',
        'rest_framework.authtoken',
        'corsheaders',
        'easy_thumbnails',
        'filer',
        'mptt',
        'filer_api',
    ]
```

3. Include the api URLconf in your project urls.py like this::

```
    path('', include('filer_api.urls')),
```

> `python manage runserver`

- Visit  http://127.0.0.1:8000/api/django-filer/images to get api

- Visit http://127.0.0.1:8000/api/django-filer/folders to get api.

- Visit http://127.0.0.1:8000/api/django-filer/folders/{:id} to get api.

