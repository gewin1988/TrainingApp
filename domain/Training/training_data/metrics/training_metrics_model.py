import json
from datetime import datetime, timedelta

from configuration.symbols import SYMBOL_EVENT, SYMBOL_ERROR, SYMBOL_INFO
from domain.Data.hr_data import HrData
from domain.Training.heart_rate.hr_data_model import HrDataModel
from domain.Training.training_data.calories.calories_model import CaloriesModel
from domain.Training.training_data.impulse.training_impulse_model import TrainingImpulseModel
from domain.Training.training_data.metrics.metrics_data.training_data.training_data import TrainingData

from domain.Training.training_data.metrics.training_metrics_dto import TrainingMetricsDTO
from domain.Training.zone.zone_model import ZoneModel
from domain.metric_calculator_central.metric_calculator_central import calculate_max_hr, calculate_min_hr, \
    calculate_avg_hr, calculate_simple_banister_trimp, calculate_advanced_banister_trimp, calculate_edward_trimp, \
    calculate_resting_calories_by_minutes, calculate_caloric_expanditure, calculate_training_stress_score, \
    calculate_intensity_factor, calculate_zoladz_caloric_expenditure, calculate_mifflin_st_jeor_calories, \
    calculate_epoc, calculate_hr_to_hr_max_percentage


def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj.__dict__ if hasattr(obj, '__dict__') else str(obj)


class TrainingMetricsModel:
    def __init__(self, dto, zone_dto_list):
        self.id = dto.id
        self.metrics_data = TrainingData(zone_dto_list)

    def set_start_time(self, start_time):
        self.metrics_data.current_data.last_timestamp = start_time # init value


    def handle_new_hr_data(self, data:HrData, training_start_time, user):
        self.metrics_data.current_data.current_hr = data.value
        self.metrics_data.current_data.hr_data.append(data)
        self.metrics_data.current_data.update_intensity_zone(hr_value=data.value, timestamp=data.timestamp, current_total_time=datetime.now() - training_start_time, user=user)


    def calculate_low_frequency_data(self, duration, user_name, age, gender, hr_max, hr_rest, height, weight):
        # print(f"{SYMBOL_EVENT} update low frequency data for: {user_name}")
        # calories,  intensity factor?
        avg_hr = calculate_avg_hr(self.metrics_data.current_data.hr_data)  # its calculated, but calculate it here also to make sure this is accurate for metric calculation
        if duration:
            minutes = duration.total_seconds()/60
            self.metrics_data.current_data.caloric_usage.resting_calories = calculate_resting_calories_by_minutes(age=age, gender=gender, height=height, weight=weight, minutes=minutes)
            self.metrics_data.current_data.caloric_usage.caloric_expenditure = calculate_caloric_expanditure(duration=duration, age=age, gender=gender, weight=weight, avg_hr=avg_hr)
            self.metrics_data.current_data.caloric_usage.zoladz_calories = calculate_zoladz_caloric_expenditure(avg_hr=avg_hr, hr_max=hr_max, weight=weight, hr_rest=hr_rest, duration_minutes=minutes)
            self.metrics_data.current_data.caloric_usage.mifflin_st_jeor_calories = calculate_mifflin_st_jeor_calories(avg_hr=avg_hr, duration_minutes=minutes, weight=weight, age=age)
            # print(f"Calculated low freq data: rest cal: {self.current_data.caloric_usage.resting_calories} exp: {self.current_data.caloric_usage.caloric_expenditure},"
            #       f"zoladz: {self.current_data.caloric_usage.zoladz_calories}, mifflin_jeor: {self.current_data.caloric_usage.mifflin_st_jeor_calories}")
        else:
            raise ValueError(f"{SYMBOL_ERROR} duration is None")

    def calculate_mid_frequency_data(self, user_name, duration, gender, heart_rate_reserve, resting_hr, hr_max):
        # print(f"{SYMBOL_EVENT} update mid frequency data for: {user_name}")
        #tss, training impulse
        if duration:
            avg_hr = calculate_avg_hr(self.metrics_data.current_data.hr_data) #its calculated, but calculate it here also to make sure this is accurate for metric calculation
            self.metrics_data.current_data.training_impulse.simplified_banister_trimp = calculate_simple_banister_trimp(duration = duration, gender = gender, hrr=heart_rate_reserve,
                                                                                                                        hr_rest= resting_hr, avg_hr=avg_hr)
            self.metrics_data.current_data.training_impulse.advanced_banister_trimp = calculate_advanced_banister_trimp(duration = duration, gender = gender, hrr=heart_rate_reserve,
                                                                                                                        hr_rest= resting_hr,
                                                                                                                        recovery_factor_avg=self.metrics_data.current_data.training_impulse.recovery_factor,
                                                                                                                        avg_hr=avg_hr)
            self.metrics_data.current_data.training_impulse.edwards_trimp = calculate_edward_trimp(self.metrics_data.current_data.zones)
            self.metrics_data.current_data.training_stress_score = calculate_training_stress_score(duration=duration, avg_hr=avg_hr, hr_max=hr_max,
                                                                                                   intensity_factor=calculate_intensity_factor(hr_max, avg_hr))
            # print(f"Calculated MID FREQ data: edward: {self.current_data.training_impulse.edwards_trimp}, "
            #       f"simple banister: {self.current_data.training_impulse.simplified_banister_trimp}",
            #       f"advanced banister: {self.current_data.training_impulse.advanced_banister_trimp}",
            #       f"tss: {self.current_data.training_stress_score}")

            # todo:     current intensity should send here also


        else:
            raise ValueError(f"{SYMBOL_ERROR} duration is None")

    def calculate_high_frequency_data(self, user_name, hr_max):
        # print(f"{SYMBOL_EVENT} update high frequency data for: {user_name}")

        self.metrics_data.current_data.max_hr = calculate_max_hr(self.metrics_data.current_data.hr_data)
        self.metrics_data.current_data.min_hr = calculate_min_hr(self.metrics_data.current_data.hr_data)
        self.metrics_data.avg_hr = calculate_avg_hr(self.metrics_data.current_data.hr_data)
        self.metrics_data.current_data.current_hr_to_max_hr_ratio = calculate_hr_to_hr_max_percentage(self.metrics_data.current_data.current_hr, hr_max)
        # print(
        #     f"Calculated High FREQ data: max_hr: {self.current_data.max_hr}, min_hr: {self.current_data.min_hr}, avg_hr: {self.current_data.avg_hr}")
        # intensity zones calculated on every new hr data arrival

    def calculate_post_training_data(self, user_name, duration, age, gender, weight, height, hr_max, resting_hr,
                                     heart_rate_reserve):
        # print(f"{SYMBOL_INFO} calculate post training metrics for user {user_name}")

        self.metrics_data.post_training_data = PostSessionTrainingData(person_hr_max=hr_max)
        self.metrics_data.post_training_data.zones=self.metrics_data.current_data.zones
        self.metrics_data.post_training_data.hr_data = self.metrics_data.current_data.hr_data
        self.metrics_data.post_training_data.max_hr = calculate_max_hr(self.metrics_data.post_training_data.hr_data)
        self.metrics_data.post_training_data.min_hr = calculate_min_hr(self.metrics_data.post_training_data.hr_data)
        self.metrics_data.post_training_data.avg_hr = calculate_avg_hr(self.metrics_data.post_training_data.hr_data)
        self.metrics_data.post_training_data.avg_hr = calculate_avg_hr(self.metrics_data.post_training_data.hr_data)  # its calculated, but calculate it here also to make sure this is accurate for metric calculation
        self.metrics_data.post_training_data.avg_hr_to_hr_max_ratio = calculate_hr_to_hr_max_percentage(self.metrics_data.post_training_data.avg_hr, hr_max)
        duration = timedelta(minutes=90) #todo: remove after test!!!!
        if duration:
            minutes = duration.total_seconds() / 60
            resting_calories_by_minutes = calculate_resting_calories_by_minutes(age=age,
                                                                                 gender=gender,
                                                                                 height=height,
                                                                                 weight=weight,
                                                                                 minutes=minutes)
            caloric_expenditure = calculate_caloric_expanditure(duration=duration,
                                                                age=age, gender=gender,
                                                                weight=weight,
                                                                avg_hr=self.metrics_data.post_training_data.avg_hr)
            zoladz_calories = calculate_zoladz_caloric_expenditure(avg_hr=self.metrics_data.post_training_data.avg_hr,
                                                                   hr_max=hr_max,
                                                                   weight=weight,
                                                                   hr_rest=resting_hr,
                                                                   duration_minutes=minutes)
            mifflin_st_jeor_calories = calculate_mifflin_st_jeor_calories(avg_hr=self.metrics_data.post_training_data.avg_hr,
                                                                          duration_minutes=minutes,
                                                                          weight=weight,
                                                                          age=age)
            simplified_banister_trimp = calculate_simple_banister_trimp(duration=duration, gender=gender, hrr=heart_rate_reserve,
                                                                        hr_rest=resting_hr, avg_hr=self.metrics_data.post_training_data.avg_hr)
            advanced_banister_trimp = calculate_advanced_banister_trimp(duration=duration, gender=gender, hrr=heart_rate_reserve,
                                                                        hr_rest=resting_hr,
                                                                        recovery_factor_avg=self.metrics_data.current_data.training_impulse.recovery_factor,
                                                                        avg_hr=self.metrics_data.post_training_data.avg_hr)
            edwards_trimp = calculate_edward_trimp(self.metrics_data.current_data.zones)
            intensity_factor = calculate_intensity_factor(hr_max, self.metrics_data.post_training_data.avg_hr)

            training_stress_score = calculate_training_stress_score(duration=duration, avg_hr=self.metrics_data.post_training_data.avg_hr,
                                                                    hr_max=hr_max, intensity_factor=intensity_factor)

            epoc=calculate_epoc()

            self.metrics_data.post_training_data.caloric_usage.resting_calories = resting_calories_by_minutes
            self.metrics_data.post_training_data.caloric_usage.caloric_expenditure = caloric_expenditure
            self.metrics_data.post_training_data.caloric_usage.zoladz_calories = zoladz_calories
            self.metrics_data.post_training_data.caloric_usage.mifflin_st_jeor_calories = mifflin_st_jeor_calories
            self.metrics_data.post_training_data.training_impulse.edwards_trimp = edwards_trimp
            self.metrics_data.post_training_data.training_impulse.simplified_banister_trimp = simplified_banister_trimp
            self.metrics_data.post_training_data.training_impulse.advanced_banister_trimp = advanced_banister_trimp
            self.metrics_data.post_training_data.intensity_factor = intensity_factor
            self.metrics_data.post_training_data.training_stress_score = training_stress_score
            self.metrics_data.post_training_data.epoc = epoc


        else:
            raise ValueError(f"{SYMBOL_ERROR} duration is None")

        print(f"{SYMBOL_INFO}{SYMBOL_INFO}{SYMBOL_INFO}{SYMBOL_INFO}{SYMBOL_INFO}{SYMBOL_INFO}{SYMBOL_INFO}{SYMBOL_INFO}{SYMBOL_INFO}")
        print(f"avg-hr = {self.metrics_data.post_training_data.avg_hr}")
        print(f" len of hr data = {len(self.metrics_data.post_training_data.hr_data)}")
        print(json.dumps(self.metrics_data.post_training_data.training_impulse, default=custom_serializer, indent=4))


    def to_dto(self):
        if self.metrics_data.post_training_data is None:
            raise ValueError(f"{SYMBOL_ERROR} post training data is None. Can not convert to metrics to DTO")
        else:

            new_metrics_data_dto = TrainingMetricsDTO(id=self.id, training_stress_score=self.metrics_data.post_training_data.training_stress_score,
                                                      epoc=self.metrics_data.post_training_data.epoc, caloric_expenditure = self.metrics_data.post_training_data.caloric_usage.caloric_expenditure,
                                                      resting_calories_by_day=self.metrics_data.post_training_data.caloric_usage.resting_calories,
                                                      zoladz_calories=self.metrics_data.post_training_data.caloric_usage.zoladz_calories,
                                                      mifflin_st_jeor_calories=self.metrics_data.post_training_data.caloric_usage.mifflin_st_jeor_calories,
                                                      max_hr=self.metrics_data.post_training_data.max_hr,
                                                      min_hr=self.metrics_data.post_training_data.min_hr,
                                                      avg_hr=self.metrics_data.post_training_data.avg_hr,
                                                      avg_hr_to_hr_max_ratio=self.metrics_data.post_training_data.avg_hr_to_hr_max_ratio,
                                                      intensity_factor=self.metrics_data.post_training_data.intensity_factor)
            return new_metrics_data_dto