[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/paaksing/django-cassiopeia/blob/master/LICENSE.txt)

# Django Cassiopeia

Django Cassiopeia has finished beta test, Django Cassiopeia 2 has **_backward incompatible changes_**, please check them out [here](https://paaksing.github.io/django-cassiopeia/documentation/migrating1to2.html).

An Integration of [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) to the Django Framework (Compatible with DRF) with enhanced new features.

Cassiopeia is a Python adaptation of the Riot Games League of Legends API (https://developer.riotgames.com/). For instance it is also the sister library to [Orianna](https://github.com/robrua/Orianna) (Java). It's been designed with usability in mind - making sure all the bookkeeping is done right so you can focus on getting the data you need and building your application.

## Documentation
Django Cassiopeia has detailed [documentation](https://paaksing.github.io/django-cassiopeia/).
For functions and methods of Cassiopeia is found in this [documentation](http://cassiopeia.readthedocs.org/en/latest/).

## Installation and Requirements
```python
Django>=3.0.1
Python>=3.6

pip install django-cassiopeia
```

> ### v2.1
> Starting version 2.1, django-cassiopeia will no longer contain cassiopeia in its modules, instead it will wrap you original cassiopeia framework with the necessary changes in place. This makes easy to get ahead of fixes of the main library without the need of me doing pararel updates, when cassiopeia updates a new version, you can get going by only upgrading cassiopeia with `pip install cassiopeia --upgrade`.

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

## High Concurrency and AsyncIO

Currently Cassiopeia is 98% thread safe with some exception on the patch number files that complains about a generator in extreme cases. So you can feel 98% safe to multithread Cassiopeia in your environments.

If you need higher concurrency and wants to work with AsyncIO then consider using my AsyncIO based framework [Pyot](https://github.com/paaksing/Pyot). It works like magic, benchmarks of 60 to 90 calls per second on a CPU optimized machine at extreme cases. It has extremely similar syntax to Cassiopeia, supports Django out of the box, wide range of Caches (Django, Redis, Disk, MongoDB), access to CDragon and MerakiCDN.

## Questions/Contributions/Bugs
* For Django Cassiopeia: Feel free to send pull requests or to contact us via this github or our general [discord](https://discord.gg/uYW7qhP). More information can be found in our [documentation](https://paaksing.github.io/django-cassiopeia/).
* For Cassiopeia: feel free to send pull requests or to contact cassiopeia devs via [cassiopeia's github](https://github.com/meraki-analytics/cassiopeia) or the same discord server. More information about main cassiopeia is found in this [documentation](http://cassiopeia.readthedocs.org/en/latest/).

## Disclaimer
Django Cassiopeia existence is acknowleged by cassiopeia's former developers. Both package/framework/library is updated in parallel with some exceptions due to the fact of different use cases.

Cassiopeia/Django-Cassiopeia isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
