from django.core.validators import (
    RegexValidator,
    MinLengthValidator,
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import Index, PROTECT, UniqueConstraint
from django_crypto_fields.fields import (
    EncryptedCharField,
    FirstnameField,
    LastnameField,
)
from edc_constants.choices import ALIVE_DEAD_UNKNOWN, GENDER, YES_NO
from edc_constants.constants import NO, UNKNOWN
from edc_model.models import BaseUuidModel
from edc_sites import get_current_country
from edc_utils import get_utcnow
from mocca_lists.models import MoccaOriginalSites

from ..mocca_original_sites import get_mocca_site_limited_to


class MoccaRegister(BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    mocca_screening_identifier = models.CharField(
        verbose_name="MOCCA (original) screening identifier",
        max_length=15,
        null=True,
        blank=True,
        help_text="If known",
    )

    mocca_study_identifier = models.CharField(
        verbose_name="MOCCA (original) study identifier",
        max_length=25,
        validators=[
            RegexValidator(
                r"0[0-9]{1}\-0[0-9]{3}|[0-9]{6}",
                "Invalid format. Expected 12-3456 for UG, 123456 for TZ",
            )
        ],
        help_text="Format must match original identifier. e.g. 12-3456 for UG, 123456 for TZ",
    )

    mocca_country = models.CharField(
        max_length=25, choices=(("uganda", "Uganda"), ("tanzania", "Tanzania"))
    )

    mocca_site = models.ForeignKey(
        MoccaOriginalSites,
        on_delete=models.PROTECT,
        limit_choices_to=get_mocca_site_limited_to,
    )

    first_name = FirstnameField(null=True)

    last_name = LastnameField(null=True)

    initials = EncryptedCharField(
        validators=[
            RegexValidator("[A-Z]{1,3}", "Invalid format"),
            MinLengthValidator(2),
            MaxLengthValidator(3),
        ],
        help_text="Use UPPERCASE letters only. May be 2 or 3 letters.",
        blank=False,
    )
    gender = models.CharField(max_length=10, choices=GENDER)

    age_in_years = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(110)], null=True
    )

    birth_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2002)], null=True,
    )
    dob = models.DateField(null=True, blank=True)

    survival_status = models.CharField(
        max_length=25, choices=ALIVE_DEAD_UNKNOWN, default=UNKNOWN
    )

    def __str__(self):
        return self.mocca_study_identifier

    def save(self, *args, **kwargs):
        self.mocca_country = get_current_country()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "MOCCA Patient Register"
        verbose_name_plural = "MOCCA Patient Register"
        ordering = ["mocca_country", "mocca_site"]
        indexes = [
            Index(fields=["mocca_country", "mocca_site"]),
            Index(fields=["mocca_study_identifier", "initials", "gender"]),
        ]
        constraints = [
            UniqueConstraint(
                fields=["mocca_screening_identifier"],
                name="unique_mocca_screening_identifier",
            ),
            UniqueConstraint(
                fields=["mocca_study_identifier"], name="unique_mocca_study_identifier"
            ),
            UniqueConstraint(
                fields=["first_name", "last_name"], name="unique_first_name__last_name"
            ),
        ]


# class MoccaRegisterContact(BaseUuidModel):
#
#     mocca_register = models.ForeignKey(MoccaRegister, on_delete=PROTECT)
#
#     report_datetime = models.DateTimeField(default=get_utcnow)
#
#     contact_number = models.CharField()
#
#     contacted = models.CharField(max_length=15, choices=YES_NO, default=NO)
#
#     survival_status = models.CharField(
#         max_length=15, choices=ALIVE_DEAD_UNKNOWN, null=True
#     )
#
#     willing_to_attend = models.CharField(max_length=15, choices=YES_NO, null=True)
#
#     call_again = models.CharField(max_length=15, choices=YES_NO)
#
#     notes = models.TextField()
#
#     class Meta:
#         verbose_name = "MOCCA Patient Register Contact"
#         verbose_name_plural = "MOCCA Patient Register Contacts"
