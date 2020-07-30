# Setup Plugin

**Note**: This is totally _Optional_, the setting is here for flexibility.

Below is a quote from cassiopeia:

> Plugins monkeypatch Cass to provide modified or additional functionality. They are listed below.

> The plugins for Cass are stored in two different repositories: cassiopeia-plugins and cassiopeia-datastores. cassiopeia-plugins contains functionality that modify the behavior of Cass’s objects, while cassiopeia-datastores provides additional datastores (such as databases). Both of these are called “plugins” in this documentation.

> Plugins can be added to Cass by downloading the appropriate plugin and putting it on your PYTHONPATH environment variable. Then, in your settings file, you specify the name of the module for that plugin (using the package keyword) as if you were directly importing it into your project. The name of the package specifies the data store that that will be loaded from that package and put on the pipeline.

## Set your plugins settings

**Note**: This is totally _Optional_, the setting is here for being flexibility.

File: `settings.py`

- Settings Variable: `CASSIOPEIA_PLUGINS` or `CASSIOPEIA_PIPELINE`
- Usage: Define the plugins you want to add.
- Accepts: Dict
    > keys: Plugin name.

    > values: dict of arguments required by the plugin.

::: tip
A list of plugins is [later on the page](#plugins).
:::

## Plugins

A list of supported Plugins.

### ChampionGG

- Installing: `pip install cassiopeia-championgg`
- Description: The ChampionGG plugin pulls data from the [champion.gg api](http://api.champion.gg/). This data is accessible via the Champion.championgg attribute.
- Type of Plugin: Datastore
- Settings variable belonging: `CASSIOPEIA_PIPELINE`
- Module/Plugin name (key): `ChampionGG`
- Supports multiple instances: No.
- Object type supported: `championgg`
- Recommended placement on pipeline: Right before `RiotAPI`.

| Arguments | Accepts | Default |
| --------- | ------- | ------- | 
| `"PACKAGE"` | Name of the plugin installed: `"cassiopeia_championgg"` | No default, required to be plugged correctly |
| `"API_KEY"` | Champion.gg api key in string | `"CHAMPIONGG_KEY"` |

```python{3-6}
CASSIOPEIA_PIPELINE: {
  #...,
  "ChampionGG": {
    "PACKAGE": "cassiopeia_championgg",
    "API_KEY": os.environ["CHAMPIONGG_KEY"]
  },
  #...
}
```
::: warning
Currently `championgg` objects will not sink into `DjangoCache` nor `Omnistone`, because it's not implemented yet. Request an Issue if needed. 
:::

### Simple KV Disk Store

- Installing: `pip install cassiopeia-diskstore`
- Description: This plugin provides a disk-database. ~~It is especially useful~~ for staticdata, which never changes. See warning below.
- Type of Plugin: Datastore
- Settings variable belonging: `CASSIOPEIA_PIPELINE`
- Module/Plugin name (key): `SimpleKVDiskStore`
- Supports multiple instances: No.
- Object type supported: `cassiopeia.dto`
- Recommended placement on pipeline: Before `DDragon` and `RiotAPI`.

| Arguments | Accepts | Default |
| --------- | ------- | ------- | 
| `"PACKAGE"` | Name of the plugin installed: `"cassiopeia_diskstore"` | No default, required to be plugged correctly |
| `"PATH"` | Your absolute path to store data | Unknown, please specify to avoid errors. |
| `"EXPIRATIONS_MAP"` | Dict of expiration mapping as documented in [previous page](./pipeline.html#arguments). | The default expirations can be found in cassiopeia's [documentations](https://cassiopeia.readthedocs.io/en/latest/plugins.html#simple-kv-disk-store) |

```python{3-9}
CASSIOPEIA_PIPELINE: {
  #...,
  "SimpleKVDiskStore": {
    "PACKAGE": "cassiopeia_diskstore",
    "PATH": "/absolute/path/to/store/data/",
    "EXPIRATIONS_MAP": {
        #... expirations settings going here ...
    },
  },
  #...
}
```
::: warning
`MatchHistory` is bugged on the API side, thus to avoid unexpected results, this is not sinked into this datastore.
:::

::: warning
You should not use this datastore unless a reason is given (to yourself).
It does not automatically delete files after it is expired, which might cause memory issues in some cases.
Consider using the Filebased cache provided by Django out of the box and add it to `DjangoCache`.
:::

