from domain.Training.zone.zone_dto import ZoneDTO


class ZoneModel:

    def __init__(self, id, name, description, lower_bound, upper_bound, weight_factor):
        self.id = id
        self.name = name  # e.g., "Zone 1"
        self.description = description  # e.g., "Recovery"
        self.lower_bound = lower_bound  # e.g., 0.5 * hr_max
        self.upper_bound = upper_bound  # e.g., 0.6 * hr_max
        self.time_spent = 0.0  # Time spent in seconds (default 0)
        self.time_percentage = 0.0  # Percentage of total time (default 0)
        self.weight_factor = weight_factor  # Weight factor (default 1)

    def __str__(self):
        return f"Name: {self.name}, Desc:{self.description}, {self.lower_bound} - {self.upper_bound}, time:{self.time_spent}, %:{self.time_percentage}, weight factor:{self.weight_factor}"

    def to_dto(self):
        return ZoneDTO(id=self.id, name=self.name, description=self.description, lower_bound=self.lower_bound, upper_bound=self.upper_bound, time_spent=self.time_spent,
                       time_percentage=self.time_percentage, weight_factor=self.weight_factor)

    def update_time_spent(self, time_in_seconds):
        """Update the time spent in this zone."""
        prev_time = self.time_spent
        self.time_spent += time_in_seconds
        # print(f"Update time spent in {self.name}: {prev_time:.3f} + {time_in_seconds:.3f} = {self.time_spent:.3f}")

    def update_time_percentage(self, total_time):
        """Update the percentage of time spent in this zone relative to total time."""
        # (zone_data["time"] / (current_total_time.total_seconds())) * 100 if current_total_time.total_seconds() > 0 else 0
        self.time_percentage = (self.time_spent / (total_time.total_seconds()))*100 if total_time.total_seconds() > 0 else 0

    def __eq__(self, other):
        """Check if two zones are equal based on their bounds."""
        if not isinstance(other, ZoneModel):
            return False
        return (self.lower_bound == other.lower_bound and
                self.upper_bound == other.upper_bound ) and (self.name == other.name)

