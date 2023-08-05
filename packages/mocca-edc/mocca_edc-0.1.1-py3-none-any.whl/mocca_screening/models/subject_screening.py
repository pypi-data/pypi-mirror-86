from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django_crypto_fields.fields import EncryptedCharField
from edc_constants.choices import YES_NO
from edc_model.models import BaseUuidModel
from edc_screening.model_mixins import ScreeningModelMixin
from edc_screening.screening_identifier import ScreeningIdentifier
from mocca_lists.models import MoccaOriginalSites

from ..eligibility import check_eligible_final
from ..mocca_original_sites import get_mocca_site_limited_to
from .mocca_register import MoccaRegister


class ScreeningIdentifier(ScreeningIdentifier):
    template = "S{random_string}"


class SubjectScreening(
    ScreeningModelMixin, BaseUuidModel,
):
    identifier_cls = ScreeningIdentifier

    screening_consent = models.CharField(
        verbose_name=(
            "Has the subject given his/her verbal consent "
            "to be screened for the MOCCA Extension trial?"
        ),
        max_length=15,
        choices=YES_NO,
    )

    mocca_site = models.ForeignKey(
        MoccaOriginalSites,
        verbose_name="Original MOCCA site",
        on_delete=models.PROTECT,
        limit_choices_to=get_mocca_site_limited_to,
    )

    mocca_participant = models.CharField(
        verbose_name="Was the patient enrolled to the original MOCCA study?",
        max_length=25,
        choices=YES_NO,
    )

    mocca_study_identifier = models.CharField(
        verbose_name="Original MOCCA study identifier",
        max_length=25,
        validators=[
            RegexValidator(
                r"0[0-9]{1}\-0[0-9]{3}|[0-9]{6}",
                "Invalid format. Expected 12-3456 for UG, 123456 for TZ",
            )
        ],
        help_text="Format must match original identifier. e.g. 12-3456 for UG, 123456 for TZ",
    )

    initials = EncryptedCharField(
        validators=[
            RegexValidator("[A-Z]{1,3}", "Invalid format"),
            MinLengthValidator(2),
            MaxLengthValidator(3),
        ],
        help_text=(
            "Use UPPERCASE letters only. May be 2 or 3 letters. "
            "Use `F`irst`L`ast or `L`ast`F`irst depending on the country custom. "
        ),
        blank=False,
    )

    birth_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2002)],
    )

    mocca_register = models.OneToOneField(
        MoccaRegister, on_delete=models.PROTECT, null=True
    )

    def save(self, *args, **kwargs):
        check_eligible_final(self)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Subject Screening"
        verbose_name_plural = "Subject Screening"
