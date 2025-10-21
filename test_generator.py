"""Test script to verify workout generation without connecting to Garmin."""
from workout_generator import WorkoutGenerator, load_program
import config
import json


def test_workout_generation():
    """Test that all workouts generate correctly."""
    print("=" * 60)
    print("TESTING WORKOUT GENERATION")
    print("=" * 60)

    # Load program
    try:
        program = load_program("program.json")
        print(f"[OK] Loaded program: {program.program_name}\n")
    except Exception as e:
        print(f"[ERROR] Failed to load program: {e}")
        return False

    # Initialize generator
    max_hr = config.MAX_HEART_RATE
    generator = WorkoutGenerator(program, max_hr)
    print(f"[OK] Initialized generator with max HR: {max_hr}\n")

    # Get days from program structure
    DAYS = list(program.weekly_structure.__class__.model_fields.keys())
    week_number = 1

    print(f"Testing Week {week_number} workout generation:\n")

    total_workouts = 0
    errors = []

    for day_name in DAYS:
        print(f"{day_name.upper()}:")

        try:
            # Generate workouts
            workouts = generator.generate_day(day_name, week_number)

            if not workouts:
                print(f"  [REST DAY]\n")
                continue

            for workout in workouts:
                total_workouts += 1
                workout_name = workout.get('workout_name', 'UNNAMED')
                workout_type = workout.get('workout_type', 'unknown')
                sport_type = workout.get('sport_type', 'unknown')

                # Type indicator
                type_indicator = ""
                if workout_type == 'strength':
                    type_indicator = " [Calendar Reminder]"
                elif workout_type in ['easy_endurance', 'long_run']:
                    type_indicator = " [Calendar Reminder]"
                elif workout_type in ['vo2max_intervals', 'threshold_intervals']:
                    type_indicator = " [Structured Intervals]"

                print(f"  [OK] {workout_name}")
                print(f"       Type: {workout_type}, Sport: {sport_type}{type_indicator}")

                # Validate required fields
                required_fields = ['workout_name', 'day', 'week', 'workout_type', 'sport_type']
                missing = [f for f in required_fields if f not in workout]
                if missing:
                    error = f"Missing fields: {missing}"
                    print(f"       [ERROR] {error}")
                    errors.append(f"{day_name}: {error}")

            print()

        except Exception as e:
            error = f"Failed to generate: {e}"
            print(f"  [ERROR] {error}\n")
            errors.append(f"{day_name}: {error}")

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total workouts generated: {total_workouts}")
    print(f"Errors: {len(errors)}")

    if errors:
        print("\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("\n[OK] All workouts generated successfully!")
        print("[OK] Ready to run main.py to schedule on Garmin")
        return True


if __name__ == "__main__":
    success = test_workout_generation()
    exit(0 if success else 1)
