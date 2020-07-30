# Django Cassiopeia 1.1 to 2.0

A list of changes made from version 1.1 (test) to 2.0

Don't ask why I increment one entire big version, it's a secret.

## Backward Incompatible Changes

1. `RIOT_API_KEY` is now `CASSIOPEIA_RIOT_API_KEY`. This is due to a possible variable name conflict, since you might have different API keys for different games (yes I am looking at you Valorant).

2. `CASSIOPEIA_GLOBAL` has splitted into `CASSIOPEIA_VERSION_FROM_MATCH` and `CASSIOPEIA_DEFAULT_REGION` because the settings is global but wasn't global visually.

3. `CASSIOPEIA_DJANGO_CACHES` is merged back to `CASSIOPEIA_PIPELINE`, because .. it's starting to be hard to maintain. When `Omnistone` was created, an issue came up that it's limiting the flexibility of the pipeline, and makes confusions. Now you specify everything inside `CASSIOPEIA_PIPELINE` since expirations is now shorten (a lot), so it won't be large neither. Check out the example at the end of [Setup Pipeline](./pipeline.html).

## Other Changes

1. Now arguments keys can be all uppercase to fit into the Django settings syntax (e.g. instead of `"expirations_map"` now can be `"EXPIRATIONS_MAP"`).

## New Features

1. Refined version of `Cache` is introduced as `Omnistone` to maintain the fast performance.

2. A safe check lock is added to all datastore that does not belong to cassiopeia, to better avoid disaster (I guess humanity got enough in 2020).