# -*- coding: utf-8 -*-
{
    'name': "Blockchain Icomunity",

    'summary': """Blockchain integration for Icomunity""",

    'description': """
    This module integrates Odoo with the Icomunity blockchain platform
    """,

    "depends": [
        "base",
        "account",
    ],

    'author': "NextaDS",
    'website': "https://www.nextads.es",
    'category': 'Uncategorized',
    'version': '17.0.0.1',
    'license': 'LGPL-3' ,

    "data": [
        "security/ir.model.access.csv",
        "views/account_move.xml",
    ],

}

