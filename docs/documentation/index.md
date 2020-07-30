# Introduction
[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/paaksing/django-cassiopeia/blob/master/LICENSE.txt)

Django Cassiopeia has finished beta test, Django Cassiopeia 2 has **_backward incompatible changes_**, please check them out [here](./migrating1to2.html).

An Integration of [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) to the Django Framework (Compatible with DRF) with enhanced new features.

Cassiopeia is a Python adaptation of the Riot Games League of Legends API (https://developer.riotgames.com/). For instance it is also the sister library to [Orianna](https://github.com/robrua/Orianna) (Java). It's been designed with usability in mind - making sure all the bookkeeping is done right so you can focus on getting the data you need and building your application.

## Installation and Requirements
```python
Django>=3.0.1
Python>=3.6

pip install django-cassiopeia
```

## Quick Start

In your `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'django_cassiopeia',
]

CASSIOPEIA_RIOT_API_KEY = os.environ["RIOT_API_KEY"]  # api key in env var
CASSIOPEIA_DEFAULT_REGION = "NA"   # default region
CASSIOPEIA_PIPELINE = {   # small pipeine to get started
    "Omnistone": {},
    "DDragon": {},
    "RiotAPI": {},
}
```

In your `views.py` that you wish to use cassiopeia functions:
```python
from django_cassiopeia import cassiopeia as cass
from django.http import JsonResponse
from django.views import View

class SummonerView(View): # Django CBV with json response
    def get(self, request):
        summoner = cass.Summoner(name="Kalturi")
        return JsonResponse({"name": summoner.name, "level": summoner.level})
```

Reminder: it can be used anywhere as long as you do the correct import:
```python
from django_cassiopeia import cassiopeia 
# You can add "as cass" for shorter module name ^.
```

## Integrated Features

* **_Bypass the limitation of cassiopeia caching:_** No more worries about memory issues! Now you have the ability to use Django's cache framework for your caching, compatible with any cache backends that Django supports (Filebased, Database, Redis, MemCached, LocalMem, more).

* **_Same performance (New in 2.0):_** You still get the same fast performance as cassiopeia's `Cache`, here you have its fine tuned version called `Omnistone` and safe to use (I am looking at you memory hunter).

* **_Prevent infinite instances:_** Weird things will happen if you don't import correctly cassiopeia in your Django project (happens to Flask too), now you add to `INSTALLED_APPS` and import it from there, no more infinite intances crashing around.

* **_Adapted settings syntax:_** Keep all settings in one place, the standard place -> `settings.py`, with adapted syntax that fits into the Django trend.
