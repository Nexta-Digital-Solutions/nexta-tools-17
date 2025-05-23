# Copyright 2016 Acsone
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Unique Supplier Invoice Number in Invoice",
    "version": "17.0.1.0.0",
    "summary": "Checks that supplier invoices are not entered twice",
    "author": "Savoir-faire Linux, Acsone SA/NV, Odoo Community Association (OCA)",
    "maintainer": "Savoir-faire Linux",
    "website": "https://github.com/OCA/account-invoicing",
    "license": "AGPL-3",
    "category": "Accounting & Finance",
    "depends": ["account"],
    "data": ["views/account_move.xml", "views/res_config_settings.xml"],
    "installable": True,
}
