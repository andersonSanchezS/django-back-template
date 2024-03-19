from datetime import timedelta, datetime as dt
from django.utils import timezone
# Models
from apps.misc.models import Holyday


def isWeekendOrHoliday(date):
    """Check if a given date is a weekend or a holiday."""
    return date.weekday() >= 5 or Holyday.objects.filter(day=date.day, month=date.month, year=date.year).exists()


def getNextWorkday(date):
    """Find the next workday by skipping weekends and holidays."""
    while isWeekendOrHoliday(date):
        date += timedelta(days=1)
    return date



def setWorkHours(date):
    """Set the time to 08:00 am on a given date."""
    return date.replace(hour=8, minute=0, second=0, microsecond=0)


def getWorkDay(solcotType):
    currentDate = dt.now() + timedelta(days=solcotType.days)

    # Adjust the date if it's on a weekend or holiday
    currentDate = getNextWorkday(currentDate)

    # If the current hour is outside of work hours, move to the next workday
    if not (8 <= currentDate.hour <= 17):
        currentDate  = setWorkHours(currentDate)  # Set time to 08:00 am
        currentDate += timedelta(days=1)  # Move to the next day
        currentDate  = getNextWorkday(currentDate)  # Adjust for weekend/holiday

    return timezone.make_aware(currentDate, timezone.get_current_timezone())
