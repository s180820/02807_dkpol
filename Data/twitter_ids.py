"""
Here's a list of the twitter id for the top 3 candidates from each of the parties with at least 5 "mandater" in "folketinget" after the 2022 election.

The list is based on  https://www.dr.dk/nyheder/politik/folketingsvalg/valgte
"""

twitter_ids = {
    "socialdemokratiet" : {
        # "mette_frederiksen" : None,
        "magnus_heunicke" : "22695562",
        "nicolai_wammen" : "2803948786",
        "mattias_tesfaye" : "546254893",
    },
    "venstre" : {
        "jakob_ellemann" : "155584627",
        "soren_gade" : "975064362359623680",
        "sophie_lohde" : "44611200",
    },
    "moderaterne" : {
        "lars_lokke" : "26201346",
        # "henrik_frandsen" : "1249019841924734977",
        # "rosa_eriksen" : "1560192117858861056",
        "jakob_engel_schmidt" : "337779051",
        "monika_rubin" : "2875249253",
    },
    "sf" : {
        "jacob_mark" : "2373406198",
        "pia_dyhr" : "65025162",
        "kirsten_andersen" : "235646319",
    },
    "danmarksdemokraterne" : {
        # "inger_stojberg" : None,
        "dennis_flydtkjær" : "531595033",
        "peter_skaarup" : "3144074691",
        "soren_espersen" : "2444718215",
    },
    "liberal_alliance" : {
        "alex_vanopslagh" : "1531564633",
        "henrik_dahl" : "2734140920",
        "ole_olesen" : "2222188479",
        # "solbjorg_jakobsen" : "1548641745264644099",
    },
    "konservative" : {
        "soren_pape" : "2712091824",
        "mette_abildgaard" : "37877392",
        "rasmus_jarlov" : "1225930531",
    },
    "enhedslisten" : {
        "pelle_dragsted" : "119879630",
        "mai_villadsen" : "4724782641",
        "rosa_lund" : "736979161",
    },
    "radikale" : {
        "martin_lidegaard" : "1070745218",
        "samira_nawa" : "92107029",
        "katrine_robsoe" : "2491403660",
    },
    "nye_borgerlige" : {
        "pernille_vermund" : "24687777",
        "lars_mathiesen" : "980721900",
        "kim_andersen" : "783935815600799744",
    },
    "alternativet" : {
        "franciska_rosenkilde" : "777113466205274112",
        "christina_olumeko" : "1324801335372488707",
        "torsten_gejl" : "2806864609",
    },
    "dansk_folkeparti" : {
        "morten_messerschmidt" : "509288627",
        "pia_kjarsgaard" : "1054640354690039809",
        "peter_kofod" : "1613378210"
    },
    "others" : {
        "Anders_Bjarklev" : "1366673620412547072",
        "Anders_Lund_Madsen" : "24790290",
        "DTU" : "294010596",
        "Michael_Kristiansen" : "1173236623",
        "Peter_Mogensen" : "1070921648",
        "Selma_Montgomery" : "1183078616139272193",
    }
}