# Setup Riot API

Configure how cassiopeia would handle calls to the Riot API.

## Set your API key
File: `settings.py`

| Settings variable             | Usage | Accepts | Default |
| ----------------------------- | ----- | ------- | ------- |
| `CASSIOPEIA_RIOT_API_KEY` | Assign your API key, keep them in env vars | Any String | None |
| `CASSIOPEIA_LIMITING_SHARE` | The sharing portion used on for request limits, typically when you have multiple servers with the same key | float: 0 ~ 1 | 1 |

```python
CASSIOPEIA_RIOT_API_KEY = os.environ["RIOT_API_KEY"]
CASSIOPEIA_LIMITING_SHARE = 1.0
```
::: tip
This is a backward uncompatible change with Django Cassipeia 1, to avoid possible future Valorant API key variable name.
:::

::: warning
Do not use `set_api_key()` method provided by cassiopeia.
Do not keep your API key in `settings.py` on production.
:::

## Set Error handler for the API

- Settings variable: `CASSIOPEIA_API_ERROR_HANDLING`
- Usage: Define the strategy used for handling error codes.
- Accepts: Dict
    > keys: `"404"`,`"500"`,`"503"`,`"TIMEOUT"`,`"403"`,`"429"`

    > values (except `"429"`) : list ([0]: strategy used, [1..3]: strategy arguments if accepts) 
    
    > values (`"429"`) : dict > keys: `"SERVICE"` (service limiter, untrackable), `"METHOD"` (method limiter), `"APPLICATION"` (key limiter). dict > values: list  ([0]: strategy used, [1..3]: strategy arguments if accepts) 

| Strategies([0])      | Usage | Accepts([1..3]) |
| -------------------- | ----- | --------------- |
| `"t"` | Throw the error | No arguments |
| `"^e"` | Exponential backoff after error | [1]: seconds of initial backoff, [2]: backoff factor to multiply for consecutive errors, [3]: number of retry attempts before throwing |
| `"r"` | Retry from `Retry-after` headers in request | [1]: number of retry attempts before throwing |


```python
CASSIOPEIA_API_ERROR_HANDLING = {
    "404": ["t"],
    "500": ["^e", 3, 2, 3],
    "503": ["^e", 3, 2, 3],
    "TIMEOUT": ["^e", 3, 2, 3],
    "403": ["t"],
    "429": {
        "SERVICE": ["^e", 3, 2, 3],
        "METHOD": ["r", 5],
        "APPLICATION": ["r", 5],
    },
}
```
::: tip INFO
This is a shorten (a lot) version of the original cassiopeia `RiotAPI` settings.
:::

::: details Click to see details of this code.
Above code is read as:

* `404` with strategy `"throw"`

* `500`, `503`, `timeout` with strategy `"exponential_backoff"`
    - initial backoff of 3 seconds 
    - backoff factor of 2
    - max attempts of 3 times 

* `429` has 3 different types of handling: see above #2 argument
    - in `SERVICE` limiter with strategy `"exponential_backoff"` just like above
    - in `METHOD` and `APPLICATION` limiter with strategy `"retry_from_headers"` and max attempts of 5 times 
:::
