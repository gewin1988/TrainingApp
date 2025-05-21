class TrainingImpulseDTO:
    def __init__(self, id, simplified_banister_trimp, advanced_banister_trimp, edwards_trimp, metrics_id, recovery_factor):
        self.id = id
        self.simplified_banister_trimp = simplified_banister_trimp
        self.advanced_banister_trimp = advanced_banister_trimp
        self.edwards_trimp = edwards_trimp
        self.metrics_id = metrics_id
        self.recovery_factor = recovery_factor