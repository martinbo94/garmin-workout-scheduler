"""Pydantic models for training program and workout data."""
from typing import Optional, Literal, List
from pydantic import BaseModel, Field


class HeartRateZone(BaseModel):
    """Heart rate zone definition."""
    name: str
    percent_min: int
    percent_max: int
    description: str


class HeartRateZones(BaseModel):
    """All heart rate zones."""
    zone_1: HeartRateZone
    zone_2: HeartRateZone
    zone_3: HeartRateZone
    zone_4: HeartRateZone
    zone_5: HeartRateZone


class Exercise(BaseModel):
    """Strength training exercise."""
    name: str
    sets: int
    reps: Optional[str] = None
    duration_sec: Optional[str] = None
    optional: bool = False


class IntervalVariant(BaseModel):
    """VO2max interval variant structure."""
    variant: Literal["A", "B", "C", "D"]
    intervals: int
    work_duration_min: float
    rest_duration_min: float


class IntervalStructure(BaseModel):
    """Structure for interval workouts."""
    warmup_duration_min: int
    warmup_intensity_zone: int
    main_set_variants: List[IntervalVariant]
    work_intensity_zones: List[int]  # e.g., [4, 5] for VO2max, [3, 4] for threshold
    rest_intensity_zones: List[int]
    cooldown_duration_min: int
    cooldown_intensity_zones: List[int]


class WorkoutPart(BaseModel):
    """Part of a multi-part workout."""
    part: int
    type: str
    modality: Optional[str] = None
    duration_min: Optional[int] = None
    structure: Optional[IntervalStructure] = None
    exercises: Optional[List[Exercise]] = None
    rest_between_sets_min: Optional[float] = None
    note: Optional[str] = None


class DayWorkout(BaseModel):
    """Single day's workout."""
    workout_type: str
    duration_min: Optional[int] = None
    duration_display: Optional[str] = None  # e.g., "45-60min" for flexible duration
    intensity_zones: Optional[List[int]] = None
    intensity_percent_max_hr: Optional[str] = None
    modality: Optional[str] = None
    optional: bool = False
    parts: Optional[List[WorkoutPart]] = None
    structure: Optional[IntervalStructure] = None


class WeeklyStructure(BaseModel):
    """Weekly workout structure."""
    monday: DayWorkout
    tuesday: DayWorkout
    wednesday: DayWorkout
    thursday: DayWorkout
    friday: DayWorkout
    saturday: DayWorkout
    sunday: DayWorkout


class PeriodizationPhase(BaseModel):
    """Periodization phase configuration."""
    weeks: str
    name: str
    vo2max_variants: List[str]
    threshold_intervals: int
    long_run_duration_min: int
    note: Optional[str] = None


class Periodization(BaseModel):
    """Periodization structure."""
    phase_1: PeriodizationPhase
    phase_2: PeriodizationPhase
    phase_3: PeriodizationPhase
    recovery_weeks: List[int]


class Program(BaseModel):
    """Complete training program."""
    program_name: str
    duration_weeks: int
    weekly_structure: WeeklyStructure
    periodization: Periodization
    heart_rate_zones: HeartRateZones
