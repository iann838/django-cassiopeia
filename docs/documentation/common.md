# Setup Django

After installing using pip: 
```python
pip install django-cassiopeia
```

## Add app to your installed apps

File: `settings.py`

* Append `django_cassiopeia`.

    ```python{8}
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_cassiopeia',
    ]
    ```

## Common Settings

File: `settings.py`

| Settings variable             | Usage | Accepts | Default |
| ----------------------------- | ----- | ------- | ------- |
| `CASSIOPEIA_VERSION_FROM_MATCH` | The strategy of the match version is being pulled. This is typically not needed since all endpoints are v4 at the moment, it was created when there were different version of matches | `"patch"`, `"version"`, `"latest"` | `"patch"` |
| `CASSIOPEIA_DEFAULT_REGION` | Default region used when no Region is specified in cassiopeia objects calls | Region in caps: `"NA", "KR"`, etc | `"NA"` |
| `CASSIOPEIA_LOGGING` | Logging level used on cassiopeia | Dict > `print_calls`: boolean, print when a call is made to Riot API, `print_riot_api_key`: print api key on request, `default` & `core`: levels of the `logging` module, defaults to `WARNING` | Example below is default |

```python
CASSIOPEIA_VERSION_FROM_MATCH = "patch"
CASSIOPEIA_DEFAULT_REGION = "NA"
CASSIOPEIA_LOGGING = {
    "PRINT_CALLS": True,
    "PRINT_RIOT_API_KEY": False,
    "DEFAULT": "WARNING",
    "CORE": "WARNING"
}
```
::: tip
The setting `"CASSIOPEIA_VERSION_FROM_MATCH"` is typically not needed since all endpoints are v4 at the moment, it was created when there were different version of matches
:::

::: warning
Do not set `"PRINT_RIOT_API_KEY"` to `True` in production!
:::