# -*- coding: utf-8 -*-
{
    "name": "cap_levage_portal",
    "summary": """
        Portail Cap-Levage
    """,
    "description": """
        Portail Cap-Levage
    """,
    "author": "E-cosi",
    "website": "https://www.e-cosi.fr",
    "category": "Uncategorized",
    "version": "0.1",
    "depends": ["base", "website", "portal", "sale", "account"],
    # always loaded
    "data": [
        "views/commons.xml",
        "views/materiel/materiels_commons.xml",
        "views/materiel/materiels_details.xml",
        "views/materiel/materiels_edition.xml",
        "views/materiel/materiels_list.xml",
        "views/agences_equipes_templates.xml",
        "views/equipe_manipulation_templates.xml",
        "views/agence_manipulation_templates.xml",
        "views/homepage_templates.xml",
        "views/unauthorized.xml",
    ],
}
