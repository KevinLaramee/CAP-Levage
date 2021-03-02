import datetime
from enum import Enum
import functools

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
            if logged_user.has_group(
                website_group_lvl_value.value
            ):
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
