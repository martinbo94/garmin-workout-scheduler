"""Main script to generate and upload weekly workouts to Garmin Connect."""
import os
from dotenv import load_dotenv
from workout_generator import WorkoutGenerator, load_program
from garmin_client import GarminClient
import config


def main():
    """Generate and upload workouts for current week."""
    # Load environment variables
    load_dotenv(override=True)

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email or not password:
        print("✗ Error: GARMIN_EMAIL and GARMIN_PASSWORD must be set in .env file")
        return

    # Configuration
    week_number = config.get_current_week()
    max_hr = config.MAX_HEART_RATE
    DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    print(f"\n{'='*60}")
    print(f"Generating workouts for Week {week_number}")
    if config.PROGRAM_START_DATE:
        print(f"Program started: {config.PROGRAM_START_DATE}")
    else:
        print(f"Program start date not set - using current week as week 1")
        print(f"Tip: Set PROGRAM_START_DATE in config.py to track weeks automatically")
    print(f"Max Heart Rate: {max_hr} bpm")
    print(f"{'='*60}\n")

    # Load program
    try:
        program = load_program("program.json")
        print(f"✓ Loaded program: {program.program_name}")
    except Exception as e:
        print(f"✗ Failed to load program: {e}")
        return

    # Initialize generator
    generator = WorkoutGenerator(program, max_hr)
    print(f"✓ Calculated heart rate zones:")
    for zone_num, zone_values in generator.hr_zones.items():
        zone_name = getattr(program.heart_rate_zones, f"zone_{zone_num}").name
        print(f"  Zone {zone_num} ({zone_name}): {zone_values['min']}-{zone_values['max']} bpm")

    # Initialize Garmin client
    print(f"\n{'='*60}")
    print("Connecting to Garmin Connect...")
    print(f"{'='*60}\n")

    client = GarminClient(email, password)
    if not client.connect():
        print("\n✗ Failed to connect to Garmin Connect. Please check your credentials.")
        return

    # Generate and upload workouts
    print(f"\n{'='*60}")
    print(f"Generating and uploading workouts...")
    print(f"{'='*60}\n")

    total_workouts = 0
    successful_uploads = 0

    for day in DAYS:
        print(f"\n{day.upper()}:")
        workouts = generator.generate_day(day, week_number)

        for workout in workouts:
            total_workouts += 1
            print(f"  Generating: {workout['workout_name']}")

            if client.upload_workout(workout):
                successful_uploads += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary")
    print(f"{'='*60}")
    print(f"Total workouts generated: {total_workouts}")
    print(f"Successfully uploaded: {successful_uploads}")
    print(f"Failed: {total_workouts - successful_uploads}")
    print(f"{'='*60}\n")


def test_connection():
    """Test Garmin Connect connection."""
    load_dotenv(override=True)

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email or not password:
        print("✗ Error: GARMIN_EMAIL and GARMIN_PASSWORD must be set in .env file")
        return

    print("\nTesting Garmin Connect connection...")
    client = GarminClient(email, password)

    if client.test_connection():
        print("\n✓ Connection test successful!")
        print("\nFetching recent workouts...")
        client.list_workouts(5)
    else:
        print("\n✗ Connection test failed.")


def list_workouts():
    """List recent workouts from Garmin Connect."""
    load_dotenv(override=True)

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email or not password:
        print("[ERROR] GARMIN_EMAIL and GARMIN_PASSWORD must be set in .env file")
        return

    client = GarminClient(email, password)
    client.list_workouts(10)


def schedule_current_week():
    """Schedule workouts for the current week only with automatic cleanup."""
    load_dotenv(override=True)
    from datetime import datetime, timedelta

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email or not password:
        print("✗ Error: GARMIN_EMAIL and GARMIN_PASSWORD must be set in .env file")
        return

    # Configuration
    DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    # Get current week number from config
    week_number = config.get_current_week()

    # Calculate Monday of current week
    today = datetime.now()
    days_since_monday = today.weekday()  # 0 = Monday, 6 = Sunday
    monday_this_week = today - timedelta(days=days_since_monday)

    print(f"\n{'='*60}")
    print(f"SCHEDULING CURRENT WEEK")
    print(f"{'='*60}")
    print(f"Week {week_number} of training program")
    print(f"Monday: {monday_this_week.strftime('%A, %B %d, %Y')}")
    print(f"{'='*60}\n")

    # Load program
    try:
        program = load_program("program.json")
        print(f"✓ Loaded program: {program.program_name}")
    except Exception as e:
        print(f"✗ Failed to load program: {e}")
        return

    # Initialize generator
    max_hr = config.MAX_HEART_RATE
    generator = WorkoutGenerator(program, max_hr)

    # Connect to Garmin
    print(f"\nConnecting to Garmin Connect...")
    client = GarminClient(email, password)
    if not client.connect():
        print("\n✗ Failed to connect to Garmin Connect")
        return

    # Cleanup old workouts first
    print(f"\n{'='*60}")
    print("CLEANING UP OLD WORKOUTS")
    print(f"{'='*60}")
    deleted_count = client.cleanup_old_workouts(days_threshold=7)
    if deleted_count > 0:
        print(f"✓ Removed {deleted_count} old workout template(s)")
    else:
        print("✓ No old workouts to clean up")

    # Prompt for modality choices for flexible days
    print(f"\n{'='*60}")
    print("CHOOSE MODALITIES FOR THIS WEEK")
    print(f"{'='*60}")
    print("Select workout type for flexible endurance/long run days:\n")

    modality_choices = {}
    for day_name in ['wednesday', 'saturday', 'sunday']:
        print(f"{day_name.upper()}:")
        print(f"  1) Ski erg (indoor rowing)")
        print(f"  2) Roller ski / Classic skiing")
        print(f"  3) Running")
        choice = input(f"  Enter choice (1-3): ").strip()

        if choice == '1':
            modality_choices[day_name] = 'indoor_rowing'
        elif choice == '2':
            modality_choices[day_name] = 'classic_skiing_ws'
        elif choice == '3':
            modality_choices[day_name] = 'running'
        else:
            print(f"  Invalid choice, defaulting to roller ski")
            modality_choices[day_name] = 'classic_skiing_ws'
        print()

    # Generate and schedule workouts
    print(f"\n{'='*60}")
    print(f"GENERATING & SCHEDULING WORKOUTS")
    print(f"{'='*60}\n")

    total_workouts = 0
    successful_uploads = 0

    for day_index, day_name in enumerate(DAYS):
        workout_date = monday_this_week + timedelta(days=day_index)
        date_str = workout_date.strftime("%Y-%m-%d")

        print(f"{day_name.upper()} ({workout_date.strftime('%b %d')}):")

        # Get sport type override if this is a flexible day
        sport_type_override = modality_choices.get(day_name)

        # Generate workouts for this day
        workouts = generator.generate_day(day_name, week_number, sport_type_override)

        if not workouts:
            print(f"  [REST DAY]\n")
            continue

        for workout in workouts:
            # Skip strength workouts (we don't need them on watch)
            if workout.get('workout_type') == 'strength':
                print(f"  {workout['workout_name']} - [SKIPPED - Strength workout]")
                continue

            total_workouts += 1
            workout_name = workout['workout_name']
            print(f"  {workout_name}")

            # Upload and schedule
            if client.upload_and_schedule_workout(workout, date_str):
                successful_uploads += 1
                print(f"    ✓ Scheduled for {date_str}")
            else:
                print(f"    ✗ Failed to schedule")

        print()

    # Summary
    print(f"{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total workouts: {total_workouts}")
    print(f"Successfully scheduled: {successful_uploads}")
    print(f"Failed: {total_workouts - successful_uploads}")
    print(f"{'='*60}")
    print(f"\n✓ Week {week_number} is now scheduled on your Garmin!")
    print(f"✓ Check Garmin Connect: Training > Calendar")
    print(f"✓ Your watch will suggest these workouts automatically")
    print(f"   when you start the matching activity type.")
    print(f"\n💡 Tip: Run this script again next week to schedule Week {week_number + 1}")
    print(f"{'='*60}\n")


def schedule_training_plan():
    """Upload and schedule all workouts for multiple weeks as a training plan."""
    load_dotenv(override=True)
    from datetime import datetime, timedelta

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email or not password:
        print("[ERROR] GARMIN_EMAIL and GARMIN_PASSWORD must be set in .env file")
        return

    # Configuration
    DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    # Ask user how many weeks to schedule
    num_weeks = int(input("\nHow many weeks to schedule? (1-12): "))
    if num_weeks < 1 or num_weeks > 12:
        print("[ERROR] Please enter a number between 1 and 12")
        return

    # Get start date (must be a Monday)
    start_date_input = input(f"\nStart date (YYYY-MM-DD) or press Enter for next Monday: ").strip()

    if start_date_input:
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
        # IMPORTANT: Ensure it's a Monday (day 0)
        if start_date.weekday() != 0:
            print(f"\n[WARNING] {start_date.strftime('%Y-%m-%d')} is a {start_date.strftime('%A')}, not Monday!")
            # Adjust to the Monday of that week
            days_since_monday = start_date.weekday()
            start_date = start_date - timedelta(days=days_since_monday)
            print(f"Adjusted to Monday: {start_date.strftime('%A, %B %d, %Y')}")
    else:
        # Default to next Monday
        today = datetime.now()
        # Calculate days until next Monday (0 = Monday)
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            # If today is Monday, use next Monday
            days_until_monday = 7
        start_date = today + timedelta(days=days_until_monday)

    print(f"\n{'='*60}")
    print(f"SCHEDULING TRAINING PLAN")
    print(f"{'='*60}")
    print(f"Start date: {start_date.strftime('%A, %B %d, %Y')}")
    print(f"Duration: {num_weeks} weeks")
    print(f"Total days: {num_weeks * 7}")
    print(f"{'='*60}\n")

    # Load program
    try:
        program = load_program("program.json")
        print(f"[OK] Loaded program: {program.program_name}")
    except Exception as e:
        print(f"[ERROR] Failed to load program: {e}")
        return

    # Initialize generator
    max_hr = config.MAX_HEART_RATE
    generator = WorkoutGenerator(program, max_hr)

    # Connect to Garmin
    print(f"\nConnecting to Garmin Connect...")
    client = GarminClient(email, password)
    if not client.connect():
        print("\n[ERROR] Failed to connect to Garmin Connect")
        return

    print()

    # Generate and schedule workouts
    total_workouts = 0
    successful_uploads = 0

    for week in range(1, num_weeks + 1):
        print(f"\n{'='*60}")
        print(f"WEEK {week}")
        print(f"{'='*60}")

        for day_index, day_name in enumerate(DAYS):
            # Calculate date for this day
            days_offset = (week - 1) * 7 + day_index
            workout_date = start_date + timedelta(days=days_offset)
            date_str = workout_date.strftime("%Y-%m-%d")

            print(f"\n{day_name.upper()} ({workout_date.strftime('%b %d')})")

            # Check if this day has flexible workouts that need modality selection
            sport_type_override = None
            if day_name in ['wednesday', 'saturday', 'sunday']:
                print(f"  Choose modality for {day_name.capitalize()}:")
                print(f"    1) Ski erg (indoor)")
                print(f"    2) Roller ski (outdoor)")
                print(f"    3) Running")
                choice = input(f"  Enter choice (1-3): ").strip()

                if choice == '1':
                    sport_type_override = 'indoor_rowing'
                elif choice == '2':
                    sport_type_override = 'classic_skiing_ws'
                elif choice == '3':
                    sport_type_override = 'running'
                else:
                    print(f"    Invalid choice, defaulting to roller ski")
                    sport_type_override = 'classic_skiing_ws'

            # Generate workouts for this day
            workouts = generator.generate_day(day_name, week, sport_type_override)

            for workout in workouts:
                # Skip strength workouts (we don't need them on watch)
                if workout.get('workout_type') == 'strength':
                    print(f"  {workout['workout_name']} - [SKIPPED - Strength workout]")
                    continue

                total_workouts += 1
                workout_name = workout['workout_name']
                print(f"  {workout_name}")

                # Upload and schedule
                if client.upload_and_schedule_workout(workout, date_str):
                    successful_uploads += 1
                    print(f"    [OK] Scheduled for {date_str}")
                else:
                    print(f"    [FAILED]")

    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total workouts: {total_workouts}")
    print(f"Successfully uploaded & scheduled: {successful_uploads}")
    print(f"Failed: {total_workouts - successful_uploads}")
    print(f"{'='*60}")
    print(f"\nYour {num_weeks}-week training plan is now scheduled!")
    print(f"Check Garmin Connect: Training > Calendar")
    print(f"\nNote: If you had existing workouts scheduled, you may see")
    print(f"duplicates. You can delete old ones from the Garmin Connect app")
    print(f"by swiping left on a workout in the calendar view.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    # Uncomment the function you want to run:

    # main()  # Generate and upload workouts for the week (old method)
    # test_connection()  # Test Garmin connection
    # list_workouts()  # List existing workouts
    schedule_current_week()  # Schedule current week with automatic cleanup (recommended)
    # schedule_training_plan()  # Upload and schedule multi-week training plan
