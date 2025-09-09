# -*- coding: utf-8 -*-
{
    'name': "España - Informe Fiscal Mod 420 (Islas Canarias IGIC)",
    'summary': """
        Informe Fiscal Español Mod 420 para el IGIC de las Islas Canarias (Impuesto General Indirecto Canario)""",
    'description': """
Informe Fiscal Español Mod 420 (Islas Canarias)
===============================================

Este módulo proporciona el Informe Fiscal Español oficial Mod 420 para las Islas Canarias,
que maneja el IGIC (Impuesto General Indirecto Canario) en lugar del IVA regular.

Características:
* Informe fiscal IGIC (Mod 420) con todas las secciones requeridas
* Etiquetas fiscales para la categorización adecuada
* Plantillas fiscales específicas de las Islas Canarias
* Soporte para todos los tipos de IGIC: 0%, 3%, 5%, 7%, 9.5%, 15%, 20%
* Manejo de bienes de inversión
* Soporte para operaciones de importación
* Secciones de correcciones y ajustes

Esta es una migración del módulo l10n_es de Odoo 18 para proporcionar la funcionalidad del Mod 420
en entornos de Odoo 17.
    """,
    'author': "NextaDS",
    'website': "https://www.nextads.es",
    'category': 'Accounting/Localizations/Account Charts',
    'version': '17.0.1.0.0',
    'license': 'OPL-1',
    'countries': ['es'],
    'depends': [
        'account',
        'base',
        'l10n_es',
    ],
    'data': [
        'data/account_tags.xml',
        'data/igic_tax_groups.xml',
        'data/mod420_report.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
