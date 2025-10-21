# TODO - Garmin Workout Scheduler

## Items to Verify

### ✓ COMPLETED (2025-10-21)
- [x] Fixed strength workout uploads (now uses "Other" sport type with simple segments)
- [x] Fixed duplicate workout deletion (smart prefix matching on "Week X - day -")
- [x] Removed `work_intensity_typical` field (using zone ranges only)
- [x] Simplified VO2max warmup/cooldown to 10 min each
- [x] Capped all VO2max rest intervals at 2 min max
- [x] Removed exercise details from strength workouts
- [x] All workouts uploaded successfully (7/7)

### 🔍 TO VERIFY IN GARMIN CONNECT

1. **Check VO2max workouts are visible**
   - Tuesday: "Week 1 - tuesday - Vo2Max Intervals C" (ID: 1362721068)
   - Thursday: "Week 1 - thursday - Vo2Max Intervals D" (ID: 1362721102)
   - **Log shows uploaded successfully, but verify they appear in:**
     - Garmin Connect Web: Training > Workouts
     - Garmin Connect Calendar for Oct 21 and Oct 23
   - If not visible, may need to check Garmin API permissions or account sync

2. **Verify strength workouts appear correctly**
   - Tuesday/Thursday strength should show as "Other" sport type
   - Should appear in calendar for the scheduled dates
   - No complex exercise structures, just timed reminders

3. **Confirm no duplicate templates remain**
   - Check Training > Workouts library
   - Should only see latest versions of each workout
   - Old formats like "Week 1 - wednesday - Easy Endurance" should be removed

### 📋 POTENTIAL FUTURE IMPROVEMENTS

1. **Week increment automation**
   - Currently manual: edit `PROGRAM_START_DATE` in config.py
   - Could add CLI argument: `python main.py --week 2`

2. **Workout template cleanup**
   - Currently keeps current week only
   - Could add option to keep last N weeks

3. **Better error reporting**
   - Add detailed API response logging for troubleshooting
   - Save failed workouts to retry file

### 📝 NOTES

**Last successful run:** 2025-10-21
- Week 1 scheduled successfully
- 7 workouts uploaded (2 removed each day on average due to old duplicates)
- No errors

**Architecture improvements completed:**
- Fully data-driven workout generation
- All workout details in program.json
- Minimal hardcoded logic in Python
- Simple prefix matching for reliable duplicate deletion
