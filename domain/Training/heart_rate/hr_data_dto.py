class HrDataDTO:
    def __init__(self, id, timestamp, value, training_metrics_id):
        self.id = id
        self.timestamp = timestamp
        self.value = value
        self.training_metrics_id = training_metrics_id