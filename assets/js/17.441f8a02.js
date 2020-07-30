(window.webpackJsonp=window.webpackJsonp||[]).push([[17],{367:function(t,s,a){"use strict";a.r(s);var e=a(25),n=Object(e.a)({},(function(){var t=this,s=t.$createElement,a=t._self._c||s;return a("ContentSlotsDistributor",{attrs:{"slot-key":t.$parent.slotKey}},[a("h1",{attrs:{id:"setup-riot-api"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#setup-riot-api"}},[t._v("#")]),t._v(" Setup Riot API")]),t._v(" "),a("p",[t._v("Configure how cassiopeia would handle calls to the Riot API.")]),t._v(" "),a("h2",{attrs:{id:"set-your-api-key"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#set-your-api-key"}},[t._v("#")]),t._v(" Set your API key")]),t._v(" "),a("p",[t._v("File: "),a("code",[t._v("settings.py")])]),t._v(" "),a("table",[a("thead",[a("tr",[a("th",[t._v("Settings variable")]),t._v(" "),a("th",[t._v("Usage")]),t._v(" "),a("th",[t._v("Accepts")]),t._v(" "),a("th",[t._v("Default")])])]),t._v(" "),a("tbody",[a("tr",[a("td",[a("code",[t._v("CASSIOPEIA_RIOT_API_KEY")])]),t._v(" "),a("td",[t._v("Assign your API key, keep them in env vars")]),t._v(" "),a("td",[t._v("Any String")]),t._v(" "),a("td",[t._v("None")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v("CASSIOPEIA_LIMITING_SHARE")])]),t._v(" "),a("td",[t._v("The sharing portion used on for request limits, typically when you have multiple servers with the same key")]),t._v(" "),a("td",[t._v("float: 0 ~ 1")]),t._v(" "),a("td",[t._v("1")])])])]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[t._v("CASSIOPEIA_RIOT_API_KEY "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" os"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(".")]),t._v("environ"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"RIOT_API_KEY"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),t._v("\nCASSIOPEIA_LIMITING_SHARE "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("1.0")]),t._v("\n")])])]),a("div",{staticClass:"custom-block tip"},[a("p",{staticClass:"custom-block-title"},[t._v("TIP")]),t._v(" "),a("p",[t._v("This is a backward uncompatible change with Django Cassipeia 1, to avoid possible future Valorant API key variable name.")])]),t._v(" "),a("div",{staticClass:"custom-block warning"},[a("p",{staticClass:"custom-block-title"},[t._v("WARNING")]),t._v(" "),a("p",[t._v("Do not use "),a("code",[t._v("set_api_key()")]),t._v(" method provided by cassiopeia.\nDo not keep your API key in "),a("code",[t._v("settings.py")]),t._v(" on production.")])]),t._v(" "),a("h2",{attrs:{id:"set-error-handler-for-the-api"}},[a("a",{staticClass:"header-anchor",attrs:{href:"#set-error-handler-for-the-api"}},[t._v("#")]),t._v(" Set Error handler for the API")]),t._v(" "),a("ul",[a("li",[a("p",[t._v("Settings variable: "),a("code",[t._v("CASSIOPEIA_API_ERROR_HANDLING")])])]),t._v(" "),a("li",[a("p",[t._v("Usage: Define the strategy used for handling error codes.")])]),t._v(" "),a("li",[a("p",[t._v("Accepts: Dict")]),t._v(" "),a("blockquote",[a("p",[t._v("keys: "),a("code",[t._v('"404"')]),t._v(","),a("code",[t._v('"500"')]),t._v(","),a("code",[t._v('"503"')]),t._v(","),a("code",[t._v('"TIMEOUT"')]),t._v(","),a("code",[t._v('"403"')]),t._v(","),a("code",[t._v('"429"')])])]),t._v(" "),a("blockquote",[a("p",[t._v("values (except "),a("code",[t._v('"429"')]),t._v(") : list ([0]: strategy used, [1..3]: strategy arguments if accepts)")])]),t._v(" "),a("blockquote",[a("p",[t._v("values ("),a("code",[t._v('"429"')]),t._v(") : dict > keys: "),a("code",[t._v('"SERVICE"')]),t._v(" (service limiter, untrackable), "),a("code",[t._v('"METHOD"')]),t._v(" (method limiter), "),a("code",[t._v('"APPLICATION"')]),t._v(" (key limiter). dict > values: list  ([0]: strategy used, [1..3]: strategy arguments if accepts)")])])])]),t._v(" "),a("table",[a("thead",[a("tr",[a("th",[t._v("Strategies([0])")]),t._v(" "),a("th",[t._v("Usage")]),t._v(" "),a("th",[t._v("Accepts([1..3])")])])]),t._v(" "),a("tbody",[a("tr",[a("td",[a("code",[t._v('"t"')])]),t._v(" "),a("td",[t._v("Throw the error")]),t._v(" "),a("td",[t._v("No arguments")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v('"^e"')])]),t._v(" "),a("td",[t._v("Exponential backoff after error")]),t._v(" "),a("td",[t._v("[1]: seconds of initial backoff, [2]: backoff factor to multiply for consecutive errors, [3]: number of retry attempts before throwing")])]),t._v(" "),a("tr",[a("td",[a("code",[t._v('"r"')])]),t._v(" "),a("td",[t._v("Retry from "),a("code",[t._v("Retry-after")]),t._v(" headers in request")]),t._v(" "),a("td",[t._v("[1]: number of retry attempts before throwing")])])])]),t._v(" "),a("div",{staticClass:"language-python extra-class"},[a("pre",{pre:!0,attrs:{class:"language-python"}},[a("code",[t._v("CASSIOPEIA_API_ERROR_HANDLING "),a("span",{pre:!0,attrs:{class:"token operator"}},[t._v("=")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"404"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"t"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"500"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"^e"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("3")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("2")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("3")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"503"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"^e"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("3")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("2")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("3")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"TIMEOUT"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"^e"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("3")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("2")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("3")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"403"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"t"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"429"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("{")]),t._v("\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"SERVICE"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"^e"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("3")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("2")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("3")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"METHOD"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"r"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("5")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n        "),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"APPLICATION"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(":")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("[")]),a("span",{pre:!0,attrs:{class:"token string"}},[t._v('"r"')]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v(" "),a("span",{pre:!0,attrs:{class:"token number"}},[t._v("5")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("]")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n    "),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v(",")]),t._v("\n"),a("span",{pre:!0,attrs:{class:"token punctuation"}},[t._v("}")]),t._v("\n")])])]),a("div",{staticClass:"custom-block tip"},[a("p",{staticClass:"custom-block-title"},[t._v("INFO")]),t._v(" "),a("p",[t._v("This is a shorten (a lot) version of the original cassiopeia "),a("code",[t._v("RiotAPI")]),t._v(" settings.")])]),t._v(" "),a("details",{staticClass:"custom-block details"},[a("summary",[t._v("Click to see details of this code.")]),t._v(" "),a("p",[t._v("Above code is read as:")]),t._v(" "),a("ul",[a("li",[a("p",[a("code",[t._v("404")]),t._v(" with strategy "),a("code",[t._v('"throw"')])])]),t._v(" "),a("li",[a("p",[a("code",[t._v("500")]),t._v(", "),a("code",[t._v("503")]),t._v(", "),a("code",[t._v("timeout")]),t._v(" with strategy "),a("code",[t._v('"exponential_backoff"')])]),t._v(" "),a("ul",[a("li",[t._v("initial backoff of 3 seconds")]),t._v(" "),a("li",[t._v("backoff factor of 2")]),t._v(" "),a("li",[t._v("max attempts of 3 times")])])]),t._v(" "),a("li",[a("p",[a("code",[t._v("429")]),t._v(" has 3 different types of handling: see above #2 argument")]),t._v(" "),a("ul",[a("li",[t._v("in "),a("code",[t._v("SERVICE")]),t._v(" limiter with strategy "),a("code",[t._v('"exponential_backoff"')]),t._v(" just like above")]),t._v(" "),a("li",[t._v("in "),a("code",[t._v("METHOD")]),t._v(" and "),a("code",[t._v("APPLICATION")]),t._v(" limiter with strategy "),a("code",[t._v('"retry_from_headers"')]),t._v(" and max attempts of 5 times")])])])])])])}),[],!1,null,null,null);s.default=n.exports}}]);