from abc import ABC, abstractmethod


class PmReader(ABC):

    @abstractmethod
    def read_fx_rates(self, pair: str, dates: []) -> list:
        pass

    @abstractmethod
    def read_instrument_prices(self, instrument_id: int, dates: []) -> list:
        pass
