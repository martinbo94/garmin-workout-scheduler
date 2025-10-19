"""Workout generator - creates workouts based on program structure and week number."""
import json
from typing import Dict, List, Literal, Optional
from models import Program, DayWorkout, IntervalVariant


class WorkoutGenerator:
    """Generates workouts based on training program and week number."""

    def __init__(self, program: Program, max_heart_rate: int):
        """Initialize generator with program and max heart rate.

        Args:
            program: Training program structure
            max_heart_rate: Maximum heart rate for calculating zones
        """
        self.program = program
        self.max_hr = max_heart_rate
        self.hr_zones = self._calculate_hr_zones()

    def _calculate_hr_zones(self) -> Dict[int, Dict[str, int]]:
        """Calculate heart rate zones based on max HR.

        Returns:
            Dictionary mapping zone numbers to {min, max} HR values
        """
        zones = {}
        for i in range(1, 6):
            zone_key = f"zone_{i}"
            zone = getattr(self.program.heart_rate_zones, zone_key)
            zones[i] = {
                "min": int(self.max_hr * zone.percent_min / 100),
                "max": int(self.max_hr * zone.percent_max / 100)
            }
        return zones

    def _get_vo2max_variant(self, week_num: int, day: Literal["tuesday", "thursday"]) -> str:
        """Get VO2max variant based on week number and day.

        Logic:
        - Even weeks: Tuesday=A (4x6), Thursday=B (5x5)
        - Odd weeks: Tuesday=C (6x4), Thursday=D (4x8)

        Args:
            week_num: Week number (1-12)
            day: Which day (tuesday or thursday)

        Returns:
            Variant letter (A, B, C, or D)
        """
        if week_num % 2 == 0:  # Even weeks
            return "A" if day == "tuesday" else "B"
        else:  # Odd weeks
            return "C" if day == "tuesday" else "D"

    def _get_threshold_variant(self, week_num: int) -> str:
        """Get threshold interval variant based on week number.

        Args:
            week_num: Week number (1-12)

        Returns:
            Variant letter (A or B)
        """
        # Weeks 1-4: 3 intervals (variant A)
        # Weeks 5-12: 4 intervals (variant B)
        if week_num <= 4:
            return "A"
        return "B"

    def _get_long_run_duration(self, week_num: int) -> int:
        """Get long run duration based on periodization phase.

        Args:
            week_num: Week number (1-12)

        Returns:
            Duration in minutes
        """
        if week_num <= 4:
            return self.program.periodization.phase_1.long_run_duration_min
        elif week_num <= 8:
            return self.program.periodization.phase_2.long_run_duration_min
        else:
            return self.program.periodization.phase_3.long_run_duration_min

    def generate_day(self, day_name: str, week_num: int, sport_type_override: Optional[str] = None) -> List[Dict]:
        """Generate workout(s) for a specific day and week.

        Returns list because some days (Tuesday/Thursday) have 2 separate workouts.

        Args:
            day_name: Name of day (monday, tuesday, etc.)
            week_num: Week number (1-12)
            sport_type_override: Optional sport type to use for flexible workouts
                                 ('running', 'classic_skiing_ws', 'indoor_rowing')

        Returns:
            List of workout dictionaries ready for Garmin formatting
        """
        day_workout: DayWorkout = getattr(self.program.weekly_structure, day_name.lower())

        # Store override for use in workout generation
        self._sport_type_override = sport_type_override

        # Handle different workout types
        if day_workout.workout_type == "rest":
            return []  # Skip rest days

        elif day_workout.workout_type == "rest_or_recovery":
            return [self._generate_recovery(day_name, week_num, day_workout)]

        elif day_workout.workout_type == "easy_endurance":
            return [self._generate_easy_endurance(day_name, week_num, day_workout)]

        elif day_workout.workout_type == "vo2max_intervals_and_strength":
            # Return TWO separate workouts
            return self._generate_vo2max_with_strength(day_name, week_num, day_workout)

        elif day_workout.workout_type == "threshold_intervals":
            return [self._generate_threshold(day_name, week_num, day_workout)]

        elif day_workout.workout_type == "long_run":
            return [self._generate_long_run(day_name, week_num, day_workout)]

        return []

    def _get_sport_type(self, modality: Optional[str]) -> str:
        """Determine Garmin sport type based on modality.

        Args:
            modality: Modality string from workout

        Returns:
            Garmin sport type: 'running', 'classic_skiing_ws', 'indoor_rowing', or 'other'
        """
        # If there's an override for flexible workouts, use it
        if modality == "flexible" and hasattr(self, '_sport_type_override') and self._sport_type_override:
            return self._sport_type_override

        # Otherwise determine from modality string
        if not modality or modality == "flexible":
            return "other"

        modality_lower = modality.lower()

        if "running" in modality_lower or "treadmill" in modality_lower:
            return "running"

        # For any ski-related modality, default to classic skiing
        if "ski" in modality_lower or "roller" in modality_lower:
            return "classic_skiing_ws"

        return "other"

    def _generate_recovery(self, day_name: str, week_num: int, day_workout: DayWorkout) -> Dict:
        """Generate recovery workout structure."""
        zone = day_workout.intensity_zones[0] if day_workout.intensity_zones else 1
        return {
            "workout_name": f"Week {week_num} - {day_name} - Recovery",
            "day": day_name.capitalize(),
            "week": week_num,
            "workout_type": "rest_or_recovery",
            "sport_type": self._get_sport_type(day_workout.modality),
            "duration_min": day_workout.duration_min,
            "intensity_zone": zone,
            "hr_range": self.hr_zones[zone],
            "optional": day_workout.optional
        }

    def _generate_easy_endurance(self, day_name: str, week_num: int, day_workout: DayWorkout) -> Dict:
        """Generate easy endurance workout structure."""
        # Use _get_zone_range to span all intensity zones properly
        zones = day_workout.intensity_zones if day_workout.intensity_zones else [2]
        hr_range = self._get_zone_range(zones)

        return {
            "workout_name": f"Week {week_num} - {day_name} - Easy Endurance",
            "day": day_name.capitalize(),
            "week": week_num,
            "workout_type": "easy_endurance",
            "sport_type": self._get_sport_type(day_workout.modality),
            "duration_min": day_workout.duration_min,
            "intensity_zones": zones,
            "hr_range": hr_range,
            "modality": day_workout.modality
        }

    def _generate_vo2max_with_strength(self, day_name: str, week_num: int, day_workout: DayWorkout) -> List[Dict]:
        """Generate VO2max intervals + strength as TWO separate workouts."""
        if not day_workout.parts:
            return []

        workouts = []

        # Part 1: VO2max intervals
        interval_part = day_workout.parts[0]
        structure = interval_part.structure

        # Get the appropriate variant
        variant_letter = self._get_vo2max_variant(week_num, day_name.lower())
        variant = next(v for v in structure.main_set_variants if v.variant == variant_letter)

        workouts.append({
            "workout_name": f"Week {week_num} - {day_name} - VO2max {variant_letter}",
            "day": day_name.capitalize(),
            "week": week_num,
            "workout_type": "vo2max_intervals",
            "sport_type": self._get_sport_type(interval_part.modality),
            "variant": variant_letter,
            "warmup": {
                "duration_min": structure.warmup_duration_min,
                "hr_range": self.hr_zones[structure.warmup_intensity_zone]
            },
            "main_set": {
                "intervals": variant.intervals,
                "work_duration_min": variant.work_duration_min,
                "rest_duration_min": variant.rest_duration_min,
                "work_hr_range": self._get_typical_hr_range(structure.work_intensity_typical),
                "rest_hr_range": self._get_zone_range(structure.rest_intensity_zones)
            },
            "cooldown": {
                "duration_min": structure.cooldown_duration_min,
                "hr_range": self._get_zone_range(structure.cooldown_intensity_zones)
            }
        })

        # Part 2: Strength workout
        if len(day_workout.parts) > 1:
            strength_part = day_workout.parts[1]
            workouts.append({
                "workout_name": f"Week {week_num} - {day_name} - Strength",
                "day": day_name.capitalize(),
                "week": week_num,
                "workout_type": "strength",
                "sport_type": "other",
                "strength_type": strength_part.type,
                "duration_min": strength_part.duration_min,
                "exercises": strength_part.exercises,
                "rest_between_sets_min": strength_part.rest_between_sets_min
            })

        return workouts

    def _generate_threshold(self, day_name: str, week_num: int, day_workout: DayWorkout) -> Dict:
        """Generate threshold interval workout."""
        structure = day_workout.structure

        # Get variant based on week
        variant_letter = self._get_threshold_variant(week_num)
        variant = next(v for v in structure.main_set_variants if v.variant == variant_letter)

        return {
            "workout_name": f"Week {week_num} - {day_name} - Threshold {variant_letter}",
            "day": day_name.capitalize(),
            "week": week_num,
            "workout_type": "threshold_intervals",
            "sport_type": self._get_sport_type(day_workout.modality),
            "variant": variant_letter,
            "warmup": {
                "duration_min": structure.warmup_duration_min,
                "hr_range": self.hr_zones[structure.warmup_intensity_zone]
            },
            "main_set": {
                "intervals": variant.intervals,
                "work_duration_min": variant.work_duration_min,
                "rest_duration_min": variant.rest_duration_min,
                "work_hr_range": self._get_typical_hr_range(structure.work_intensity_typical),
                "rest_hr_range": self._get_zone_range(structure.rest_intensity_zones)
            },
            "cooldown": {
                "duration_min": structure.cooldown_duration_min,
                "hr_range": self._get_zone_range(structure.cooldown_intensity_zones)
            },
            "modality": day_workout.modality
        }

    def _generate_long_run(self, day_name: str, week_num: int, day_workout: DayWorkout) -> Dict:
        """Generate long run workout."""
        duration = self._get_long_run_duration(week_num)
        zone_range = self._get_zone_range(day_workout.intensity_zones)

        return {
            "workout_name": f"Week {week_num} - {day_name} - Long Run",
            "day": day_name.capitalize(),
            "week": week_num,
            "workout_type": "long_run",
            "sport_type": self._get_sport_type(day_workout.modality),
            "duration_min": duration,
            "hr_range": zone_range,
            "modality": day_workout.modality
        }

    def _get_typical_hr_range(self, typical_range: str) -> Dict[str, int]:
        """Convert typical HR range string to min/max values.

        Args:
            typical_range: String like "90-95" or "85-90"

        Returns:
            Dict with min and max HR values
        """
        min_pct, max_pct = map(int, typical_range.split("-"))
        return {
            "min": int(self.max_hr * min_pct / 100),
            "max": int(self.max_hr * max_pct / 100)
        }

    def _get_zone_range(self, zones: list) -> Dict[str, int]:
        """Get HR range spanning multiple zones.

        Args:
            zones: List of zone numbers

        Returns:
            Dict with min and max HR values
        """
        min_hr = min(self.hr_zones[z]["min"] for z in zones)
        max_hr = max(self.hr_zones[z]["max"] for z in zones)
        return {"min": min_hr, "max": max_hr}


def load_program(filepath: str = "program.json") -> Program:
    """Load program from JSON file.

    Args:
        filepath: Path to program JSON file

    Returns:
        Program model
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return Program(**data)
