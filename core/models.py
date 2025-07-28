# DJANGO IMPORTS
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta
import random


class BaseModel(models.Model):
    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_createdby"
    )
    is_draft = models.BooleanField(_('Is Draft'), default=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    order = models.CharField(_("Order"), max_length=255, blank=True, null=True)
    display_order = models.CharField(
        _("Display Order"),
        max_length=255,
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(_('Is Deleted'), default=False)
    created_at = models.DateTimeField(
        _('Created At'),
        auto_now_add=True,
        null=True
    )
    update_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name=(
            "%(app_label)s_%(class)s_updated"
        )
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )
    deleted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_deleted"
    )
    deleted_at = models.DateTimeField(_('Deleted At'), blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True


class OTP(BaseModel):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=5)

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.phone} - {self.code}"


class Election(BaseModel):
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title


class Employee(BaseModel):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class Position(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    total_seats = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Candidate(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            'employee',
        )  # Optional: one-time candidacy across system

    def __str__(self):
        return self.employee.name


class Ballot(BaseModel):
    ballot_no = models.CharField(max_length=20, unique=True)
    symbol = models.CharField(max_length=50)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.ballot_no} - {self.candidate.employee.name} "
            f"for {self.position.title}"
        )

    class Meta:
        unique_together = ('candidate', 'position', 'election')
        verbose_name_plural = "Ballots"


class Vote(BaseModel):
    voter = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='voter'
    )
    ballot = models.ForeignKey(Ballot, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('voter', 'position')  # Prevent double voting

    def __str__(self):
        return (
            f"{self.voter.name} voted for "
            f"{self.ballot.candidate.employee.name} in "
            f"{self.ballot.position.title}"
        )
