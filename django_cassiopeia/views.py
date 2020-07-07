from django.shortcuts import render, HttpResponse
from django_cassiopeia import cassiopeia as cass
from time import sleep
import json


# Create your views here.
def test(request):
    return render(request, "test/test.html")

def test_request(request, n):
    context = {
        "n" : n,
    }
    sleep(n/5)
    try:
        kalturi = cass.Summoner(name="Kalturi", region="NA")
        senna = cass.Champion(id=235)
        rune = cass.Rune(id=8112)
        match = cass.Match(id=3481455783)
        if n < 20:
            print(match.creation)
        elif n < 40:
            print(kalturi.profile_icon.id)
        elif n < 60:
            print(kalturi.match_history_uri)
        elif n < 80:
            print(senna.ally_tips)
        elif n < 100:
            print(rune.name)
        else:
            history = cass.MatchHistory(summoner=kalturi, begin_index=0, end_index=100)
            print(match.id for match in history)
    except:
        raise RuntimeError("Failed at request "+str(n))
    return HttpResponse(json.dumps(context), content_type="application/json")