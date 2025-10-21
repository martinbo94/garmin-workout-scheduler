"""Configuration for training program."""
from datetime import datetime, timedelta

# Heart rate
MAX_HEART_RATE = 212

# Program start date (Monday of week 1)
# Format: "YYYY-MM-DD"
PROGRAM_START_DATE = "2025-10-19"

# Sport type options are no longer needed - workouts are now hardcoded
# Wednesday & Sunday: running (calendar reminders only)
# Saturday: ski_erg (mapped to cardio in Garmin API)


def get_current_week() -> int:
    """Calculate current week number based on start date.

    Returns:
        Week number (1-N where N is program.duration_weeks)
    """
    if PROGRAM_START_DATE is None:
        # If no start date set, use current week as week 1
        return 1

    start_date = datetime.strptime(PROGRAM_START_DATE, "%Y-%m-%d")
    today = datetime.now()

    # Calculate weeks elapsed since start
    days_elapsed = (today - start_date).days
    weeks_elapsed = days_elapsed // 7

    # Week number (cycles based on program duration - default 12)
    # Note: This assumes 12-week cycle. For dynamic cycling, load program.duration_weeks
    week_num = (weeks_elapsed % 12) + 1

    return week_num


def get_monday_of_current_week() -> str:
    """Get the Monday of current week.

    Returns:
        Date string in YYYY-MM-DD format
    """
    today = datetime.now()
    # Calculate days since Monday (0 = Monday, 6 = Sunday)
    days_since_monday = today.weekday()
    # Get the Monday of this week
    monday = today - timedelta(days=days_since_monday)
    return monday.strftime("%Y-%m-%d")
