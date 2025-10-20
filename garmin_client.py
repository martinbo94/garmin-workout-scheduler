"""Garmin Connect client - handles authentication and workout upload."""
from typing import Dict, List, Optional
from garminconnect import Garmin, GarminConnectAuthenticationError


class GarminClient:
    """Client for interacting with Garmin Connect API."""

    def __init__(self, email: str, password: str):
        """Initialize Garmin client.

        Args:
            email: Garmin Connect email
            password: Garmin Connect password
        """
        self.email = email
        self.password = password
        self.client: Optional[Garmin] = None

    def connect(self) -> bool:
        """Authenticate with Garmin Connect.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client = Garmin(self.email, self.password)
            self.client.login()
            print("[OK] Successfully connected to Garmin Connect")
            return True
        except GarminConnectAuthenticationError as e:
            print(f"[ERROR] Authentication failed: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Connection error: {e}")
            return False

    def test_connection(self) -> bool:
        """Test Garmin Connect connection.

        Returns:
            True if connection works, False otherwise
        """
        if not self.client:
            return self.connect()

        try:
            # Simple API call to test connection
            self.client.get_user_summary(None)
            print("[OK] Connection test successful")
            return True
        except Exception as e:
            print(f"[ERROR] Connection test failed: {e}")
            return False

    def list_workouts(self, limit: int = 100, silent: bool = False) -> List[Dict]:
        """List existing workouts on Garmin Connect.

        Args:
            limit: Maximum number of workouts to retrieve (default: 100)
            silent: If True, don't print the list (default: False)

        Returns:
            List of workout dictionaries
        """
        if not self.client:
            if not self.connect():
                return []

        try:
            # Use direct API endpoint (garminconnect library's get_workouts() is broken)
            url = f"{self.client.garmin_workouts}/workouts"
            response = self.client.garth.get("connectapi", url, api=True)
            workouts = response.json()

            # Handle response format
            if isinstance(workouts, dict) and 'workouts' in workouts:
                workouts = workouts['workouts']
            elif not isinstance(workouts, list):
                workouts = []

            # Apply limit
            workouts = workouts[:limit]

            if not silent:
                print(f"\nFound {len(workouts)} workout template(s):")

                if workouts:
                    for i, workout in enumerate(workouts, 1):
                        name = workout.get('workoutName', 'Unnamed')
                        sport = workout.get('sportType', {}).get('sportTypeKey', 'unknown')
                        workout_id = workout.get('workoutId', 'N/A')
                        print(f"  {i}. {name} ({sport}) [ID: {workout_id}]")
                else:
                    print("  (No workout templates found)")

            return workouts
        except Exception as e:
            if not silent:
                print(f"[ERROR] Failed to list workouts: {e}")
            return []

    def upload_workout(self, workout_data: Dict, return_id: bool = False):
        """Upload workout to Garmin Connect.

        Args:
            workout_data: Workout dictionary from WorkoutGenerator
            return_id: If True, return workout ID instead of boolean

        Returns:
            If return_id=False: True if successful, False otherwise
            If return_id=True: workout ID if successful, None otherwise
        """
        if not self.client:
            if not self.connect():
                return None if return_id else False

        try:
            garmin_workout = self._format_for_garmin(workout_data)
            result = self.client.upload_workout(garmin_workout)
            print(f"[OK] Uploaded: {workout_data['workout_name']}")

            if return_id:
                # Extract workout ID from response
                workout_id = result.get('workoutId')
                return workout_id
            return True
        except Exception as e:
            print(f"[ERROR] Failed to upload {workout_data['workout_name']}: {e}")
            return None if return_id else False

    def get_scheduled_workouts_for_date(self, date_str: str) -> List[Dict]:
        """Get workouts scheduled for a specific date.

        Args:
            date_str: Date in format "YYYY-MM-DD"

        Returns:
            List of scheduled workout dictionaries with workoutId and scheduleId
        """
        if not self.client:
            if not self.connect():
                return []

        try:
            # Get scheduled workouts from the calendar/schedule endpoint
            # Format date for API (need to check if this works)
            url = f"{self.client.garmin_workouts}/schedule/{date_str}"
            response = self.client.garth.get("connectapi", url, api=True)
            schedules = response.json()

            # Return list of scheduled workouts
            if isinstance(schedules, list):
                return schedules
            elif isinstance(schedules, dict):
                return [schedules]
            return []
        except Exception:
            # Silently fail - this is expected if no workouts are scheduled
            return []

    def delete_workout_schedule(self, workout_id: int, date_str: str) -> bool:
        """Remove a workout from the calendar schedule (unschedule it).

        Args:
            workout_id: ID of the workout to unschedule
            date_str: Date in format "YYYY-MM-DD"

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            if not self.connect():
                return False

        try:
            # Try to delete the schedule (not the workout itself)
            url = f"{self.client.garmin_workouts}/schedule/{workout_id}"
            self.client.garth.delete("connectapi", url, api=True)
            return True
        except Exception:
            # Try alternate format with date
            try:
                url = f"{self.client.garmin_workouts}/schedule/{workout_id}/{date_str}"
                self.client.garth.delete("connectapi", url, api=True)
                return True
            except Exception:
                return False

    def delete_workout(self, workout_id: int) -> bool:
        """Delete a workout template entirely from Garmin Connect.

        Args:
            workout_id: ID of the workout template to delete

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            if not self.connect():
                return False

        try:
            url = f"{self.client.garmin_workouts}/workout/{workout_id}"
            self.client.garth.delete("connectapi", url, api=True)
            return True
        except Exception:
            return False

    def cleanup_old_workouts(self, days_threshold: int = 7) -> int:
        """Delete old workout templates that match our naming pattern.

        This helps prevent clutter by removing workout templates from previous weeks.
        Only deletes workouts with names like "Week X - Day - Type".

        Args:
            days_threshold: Delete workouts older than this many days (default: 7)

        Returns:
            Number of workouts deleted
        """
        if not self.client:
            if not self.connect():
                return 0

        try:
            from datetime import datetime, timedelta
            import re

            # Get all workouts using working API endpoint (silently)
            workouts = self.list_workouts(limit=100, silent=True)
            deleted_count = 0
            cutoff_date = datetime.now() - timedelta(days=days_threshold)

            for workout in workouts:
                workout_name = workout.get('workoutName', '')
                workout_id = workout.get('workoutId')

                # Only delete workouts that match our naming pattern
                # Pattern: "Week X - dayname - Type"
                if not re.match(r'^Week \d+ - \w+ - ', workout_name):
                    continue

                # Check if workout was created/updated before cutoff
                updated_date_str = workout.get('updated')
                if updated_date_str:
                    # Parse ISO date format
                    try:
                        # Garmin uses ISO format like "2025-10-19T12:00:00.0"
                        updated_date = datetime.fromisoformat(updated_date_str.replace('Z', '+00:00').split('.')[0])

                        if updated_date < cutoff_date:
                            if self.delete_workout(workout_id):
                                deleted_count += 1
                                print(f"  [DELETED] {workout_name}")
                    except:
                        # Skip if we can't parse the date
                        continue

            return deleted_count
        except Exception as e:
            print(f"[WARNING] Cleanup encountered error: {e}")
            return 0

    def upload_and_schedule_workout(self, workout_data: Dict, date_str: str, replace_existing: bool = True) -> bool:
        """Upload a workout and immediately schedule it to a date.

        Args:
            workout_data: Workout dictionary from WorkoutGenerator
            date_str: Date in format "YYYY-MM-DD"
            replace_existing: If True, delete any existing workouts for this date first

        Returns:
            True if both upload and schedule successful, False otherwise
        """
        # Check for existing workouts and unschedule them if requested
        if replace_existing:
            existing = self.get_scheduled_workouts_for_date(date_str)
            if existing:
                print(f"    [INFO] Found {len(existing)} existing workout(s) for {date_str}")
                for old_workout in existing:
                    old_id = old_workout.get('workoutId')
                    old_name = old_workout.get('workoutName', 'Unknown')
                    if old_id:
                        if self.delete_workout_schedule(old_id, date_str):
                            print(f"    [UNSCHEDULED] {old_name}")

        # Upload and get ID
        workout_id = self.upload_workout(workout_data, return_id=True)

        if not workout_id:
            return False

        # Schedule it
        return self.schedule_workout(workout_id, date_str)

    def schedule_workout(self, workout_id: int, date_str: str) -> bool:
        """Schedule a workout to a specific date on the calendar.

        Args:
            workout_id: ID of the uploaded workout
            date_str: Date in format "YYYY-MM-DD"

        Returns:
            True if successful, False otherwise
        """
        if not self.client:
            if not self.connect():
                return False

        try:
            # The schedule endpoint requires the date in a specific format
            url = f"{self.client.garmin_workouts}/schedule/{workout_id}"
            payload = {"date": date_str}

            # Use garth to make the API call
            self.client.garth.post("connectapi", url, json=payload, api=True)
            print(f"[OK] Scheduled workout {workout_id} for {date_str}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to schedule workout: {e}")
            return False

    def _get_garmin_sport_type(self, sport_type_key: str) -> Dict:
        """Convert sport type to Garmin sport type structure.

        Args:
            sport_type_key: Internal sport type key

        Returns:
            Garmin sport type dictionary with sportTypeId and sportTypeKey
        """
        # Map to Garmin sport type keys
        garmin_sport_key_map = {
            "running": "running",
            "treadmill_running": "running",
            "classic_skiing_ws": "cross_country_skiing_ws",
            "indoor_rowing": "indoor_rowing",
            "other": "other"
        }
        garmin_sport_key = garmin_sport_key_map.get(sport_type_key, "other")

        # Sport type IDs vary, but the key is more important for API
        sport_type_id_map = {
            "running": 1,
            "cross_country_skiing_ws": 20,
            "indoor_rowing": 15,
            "other": 0
        }
        sport_type_id = sport_type_id_map.get(garmin_sport_key, 0)

        return {
            "sportTypeId": sport_type_id,
            "sportTypeKey": garmin_sport_key,
            "displayOrder": 1
        }

    def _format_for_garmin(self, workout_data: Dict) -> Dict:
        """Convert workout data to Garmin Connect format.

        Args:
            workout_data: Workout dictionary from WorkoutGenerator

        Returns:
            Garmin-formatted workout dictionary
        """
        workout_type = workout_data.get("workout_type")
        sport_type = workout_data.get("sport_type", "other")

        # Map sport type to Garmin sport type key
        sport_type_map = {
            "running": "running",
            "treadmill_running": "running",
            "classic_skiing_ws": "cross_country_skiing_ws",
            "indoor_rowing": "indoor_rowing",
            "other": "other"
        }

        garmin_workout = {
            "workoutName": workout_data["workout_name"],
            "sportType": {"sportTypeKey": sport_type_map.get(sport_type, "other")},
            "workoutSegments": []
        }

        # Build workout segments based on workout type
        if workout_type in ["vo2max_intervals", "threshold_intervals"]:
            garmin_workout["workoutSegments"] = self._build_interval_segments(workout_data)

        elif workout_type in ["easy_endurance", "rest_or_recovery", "long_run"]:
            garmin_workout["workoutSegments"] = self._build_simple_segments(workout_data)

        elif workout_type == "strength":
            garmin_workout["workoutSegments"] = self._build_strength_segments(workout_data)

        return garmin_workout

    def _build_interval_segments(self, workout_data: Dict) -> List[Dict]:
        """Build workout segments for interval workouts.

        Args:
            workout_data: Workout data with warmup, main_set, cooldown

        Returns:
            List of Garmin workout segments
        """
        # Get sport type with proper structure
        sport_type_key = workout_data.get("sport_type", "running")
        sport_type = self._get_garmin_sport_type(sport_type_key)

        # All steps go in one segment
        all_steps = []
        step_order = 1

        # Warmup step
        warmup = workout_data.get("warmup", {})
        all_steps.append({
            "type": "ExecutableStepDTO",
            "stepOrder": step_order,
            "stepType": {
                "stepTypeId": 1,
                "stepTypeKey": "warmup",
                "displayOrder": 1
            },
            "endCondition": {
                "conditionTypeId": 2,
                "conditionTypeKey": "time",
                "displayOrder": 2,
                "displayable": True
            },
            "endConditionValue": float(warmup.get("duration_min", 15) * 60),
            "targetType": {
                "workoutTargetTypeId": 4,
                "workoutTargetTypeKey": "heart.rate.zone",
                "displayOrder": 4
            },
            "targetValueOne": float(warmup.get("hr_range", {}).get("min", 120)),
            "targetValueTwo": float(warmup.get("hr_range", {}).get("max", 140))
        })
        step_order += 1

        # Main set - repeat group
        main_set = workout_data.get("main_set", {})
        intervals = main_set.get("intervals", 4)
        work_duration = main_set.get("work_duration_min", 5)
        rest_duration = main_set.get("rest_duration_min", 2.5)
        work_hr = main_set.get("work_hr_range", {})
        rest_hr = main_set.get("rest_hr_range", {})

        # Create repeat steps
        repeat_steps = []

        # Work interval
        repeat_steps.append({
            "type": "ExecutableStepDTO",
            "stepOrder": step_order + 1,
            "childStepId": 1,
            "stepType": {
                "stepTypeId": 3,
                "stepTypeKey": "interval",
                "displayOrder": 3
            },
            "endCondition": {
                "conditionTypeId": 2,
                "conditionTypeKey": "time",
                "displayOrder": 2,
                "displayable": True
            },
            "endConditionValue": float(work_duration * 60),
            "targetType": {
                "workoutTargetTypeId": 4,
                "workoutTargetTypeKey": "heart.rate.zone",
                "displayOrder": 4
            },
            "targetValueOne": float(work_hr.get("min", 160)),
            "targetValueTwo": float(work_hr.get("max", 180))
        })

        # Recovery interval
        repeat_steps.append({
            "type": "ExecutableStepDTO",
            "stepOrder": step_order + 2,
            "childStepId": 1,
            "stepType": {
                "stepTypeId": 4,
                "stepTypeKey": "recovery",
                "displayOrder": 4
            },
            "endCondition": {
                "conditionTypeId": 2,
                "conditionTypeKey": "time",
                "displayOrder": 2,
                "displayable": True
            },
            "endConditionValue": float(rest_duration * 60),
            "targetType": {
                "workoutTargetTypeId": 4,
                "workoutTargetTypeKey": "heart.rate.zone",
                "displayOrder": 4
            },
            "targetValueOne": float(rest_hr.get("min", 110)),
            "targetValueTwo": float(rest_hr.get("max", 140))
        })

        # Add repeat group
        all_steps.append({
            "type": "RepeatGroupDTO",
            "stepOrder": step_order,
            "childStepId": 1,
            "stepType": {
                "stepTypeId": 6,
                "stepTypeKey": "repeat",
                "displayOrder": 6
            },
            "numberOfIterations": intervals,
            "smartRepeat": False,
            "workoutSteps": repeat_steps
        })
        step_order += 3

        # Cooldown step
        cooldown = workout_data.get("cooldown", {})
        all_steps.append({
            "type": "ExecutableStepDTO",
            "stepOrder": step_order,
            "stepType": {
                "stepTypeId": 2,
                "stepTypeKey": "cooldown",
                "displayOrder": 2
            },
            "endCondition": {
                "conditionTypeId": 2,
                "conditionTypeKey": "time",
                "displayOrder": 2,
                "displayable": True
            },
            "endConditionValue": float(cooldown.get("duration_min", 10) * 60),
            "targetType": {
                "workoutTargetTypeId": 4,
                "workoutTargetTypeKey": "heart.rate.zone",
                "displayOrder": 4
            },
            "targetValueOne": float(cooldown.get("hr_range", {}).get("min", 110)),
            "targetValueTwo": float(cooldown.get("hr_range", {}).get("max", 140))
        })

        return [{
            "segmentOrder": 1,
            "sportType": sport_type,
            "workoutSteps": all_steps
        }]

    def _build_simple_segments(self, workout_data: Dict) -> List[Dict]:
        """Build segments for simple duration-based workouts.

        Args:
            workout_data: Workout data with duration and HR range

        Returns:
            List of Garmin workout segments
        """
        duration_min = workout_data.get("duration_min", 30)
        hr_range = workout_data.get("hr_range", {"min": 120, "max": 140})

        # Get sport type with proper structure
        sport_type_key = workout_data.get("sport_type", "running")
        sport_type = self._get_garmin_sport_type(sport_type_key)

        return [{
            "segmentOrder": 1,
            "sportType": sport_type,
            "workoutSteps": [{
                "type": "ExecutableStepDTO",
                "stepOrder": 1,
                "stepType": {
                    "stepTypeId": 3,
                    "stepTypeKey": "interval",
                    "displayOrder": 3
                },
                "endCondition": {
                    "conditionTypeId": 2,
                    "conditionTypeKey": "time",
                    "displayOrder": 2,
                    "displayable": True
                },
                "endConditionValue": float(duration_min * 60),
                "targetType": {
                    "workoutTargetTypeId": 4,
                    "workoutTargetTypeKey": "heart.rate.zone",
                    "displayOrder": 4
                },
                "targetValueOne": float(hr_range.get("min", 120)),
                "targetValueTwo": float(hr_range.get("max", 140))
            }]
        }]

    def _build_strength_segments(self, workout_data: Dict) -> List[Dict]:
        """Build segments for strength workouts.

        Args:
            workout_data: Workout data with exercises

        Returns:
            List of Garmin workout segments
        """
        exercises = workout_data.get("exercises", [])
        segments = []
        segment_order = 1

        for exercise in exercises:
            if exercise.optional:
                continue

            # Estimate duration per set (in seconds)
            if exercise.duration_sec:
                # Parse duration_sec (e.g., "45-60" or "60")
                duration_str = str(exercise.duration_sec).split()[0]  # Remove " each side" etc
                if "-" in duration_str:
                    duration = int(duration_str.split("-")[0])
                else:
                    duration = int(duration_str)
                duration_per_set = duration
            elif exercise.reps:
                # Estimate ~3 seconds per rep
                reps_str = str(exercise.reps).split("-")[0].split()[0]  # Get first number
                reps = int(reps_str) if reps_str.isdigit() else 10
                duration_per_set = reps * 3
            else:
                duration_per_set = 30

            # Add rest time
            rest_time = int(workout_data.get("rest_between_sets_min", 2) * 60)
            total_time = (duration_per_set + rest_time) * exercise.sets

            segments.append({
                "segmentOrder": segment_order,
                "sportType": {"sportTypeKey": "strength_training"},
                "workoutSteps": [{
                    "type": "WorkoutStep",
                    "stepOrder": 1,
                    "stepType": {"stepTypeKey": "workout"},
                    "endCondition": {
                        "conditionTypeKey": "time",
                        "conditionTypeId": 2
                    },
                    "endConditionValue": total_time,
                    "targetType": {"workoutTargetTypeKey": "no.target"},
                    "description": f"{exercise.name}: {exercise.sets} sets"
                }]
            })
            segment_order += 1

        return segments
