# Usage

Cassiopeia functions and methods:
* The full documentation for the functions and methods of casiopeia can be found at [here](http://cassiopeia.readthedocs.org/en/latest/).

Here are some examples of a function based view that implements a basic use of the API.

* This example uses Cassiopeia interface of type `get_*()`.
    ```python
    from django.shortcuts import render, HttpResponse

    # Import the correct cassiopeia
    from django_cassiopeia import cassiopeia as cass

    def summonerstats(request):
        context = {}
        summoner = cass.get_summoner(name="Kalturi")
        context["name"] = summoner.name
        context["level"] = summoner.level
        context["region"] = summoner.region
        return render(request, "your_template.html", context)
    ```

* This example uses Cassiopeia interface of type `Object()`, *This is the preferable way of doing it*, because it uses Lazy loading, the call will not fire unless it is necessary to gather new information. For more information please have a look to [How Cass works](https://cassiopeia.readthedocs.io/en/latest/inner_workings.html).
    ```python
    from django.shortcuts import render, HttpResponse
    from django_cassiopeia import cassiopeia as cass
    
    def summonerstats2(request):
        context = {}
        summoner = cass.Summoner(name="Kalturi")   #This will not fire a call
        context["name"] = summoner.name   #This will neither fire a call, cuz name is already given
        context["level"] = summoner.level   #Now this fire a call to get `level`
        context["region"] = summoner.region   #This won't fire again, the object is called and loaded.
        return render(request, "your_template.html", context)
    
    def matchhistory(request):
        summoner1 = cass.Summoner(name="Kalturi")
        summoner2 = cass.Summoner(account_id="YourEncryptedAccountId")
        # This will trigger a call because MatchList needs accountId.
        history1 = cass.MatchHistory(summoner=summoner1)
        # This won't trigger a call, cuz accountId is already loaded.
        history2 = cass.MatchHistory(summoner=summoner2)
        context = {
            "histories": [history1, history2]
        }
        return render(request, "your_template.html", context)
    ```

::: tip
This works very nicely with Class Based Views too, just being flexible here as the Quick Start were already using CBV.
You should not have any problems with Django REST Framework neither.
:::