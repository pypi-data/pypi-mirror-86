import abc

import System
import System.Runtime.ConstrainedExecution


class Consistency(System.Enum):
    """This class has no documentation."""

    MayCorruptProcess = 0

    MayCorruptAppDomain = 1

    MayCorruptInstance = 2

    WillNotCorruptState = 3


class Cer(System.Enum):
    """This class has no documentation."""

    # Cannot convert to Python: None = 0

    MayFail = 1

    Success = 2


class ReliabilityContractAttribute(System.Attribute):
    """This class has no documentation."""

    @property
    def ConsistencyGuarantee(self) -> System.Runtime.ConstrainedExecution.Consistency:
        ...

    @property
    def Cer(self) -> System.Runtime.ConstrainedExecution.Cer:
        ...

    def __init__(self, consistencyGuarantee: System.Runtime.ConstrainedExecution.Consistency, cer: System.Runtime.ConstrainedExecution.Cer) -> None:
        ...


class PrePrepareMethodAttribute(System.Attribute):
    """This class has no documentation."""

    def __init__(self) -> None:
        ...


class CriticalFinalizerObject(System.Object, metaclass=abc.ABCMeta):
    """This class has no documentation."""

    def __init__(self) -> None:
        """This method is protected."""
        ...


