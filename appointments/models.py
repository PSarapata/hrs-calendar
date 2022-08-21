from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Activity(models.Model):
    """
        Model describing an activity.
    """
    description=models.CharField("Short description of what the activity involves", max_length=512, blank=True)
    name=models.CharField("Activity name", max_length=128)
    price=models.OneToOneField("ActivityPrice", verbose_name="Current price", on_delete=models.SET_NULL, related_name="activity", null=True)


class ActivityPrice(models.Model):
    """
        Model representing activity price at given point in time.
    """
    effective_since=models.DateTimeField("Effective date and time (since)", default=timezone.now)  # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.DateField.auto_now_add
    effective_until=models.DateTimeField("Effective until", null=True, blank=True, default=None)
    is_archived=models.BooleanField("If in the past", default=False)
    price=models.DecimalField("Activity price", max_digits=10, decimal_places=2)
    pricelist=models.ForeignKey("PriceList", verbose_name="Effective pricelist", on_delete=models.DO_NOTHING)
    activity_id=models.ForeignKey(Activity, on_delete=models.DO_NOTHING, related_name="prices", unique=False)


class ActivitySlot(models.Model):
    """
        Model representing a lesson,
        linking a more generic Activity descriptor (e.g. 'One to one horse jumping lesson') with participants (multiple User instances).
    """
    activity=models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="slots")
    capacity=models.IntegerField("How many people is the activity meant for", default=1)
    duration=models.DurationField("Activity duration", default=timedelta(hours=1))
    end_time=models.DateTimeField("Activity end time")
    horses=models.ManyToManyField("Horse", verbose_name="Horses involved in the activity", through="HorseActivitySlot", through_fields=("slot", "horse"))
    is_archived=models.BooleanField("If in the past", default=False)
    is_full=models.BooleanField("If false, one can still sign up", default=False)
    instructor=models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons")
    participants=models.ManyToManyField(User, related_name="slots")
    price=models.DecimalField("Activity price at the time", max_digits=10, decimal_places=2)
    start_time=models.DateTimeField("Activity start time")
    venue=models.ForeignKey("Venue", verbose_name="Place of activity", on_delete=models.CASCADE, related_name="slots")


class Comment(models.Model):
    message=models.CharField("Important notes", max_length=512)
    slot=models.ForeignKey(ActivitySlot, on_delete=models.CASCADE, related_name="comments")


class Horse(models.Model):
    age=models.IntegerField("Age of the horse")
    is_available=models.BooleanField("Whether the horse is available for activities (is it healthy, etc.)", default=True)
    name=models.CharField("Name of the horse", max_length=128)
    skills=models.ManyToManyField("HorseSkill")


class HorseSkill(models.Model):
    description=models.CharField("Skill description", max_length=512, blank=True, null=True)
    name=models.CharField("Skill name", max_length=128)


class HorseActivitySlot(models.Model):
    horse=models.ForeignKey(Horse, on_delete=models.CASCADE, related_name="slots")
    slot=models.ForeignKey(ActivitySlot, on_delete=models.CASCADE, related_name="horse_slots")
    start_time=models.DateTimeField("Activity start time")
    duration=models.DurationField("Activity duration", default=timedelta(hours=1))
    end_time=models.DateTimeField("Activity end time")
    is_available=models.BooleanField("If the horse is available at given time", default=True)
    venue=models.ForeignKey(
            "Venue",
            on_delete=models.SET_NULL,
            null=True,
            default=None,
            related_name="horse_slots",
            verbose_name="Place, where horse is to be found at the time"
        )


class PriceList(models.Model):
    """
        Model representing activity prices at given point in time.
    """
    activities=models.ManyToManyField(Activity, through=ActivityPrice, through_fields=("pricelist", "activity_id"))
    effective_since=models.DateTimeField("Effective date and time (since)", default=timezone.now)  # https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.DateField.auto_now_add
    effective_until=models.DateTimeField("Effective until", null=True, blank=True)
    is_archived=models.BooleanField("If in the past", default=False)


class Venue(models.Model):
    """
        Model representing the place of activity (e.g. 'Indoor riding hall')
    """
    name=models.CharField("Venue name", max_length=248)
    capacity=models.IntegerField("Venue maximum capacity")
    is_available=models.BooleanField("Whether the venue is available", default=True)