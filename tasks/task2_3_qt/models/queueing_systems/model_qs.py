class FiniteStateModelQS:
    def __init__(self,
                 state_probabilities: list[float],
                 arrival_rate,
                 channel_count: int,
                 queue_length: int | None,
                 source_limit: int | None):
        if queue_length is None and source_limit is None:
            raise ValueError("Бесконечное количество состояний")
        if queue_length is not None and len(state_probabilities) != channel_count + queue_length + 1:
            raise ValueError("Наебал с количеством вероятностей")
        self._state_probabilities = state_probabilities
        self.channel_count = channel_count
        self.queue_length = queue_length
        self.source_limit = source_limit
        self.arrival_rate = arrival_rate

    def state_probability(self, state: int):
        return self._state_probabilities[state]

    def queue_loading(self):
        result = 0
        for j in range(len(self._state_probabilities)):
            result += self._state_queue_fullness(state=j) * self._state_probabilities[j]
        return result

    def channels_loading(self):
        result = 0
        for j in range(len(self._state_probabilities)):
            result += self._state_channels_fullness(state=j) * self._state_probabilities[j]
        return result

    def system_loading(self):
        return self.queue_loading() + self.channels_loading()

    def queue_average_time(self):
        result = self.queue_loading() / self.arrival_rate
        if self.source_limit is not None:
            result /= self.source_limit - self.system_loading()
        return result

    def system_average_time(self):
        result = self.system_loading() / self.arrival_rate
        if self.source_limit is not None:
            result /= self.source_limit - self.system_loading()
        return result

    def _state_channels_fullness(self, state: int):
        if state < self.channel_count:
            return state
        else:
            return self.channel_count

    def _state_queue_fullness(self, state: int):
        if state <= self.channel_count:
            return 0
        else:
            return state - self.channel_count
