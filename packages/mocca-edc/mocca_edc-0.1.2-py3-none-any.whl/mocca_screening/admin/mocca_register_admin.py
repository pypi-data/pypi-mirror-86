from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple
from edc_model_admin import (
    ModelAdminFormInstructionsMixin,
    TemplatesModelAdminMixin,
)
from edc_model_admin.model_admin_simple_history import SimpleHistoryAdmin
from edc_sites import get_current_country
from mocca_screening.mocca_original_sites import get_mocca_sites_by_country

from ..admin_site import mocca_screening_admin
from ..forms import MoccaRegisterForm
from ..models import MoccaRegister


# class MoccaRegisterContactInline(TabularInlineMixin, admin.TabularInline):
#
#     model = MoccaRegisterContact
#     form = MoccaRegisterContactForm
#     min_num = 3


@admin.register(MoccaRegister, site=mocca_screening_admin)
class MoccaRegisterAdmin(
    TemplatesModelAdminMixin, ModelAdminFormInstructionsMixin, SimpleHistoryAdmin
):
    form = MoccaRegisterForm
    show_object_tools = True

    fieldsets = (
        [
            "Original Enrollment Data",
            {
                "fields": (
                    "report_datetime",
                    "mocca_study_identifier",
                    "mocca_screening_identifier",
                    "mocca_site",
                    "first_name",
                    "last_name",
                    "initials",
                    "gender",
                    "dob",
                    "birth_year",
                    "age_in_years",
                )
            },
        ],
        # [
        #     "Additional information",
        #     {
        #         "fields": (
        #             "age",
        #             "gender",
        #             "hiv_file_number",
        #             "hospital_number",
        #             "other_identifier",
        #         )
        #     },
        # ],
        # [
        #     "Contact information",
        #     {
        #         "fields": (
        #             "mobile_one",
        #             "mobile_one_comment",
        #             "mobile_two",
        #             "mobile_two_comment",
        #             "mobile_three",
        #             "mobile_three_comment",
        #             "comment",
        #         )
        #     },
        # ],
        audit_fieldset_tuple,
    )

    list_display = (
        "mocca_study_identifier",
        "mocca_site",
        "initials",
        "gender",
        "dob",
        "age_in_years",
        "birth_year",
    )

    list_filter = ("mocca_country", "mocca_site", "gender", "created", "modified")

    radio_fields = {
        "gender": admin.VERTICAL,
        "mocca_site": admin.VERTICAL,
    }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "mocca_site":
            sites = get_mocca_sites_by_country(country=get_current_country())
            kwargs["queryset"] = db_field.related_model.objects.filter(
                name__in=[v.name for v in sites.values()]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
