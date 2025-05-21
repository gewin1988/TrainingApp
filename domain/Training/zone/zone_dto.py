class ZoneDTO:
    def __init__(self, id, name, description, lower_bound, upper_bound, time_spent, time_percentage, weight_factor):
        self.id = id
        self.name = name  # e.g., "Zone 1"
        self.description = description  # e.g., "Recovery"
        self.lower_bound = lower_bound  # e.g., 0.5 * hr_max
        self.upper_bound = upper_bound  # e.g., 0.6 * hr_max
        self.time_spent = time_spent  # Time spent in seconds (default 0)
        self.time_percentage = time_percentage  # Percentage of total time (default 0)
        self.weight_factor = weight_factor  # Weight factor (default 1)