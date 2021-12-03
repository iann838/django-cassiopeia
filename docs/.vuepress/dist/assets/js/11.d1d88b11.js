(window.webpackJsonp=window.webpackJsonp||[]).push([[11],{361:function(t,s,a){"use strict";a.r(s);var n=a(25),e=Object(n.a)({},(function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[a("h1",{attrs:{id:"usage"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#usage"}},[t._v("#")]),t._v(" Usage")]),t._v(" "),a("p",[t._v("Cassiopeia functions and methods:")]),t._v(" "),a("ul",[a("li",[t._v("The full documentation for the functions and methods of casiopeia can be found at "),a("a",{attrs:{href:"http://cassiopeia.readthedocs.org/en/latest/",target:"_blank",rel:"noopener noreferrer"}},[t._v("here"),a("OutboundLink")],1),t._v(".")])]),t._v(" "),a("p",[t._v("Here are some examples of a function based view that implements a basic use of the API.")]),t._v(" "),a("ul",[a("li",[a("p",[t._v("This example uses Cassiopeia interface of type "),a("code",[t._v("get_*()")]),t._v(".")]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("from")]),t._v(" django"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("shortcuts "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" render"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" HttpResponse\n\n"),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("# Import the correct cassiopeia")]),t._v("\n"),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("from")]),t._v(" django_cassiopeia "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" cassiopeia "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("as")]),t._v(" cass\n\n"),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("def")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token function"}},[t._v("summonerstats")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("request"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    context "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n    summoner "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" cass"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("get_summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("name"),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"Kalturi"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n    context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"name"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("name\n    context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"level"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("level\n    context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"region"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("region\n    "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("return")]),t._v(" render"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("request"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"your_template.html"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])])])]),t._v(" "),a("li",[a("p",[t._v("This example uses Cassiopeia interface of type "),a("code",[t._v("Object()")]),t._v(", "),a("em",[t._v("This is the preferable way of doing it")]),t._v(", because it uses Lazy loading, the call will not fire unless it is necessary to gather new information. For more information please have a look to "),a("a",{attrs:{href:"https://cassiopeia.readthedocs.io/en/latest/inner_workings.html",target:"_blank",rel:"noopener noreferrer"}},[t._v("How Cass works"),a("OutboundLink")],1),t._v(".")]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("from")]),t._v(" django"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("shortcuts "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" render"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" HttpResponse\n"),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("from")]),t._v(" django_cassiopeia "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("import")]),t._v(" cassiopeia "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("as")]),t._v(" cass\n\n"),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("def")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token function"}},[t._v("summonerstats2")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("request"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    context "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n    summoner "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" cass"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("Summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("name"),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"Kalturi"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("   "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("#This will not fire a call")]),t._v("\n    context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"name"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("name   "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("#This will neither fire a call, cuz name is already given")]),t._v("\n    context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"level"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("level   "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("#Now this fire a call to get `level`")]),t._v("\n    context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"region"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("region   "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("#This won't fire again, the object is called and loaded.")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("return")]),t._v(" render"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("request"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"your_template.html"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n\n"),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("def")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token function"}},[t._v("matchhistory")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("request"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v("\n    summoner1 "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" cass"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("Summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("name"),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"Kalturi"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n    summoner2 "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" cass"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("Summoner"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("account_id"),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"YourEncryptedAccountId"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("# This will trigger a call because MatchList needs accountId.")]),t._v("\n    history1 "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" cass"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("MatchHistory"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("summoner"),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v("summoner1"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token comment"}},[t._v("# This won't trigger a call, cuz accountId is already loaded.")]),t._v("\n    history2 "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" cass"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("MatchHistory"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("summoner"),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v("summoner2"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n    context "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"histories"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),t._v("history1"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" history2"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token keyword"}},[t._v("return")]),t._v(" render"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("(")]),t._v("request"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"your_template.html"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" context"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(")")]),t._v("\n")])])])])]),t._v(" "),a("div",{staticClass:"custom-block tip"},[a("p",{staticClass:"custom-block-title"},[t._v("TIP")]),t._v(" "),a("p",[t._v("This works very nicely with Class Based Views too, just being flexible here as the Quick Start were already using CBV.\nYou should not have any problems with Django REST Framework neither.")])])])}),[],!1,null,null,null);s.default=e.exports}}]);