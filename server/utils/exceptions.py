from abc import ABC, abstractproperty


class HandledException(ABC, Exception):
    @abstractproperty
    def message(self) -> str:
        pass

    @abstractproperty
    def status_code(self) -> int:
        pass
