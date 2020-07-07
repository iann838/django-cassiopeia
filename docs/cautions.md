# Avoids and DON'Ts

Normally a documentation wouldn't have this type of section because "all the odds should be handled", this section is here because this is an integration from another library(framework), there are a lot of things that goes out of control if the developer miss identifies the differences.

## DO NOT import cassiopeia.

In `cassiopeia` the normal behavior would be:
```python
import cassiopeia as cass
```
DO NOT do this, because if you have `cassiopeia` installed in your environment, it will import `cassiopeia` FROM `cassiopeia`, which does not provides the same adaptive functionality to django. There is actually something worse: if you import it at the wrong level, every time you fire a function will import a new instance of it and killing it after execution, might not be a deal .. but if such function is fired one after the other, it will have conflict between the instances (If you want to know how it conflicts, feel free to fire some 10 ajax per second to a request that uses cass).
With `django-cassiopeia`, the correct and only way to import it is:
```python
from django-cassiopeia import cassiopeia as cass
                                         # or as whatever you want
```

## DO NOT apply settings manually.

In `cassiopeia`, it is needed to `apply_settings(yoursettingsdict)` to actually update your settings for the instance you're processing. This is not the case with `django-cassiopeia`, when you define all your settings as described in the page above, it would automatically do the `apply_settings()` for you. You can still do `apply_settings()` manually, but it will raise some exceptions if you put Django's cache in it as arguments (I am still evaluating to actually remove `apply_settings()` in this integration, fire an issue if you need it, because I really can't find a reason to leave it there).

## AVOID using cassiopeia standard cache.
^ until an actual fix is made.

This is the second time I am saying this LOL, this time more in deep of what is going on.
The standard cache that `cassiopeia` provides, can give some serious memory issues (You can go to cassiopeia's github issues tab and reference from there) due to these problems:
1. The cache does not deletes expired objects correctly, it deletes expired objects with the following condition: manually calling `expire()` (Which is what most cass users do) and firing a `GET` after the object is expired. The former solution might solve but .. it is slippy and can go out of your hand...
2. The standard cache dies everytime when you kill the django server (idk you, but I kill my dev server like every ten minutes for changes, even a production server you need to fire a restart at some point when you update features).
3. You don't have control of the objects you cache, it just caches and that's it .. with some better cache backend such as redis, database, you can do a lot more things, such as finding and deleting 1 specific key.

## Avoid using 'forever' caching

There is no point of using a cache for forever caching (which is not what a cache is intended), a warning will fire if you do it with django's cache. This will generate out of date/sync data that does not correspond to the current status of the game. (In some cases django will expire it automatically after a long period of time, so won't work either)
For forever storing an object, you can use the compatible plugin `SimpleKVDiskStore` which is a filebased store. Or simply just make a method that stores it on your database.