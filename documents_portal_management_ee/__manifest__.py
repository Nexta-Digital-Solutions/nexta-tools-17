# -*coding: utf-8 -*-
{
    "name": "Documents Portal | Portal Documents",
    "summary": """
        This module provide simple and very useful portal functionality to enterprise documents module. 
        documents  owners can see their own documents on portal also they can upload documents to odoo documents.
    """,
    "version": "17.0.1.1",
    "description": """
        This module provide simple and very useful portal functionality to enterprise documents module. 
        documents  owners can see their own documents on portal also they can upload documents to odoo documents.
        Documents Portal,
        Portal Documents,
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis.store",
    "images": ["images/documents_portal_management_ee.png"],
    "category": "Sales",
    "depends": [
        "base",
        "mail",
        "portal",
        "documents",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/documents_portal_data.xml",        
        "views/documents_portal_templates.xml",
        "views/documents_document_view.xml",
        "wizard/documents_document_export.xml",             
    ],
    "assets": {
        "web.assets_backend": [
            "documents_portal_management_ee/static/src/js/*.js",
            "documents_portal_management_ee/static/src/xml/*.xml",
        ],
    },    
    "installable": True,
    "application": True
    
}
