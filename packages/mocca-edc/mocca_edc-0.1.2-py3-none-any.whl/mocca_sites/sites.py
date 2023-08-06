from django.core.management import color_style
from edc_sites.single_site import SingleSite

style = color_style()

fqdn = "mocca.clinicedc.org"

# site_id, name, **kwargs
all_sites = {
    "uganda": (
        SingleSite(
            119,
            "kisugu",
            title="Kisugu Hospital",
            country_code="ug",
            country="uganda",
            domain=f"kisugu.ug.{fqdn}",
        ),
        SingleSite(
            120,
            "kiswa",
            title="Kiswa Hospital",
            country_code="ug",
            country="uganda",
            domain=f"kiswa.ug.{fqdn}",
        ),
        SingleSite(
            121,
            "mulago",
            title="Mulago Hospital",
            country_code="ug",
            country="uganda",
            domain=f"mulago.ug.{fqdn}",
        ),
        SingleSite(
            122,
            "ndejje",
            title="Ndejje Hospital",
            country_code="ug",
            country="uganda",
            domain=f"ndejje.ug.{fqdn}",
        ),
        SingleSite(
            123,
            "wakiso",
            title="Wakiso Hospital",
            country_code="ug",
            country="uganda",
            domain=f"wakiso.ug.{fqdn}",
        ),
    ),
    "tanzania": (
        SingleSite(
            220,
            "amana",
            title="Amana Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"amana.tz.{fqdn}",
        ),
        SingleSite(
            221,
            "hindu_mandal",
            title="Hindu Mandal Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"hindu-mandal.tz.{fqdn}",
        ),
        SingleSite(
            222,
            "mkuranga",
            title="Mkuranga Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"mkuranga.tz.{fqdn}",
        ),
        SingleSite(
            240,
            "mwananyamala",
            title="Mwananyamala Hospital",
            country="tanzania",
            country_code="tz",
            domain=f"mwananyamala.tz.{fqdn}",
        ),
    ),
}
