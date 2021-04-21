import datetime
import functools
from enum import Enum

from odoo import http


class GroupWebsite(Enum):
    lvl_0 = "certification.website_lvl_0"
    lvl_1 = "certification.website_lvl_1"
    lvl_2 = "certification.website_lvl_2"
    lvl_3 = "certification.website_lvl_3"


class GroupCertification(Enum):
    lvl_1 = "certification.certification_lvl_1"
    lvl_2 = "certification.certification_lvl_2"
    lvl_3 = "certification.certification_lvl_3"
    lvl_4 = "certification.certification_lvl_4"
    lvl_5 = "certification.certification_lvl_5"


def check_group(website_group_lvl_value: GroupWebsite = GroupWebsite.lvl_1):
    """
    Vérifie si le user connecté à les bons groupes
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            logged_user = http.request.env.user
            if logged_user.has_group(website_group_lvl_value.value):
                if (
                    logged_user.partner_id.date_fin_essai
                    and logged_user.partner_id.date_fin_essai
                    < datetime.datetime.now().date()
                ):
                    return http.request.render("certification.essai_depasse")
                else:
                    return function(*args, **kwargs)
            else:
                return http.request.render("cap_levage_portal.unauthorized")

        return wrapper

    return decorator


def get_logged_user_company(partner):
    result = partner
    if partner.parent_id.active:
        result = get_logged_user_company(partner.parent_id)
    return result


def partner_search_domain(partner, type_partner):
    # The child_of operator will look for records who are children or grand-children of a given record
    return [
        "&",
        "&",
        "|",
        ("id", "=", partner.id),
        ("parent_id", "child_of", partner.id),
        ("type", "=", type_partner),
        ("parent_id", "!=", None),
    ]


def agence_search_domain(partner):
    return partner_search_domain(partner, "delivery")


def equipe_search_domain(partner):
    return partner_search_domain(partner, "contact")


def materiels_equipe_possible_list(request, partner):
    partner_model = request.env["res.partner"]
    equipes_list = partner_model.search(equipe_search_domain(partner)).ids
    return equipes_list


def convert_empty_to_none(post):
    """
    Remplace les '' en None dans le dict en entrée
    :param post:
    :return:
    """
    new_post = {key: (value if value != "" else None) for (key, value) in post.items()}
    return new_post
