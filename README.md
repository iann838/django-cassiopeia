[![MIT Licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/meraki-analytics/orianna/blob/master/LICENSE.txt)
[![Documentation Status](https://readthedocs.org/projects/cassiopeia/badge/?version=latest)](http://cassiopeia.readthedocs.org/en/latest/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1170906.svg)](https://doi.org/10.5281/zenodo.1170906)

# Django Cassiopeia

An Integration of [Cassiopeia](https://github.com/meraki-analytics/cassiopeia) to the Django Framework (Compatible with DRF) including more new features.

Cassiopeia itself is a Python adaptation of the Riot Games League of Legends API (https://developer.riotgames.com/). For instance it is also the sister library to [Orianna](https://github.com/robrua/Orianna) (Java). It's been designed with usability in mind - making sure all the bookkeeping is done right so you can focus on getting the data you need and building your application.

## Cassiopeia specific Documentation
Cassiopeia has detailed [documentation](http://cassiopeia.readthedocs.org/en/latest/).

## Installation and Requirements
```python
Django>=2.2.0
Python>=3.6

pip install django-cassiopeia
```

## Why use Cassiopeia (quoting from Cassiopeia repository)?

* An excellent user interface that makes working with data from the Riot API easy and fun.

* "Perfect" rate limiting.

* Guaranteed optimal usage of your API key.

* Built in caching and (coming) the ability to easily hook into a database for offline storage of data.

* Extendability to non-Riot data. Because Cass is a framework and not just an API wrapper, you can integrate your own data sources into your project. Cass already supports Data Dragon and the ``champion.gg`` API in addition to the Riot API.

* Dynamic settings so you can configure Cass for your specific use case.

## Features Integration and Problem Fixing

* Cassiopeia current caching system does not automatically (or regularly) expire objects on expirations which might cause severe memory issues when working with web frameworks if it goes out of your control. This integration will give you the ability to use Django's cache framework for your caching, which is full production tested.

* The variety of cache backends that Cass provides may not fit your needs when paired with Django, now you can use ANY cache backends of your like that the Django's cache framework supports: Django-Redis, python-Memcached, pylibmc, Filebased, MySQL, Postgre, SQLite, ... (Check out [Django's cache framework official docs](https://docs.djangoproject.com/en/dev/topics/cache/) for more). Also ! You can configure it to have more than 1 cache, the ability to separate multiple objects to different caching system. 

* When not imported Cassiopeia correctly within the Django environment, each time you call a function that uses cass will create a new instance of it and killing all existing Ghost modules (for information of Cassiopeia's Ghost(Lazy) loading check out its [documentations](http://cassiopeia.readthedocs.org/en/latest/)), creating conflicts that might crash your server. This meant to fix (or try to fix, still under test) this problem

* The "Perfect" rate limiting does not actually work here .. since a Web Framework can behave in a variety of process flow: multi-process, async, conj. (see Existing Problems below).

* The Settings interface is adapted to a syntax that is compatible (visually) with Django Settings (see Setup for Django environment below).

## Existing Problems (minor ?) and Plans

* The current rate limiter is the same used in cassiopeia, so is rather a "Do not black list me" rate limiter (which is what the Riot Team recommends), but we (both cass and django-cass devs) prefer to not get as much 429s, a rate limiter that fits (or may fits) to Django is under going research.

## Trade-offs

* There is a caveat when using Django's cache over the Standard cache that Cassiopeia provides: It cannot cache `cassiopeia.core` objects due to the fact of its `key` not being of type `string` or a `picklable` object, so it rather caches `cassiopeia.dto` objects which then automatically be transform to `cassiopeia.core`. The time consumption difference is super minimal `cassiopeia.dto` needs some 20ms more than `cassiopeia.core`, but `cassiopeia.core` takes a lot more memory (at least 5 times more if you use compressors on your Django's cache).

## Questions/Contributions/Bugs
* For Django Cassiopeia: Feel free to send pull requests or to contact us via this github or our general [discord](https://discord.gg/uYW7qhP). More information can be found in our [documentation](http://cassiopeia.readthedocs.org/en/latest/).
* For Cassiopeia: feel free to send pull requests or to contact cassiopeia devs via [cassiopeia's github](https://github.com/meraki-analytics/cassiopeia) or the same discord server. More information about main cassiopeia is found in this [documentation](http://cassiopeia.readthedocs.org/en/latest/).

## Citing Cassiopeia (Quoting from cassiopeia repository)
If you used Cassiopeia for your research, please [cite the project](https://doi.org/10.5281/zenodo.1170906).

## Supporting Cassiopeia and Django Cassiopeia
* If you've loved using Cassiopeia, consider supporting the former developers of the main framework through [PayPal](https://www.paypal.me/merakianalytics) or [Patreon](https://www.patreon.com/merakianalytics).
* If you want to support this specific project (`django-cassiopeia`), consider supporting me through [Patreon](https://www.patreon.com/paaksing) too. 

## Disclaimer
Django Cassiopeia existence is acknowleged by cassiopeia's former developers. Both package/framework/library is updated in parallel with some exceptions due to the fact of different use cases.

Cassiopeia/Django-Cassiopeia isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.
