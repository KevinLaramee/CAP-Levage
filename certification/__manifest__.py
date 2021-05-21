# -*- coding: utf-8 -*-
{
    "name": "Certification - Cap Levage",
    "summary": """
        Gestion des certifications
        pour Cap-Levage""",
    "description": """
        Gestion des certifications
    """,
    "author": "Critt-Informatique",
    "website": "https://caplevage.fr/",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Cap Levage",
    "version": "0.5",
    # any module necessary for this one to work correctly
    #'depends': ['base', 'product', 'website', 'maintenance', 'sale', 'point_of_sale', 'website_sale', 'mrp_repair', 'auth_signup'],
    "depends": [
        "base",
        "product",
        "website",
        "sale",
        "website_sale",
        "auth_signup",
        "im_livechat",
        "purchase",
        "mrp",
        "hr",
        "documents",
        "sale_management",
        "repair",
    ],
    # always loaded
    "data": [
        "views/certification.xml",
        "views/equipment.xml",
        "views/sale_views.xml",
        "views/repair_views.xml",
        "views/templates.xml",
        "views/website.xml",
        "views/web_tree_dynamic_colored_field.xml",
        "views/horodating.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        #'views/email.xml',
        # 'views/res_users.xml',
    ],
    # 'qweb': ['static/src/xml/qweb.xml'],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
