import math

from configuration.symbols import SYMBOL_ERROR


def calculate_max_hr(hr_data):
    # return max value of hr data list
    return max(hr_data, key=lambda hr: hr.value).value

def calculate_min_hr(hr_data):
    # return max value of hr data list
    min_hr = min(hr_data, key=lambda hr: hr.value).value
    return min_hr

def calculate_avg_hr(hr_data):
    # return max value of hr data list
    if len(hr_data) > 0:
        total = sum(hr.value for hr in hr_data)  # Sum the values of heart rates
        count = len(hr_data)  # Get the count of heart rates
        return total / count  # Return the average
    else:
        return 0  # Return 0 if there are no heart rates

def calculate_hr_to_hr_max_percentage(hr,hr_max):
    return (hr/hr_max)*100


def calculate_resting_calories_by_minutes(gender, age, weight, height, minutes):
    resting_calories_by_minutes = (calculate_resting_calories_by_day(gender, age, weight, height)) * (minutes / 1440)
    return resting_calories_by_minutes

def calculate_resting_calories_by_day(gender, age, weight, height):
    w = 10*weight
    h = 6.25*height
    a = 5*age
    if gender.lower()=="female":
        resting_cal_by_day =   h+w+a-161
    elif gender.lower()=="male":
        resting_cal_by_day =   h+w+a+5
    else:
        raise ValueError(f"{SYMBOL_ERROR} Gender should be male or female!")

    return resting_cal_by_day

def calculate_intensity_factor(hr_max, avg_hr):
    if avg_hr > 0:
        return avg_hr/hr_max
    else:
        print("Error during intensity factor calculation!")
        return 0

def calculate_training_stress_score( duration, hr_max, avg_hr, intensity_factor):
    """Low TSS (<50): A light workout with minimal training stress. This is great for active recovery or beginner-level training.
    Moderate TSS (50–100): A standard moderate workout, usually for aerobic training. This could be a medium-effort endurance session.
    High TSS (100–150): A tough workout, potentially one where you're pushing the limits of your endurance. It could involve interval training or long-duration, high-intensity exercise.
    Very High TSS (>150): A very intense session, like a race, maximal effort, or long endurance session at or above your FTP or VO2 max."""
    if avg_hr == 0:  # Avoid division by zero
        return 0

    # print(f"%%%%%%%%%%%%%%%%%%%%%%calculating tss if: {intensity_factor}")
    duration_sec = duration.total_seconds()
    # TSS formula (using the correct placement for IF)
    tss = ((duration_sec * avg_hr * intensity_factor) / (hr_max * 3600)) * 100

    return tss

def calculate_zoladz_caloric_expenditure(avg_hr, hr_rest, hr_max, weight, duration_minutes):
    """
    Zoladz-formula
    """
    # HRR%
    hrr_percent = (avg_hr - hr_rest) / (hr_max - hr_rest)

    # Calories burnt by minutes
    calories_per_minute = (0.64 + 0.48 * hrr_percent) * weight *0.5 #0.5 azt én írtam be mert irreáis a szám

    # Sum of burnt calories
    total_calories = calories_per_minute * duration_minutes

    return total_calories

def calculate_mifflin_st_jeor_calories(avg_hr, weight, age, duration_minutes):
    # Kalória per perc
    calories_per_minute = (0.4472 * avg_hr - 0.05741 * age + 0.074 * weight + 2.21) / 4.184

    # Összes kalória
    total_calories = calories_per_minute * duration_minutes

    return total_calories

def calculate_caloric_expanditure(duration, avg_hr, age, weight, gender):
    # Keytel et al. (2005) formula
    cpm = 0
    # print(f"calculating calores for age: {age}, weithg: {weight}, avg_hr: {avg_hr}, dur: {duration}")
    if gender.lower() == "female":
        cpm = ((0.4472 * avg_hr) - (0.1263 * weight) + (0.074 * age) - 20.4022) / 4.184
        # print(f"woman calories: {cpm} by: (((0.4472*{avg_hr} +(0.1263*{weight}+(0.074*{age}-20.4022)/4.184*{duration.total_seconds()}")
    elif gender.lower() == "male":
        cpm = ((0.6309 * avg_hr) + (0.1988 * weight) + (0.2017 * age) - 55.0969) / 4.184
    else:
        raise ValueError("Gender must be 'male' or 'female'")

    # print(f"************-calculated calories: {cpm*(duration.total_seconds()/60)}")
    return cpm*(duration.total_seconds()/60)

def calculate_edward_trimp(intensity_zones):
    edward_trimp = 0
    for zone in intensity_zones:
        edward_trimp += (zone.time_spent/60)*zone.weight_factor

    return edward_trimp

def calculate_simple_banister_trimp(duration, avg_hr, gender, hrr, hr_rest):
    calculated_simple_trimp = 0
    b = 0
    if gender.lower()=="female":
        b=1.67
    elif gender.lower()=="male":
        b=1.92
    else:
        raise ValueError("Gender must be male or female")

    delta_hr = (avg_hr-hr_rest)/hrr
    y = math.exp(b*delta_hr)
    calculated_simple_trimp = (duration.total_seconds()/60)*delta_hr*y
    # print(f"{duration.total_seconds()/60} * {delta_hr} * {y}")
    return calculated_simple_trimp

def calculate_advanced_banister_trimp(duration, avg_hr, gender, hrr, hr_rest, recovery_factor_avg):
    calculated_advanced_trimp = calculate_simple_banister_trimp(duration=duration, avg_hr=avg_hr, gender=gender, hrr=hrr, hr_rest=hr_rest) * recovery_factor_avg
    return calculated_advanced_trimp

def calculate_epoc():
    return 0