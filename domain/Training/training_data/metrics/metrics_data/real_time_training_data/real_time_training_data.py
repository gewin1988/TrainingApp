from domain.Training.training_data.metrics.metrics_data.base.base_training_data import BaseTrainingData


class RealTimeTrainingData(BaseTrainingData):
    def __init__(self, zone_dto_list):
        super().__init__(zones=zone_dto_list)  # Az alaposztály __init__ metódusának meghívása
        self.last_timestamp = None
        self.current_hr_to_max_hr_ratio = 0
        self.current_hr = 0
        self.current_intensity = None



    def find_nearest_zone(self, hr_value):
        """
        Find the nearest zone for a given heart rate value.
        """
        min_distance = float('inf')
        nearest_zone = None

        for zone in self.zones:
            # Calculate the distance to the lower and upper bounds of the zone
            distance_to_lower = abs(hr_value - zone.lower_bound)
            distance_to_upper = abs(hr_value - zone.upper_bound)

            # Find the minimum distance to this zone
            min_zone_distance = min(distance_to_lower, distance_to_upper)

            # Update the nearest zone if this zone is closer
            if min_zone_distance < min_distance:
                min_distance = min_zone_distance
                nearest_zone = zone

        return nearest_zone

    def update_intensity_zone(self, hr_value, timestamp, current_total_time, user):

        # print(f"intensity update called with value: {hr_value}, timestamp: {timestamp}, ctt: {current_total_time}")
        if self.last_timestamp is not None:
            # time_diff = Decimal(str((timestamp - self.last_timestamp).total_seconds()))
            time_diff = (timestamp - self.last_timestamp).total_seconds()

            max_gap = 4.0
            if time_diff > max_gap:
                print(f"Large gap detected: {time_diff} seconds. Skipping this interval.")
                self.last_timestamp = timestamp  # Reset the last timestamp
                return

            classified = False  # Track if the value was classified

            # Try to classify the heart rate value into a zone
            for zone in self.zones:
                if zone.lower_bound <= hr_value < zone.upper_bound:
                    # self.time_spent[zone]["time"] += time_diff

                    zone.update_time_spent(time_diff)
                    # if user == "Adam Forgo":
                    #     print(f"hr data: {hr_value} goes to zone {zone.name} (time: {zone.time_spent:.1f}+{time_diff:.1f}->{(zone.time_spent+time_diff):.1f}) ## {zone.lower_bound:.1f} - {zone.upper_bound:.1f}")
                    self.current_intensity = zone
                    classified = True
                    break

            # If the value was not classified, assign it to the nearest zone
            if not classified:
                nearest_zone = self.find_nearest_zone(hr_value)
                # self.time_spent[nearest_zone]["time"] += time_diff
                for zone in self.zones:
                    if zone == nearest_zone:
                        zone.update_time_spent(time_diff)
                        # if user == "Adam Forgo":
                        #     print(f"hr data: {hr_value} goes to {zone.name} (time: {zone.time_spent:.1f}+{time_diff:.1f}->{(zone.time_spent+time_diff):.1f}) ## {zone.lower_bound:.1f} - {zone.upper_bound:.1f}")
                        break
                self.current_intensity = nearest_zone

            for zone in self.zones:
                zone.update_time_percentage(current_total_time)

        self.last_timestamp = timestamp

