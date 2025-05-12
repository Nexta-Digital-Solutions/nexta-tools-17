# Copyright 2024 NextaDS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Unique Supplier Invoice Number check Year",
    "version": "17.0.0.0.1",
    "summary": "Checks that supplier invoices are not entered twice the same year",
    "author": "NextaDS",
    "maintainer": "jbasiero@nextads.es",
    "license": "AGPL-3",
    "category": "Accounting & Finance",
    "depends": [
        "account",
        "account_invoice_supplier_ref_unique",
    ],
    "installable": True,
}
