# -*- coding: utf-8 -*-
{
    'name': "voip_calls",

    'summary': "Modificaciones para voip",

    'description': """
        Modificaciones voip
    """,

    'author': "NextaDS",
    'website': "https://www.nextads.es",
    'category': 'Uncategorized',
    'version': '17.0.0.1',
    'depends': ['base', 'voip'],
    'assets':{
         "voip.assets_sip": [
            "voip_calls/static/src/core/user_agent_service.js"
        ]
    }
}

