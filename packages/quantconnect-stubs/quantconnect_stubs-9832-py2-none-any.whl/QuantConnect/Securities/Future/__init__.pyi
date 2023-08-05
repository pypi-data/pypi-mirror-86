import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Interfaces
import QuantConnect.Securities
import QuantConnect.Securities.Future
import System
import System.Collections.Generic


class FutureHolding(QuantConnect.Securities.SecurityHolding):
    """Future holdings implementation of the base securities class"""

    def __init__(self, security: QuantConnect.Securities.Security, currencyConverter: QuantConnect.Securities.ICurrencyConverter) -> None:
        """
        Future Holding Class constructor
        
        :param security: The future security being held
        :param currencyConverter: A currency converter instance
        """
        ...


class Future(QuantConnect.Securities.Security, QuantConnect.Securities.IDerivativeSecurity):
    """Futures Security Object Implementation for Futures Assets"""

    DefaultSettlementDays: int = 1
    """The default number of days required to settle a futures sale"""

    DefaultSettlementTime: datetime.timedelta = ...
    """The default time of day for settlement"""

    @property
    def IsFutureChain(self) -> bool:
        """Returns true if this is the future chain security, false if it is a specific future contract"""
        ...

    @property
    def IsFutureContract(self) -> bool:
        """Returns true if this is a specific future contract security, false if it is the future chain security"""
        ...

    @property
    def Expiry(self) -> datetime.datetime:
        """Gets the expiration date"""
        ...

    @property
    def SettlementType(self) -> QuantConnect.SettlementType:
        """Specifies if futures contract has physical or cash settlement on settlement"""
        ...

    @SettlementType.setter
    def SettlementType(self, value: QuantConnect.SettlementType):
        """Specifies if futures contract has physical or cash settlement on settlement"""
        ...

    @property
    def Underlying(self) -> QuantConnect.Securities.Security:
        """Gets or sets the underlying security object."""
        ...

    @Underlying.setter
    def Underlying(self, value: QuantConnect.Securities.Security):
        """Gets or sets the underlying security object."""
        ...

    @property
    def ContractFilter(self) -> QuantConnect.Securities.IDerivativeSecurityFilter:
        """Gets or sets the contract filter"""
        ...

    @ContractFilter.setter
    def ContractFilter(self, value: QuantConnect.Securities.IDerivativeSecurityFilter):
        """Gets or sets the contract filter"""
        ...

    @typing.overload
    def __init__(self, exchangeHours: QuantConnect.Securities.SecurityExchangeHours, config: QuantConnect.Data.SubscriptionDataConfig, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.SymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider) -> None:
        """
        Constructor for the Future security
        
        :param exchangeHours: Defines the hours this exchange is open
        :param config: The subscription configuration for this security
        :param quoteCurrency: The cash object that represent the quote currency
        :param symbolProperties: The symbol properties for this security
        :param currencyConverter: Currency converter used to convert CashAmount instances into units of the account currency
        :param registeredTypes: Provides all data types registered in the algorithm
        """
        ...

    @typing.overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.SymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider, securityCache: QuantConnect.Securities.SecurityCache) -> None:
        """
        Constructor for the Future security
        
        :param symbol: The subscription security symbol
        :param exchangeHours: Defines the hours this exchange is open
        :param quoteCurrency: The cash object that represent the quote currency
        :param symbolProperties: The symbol properties for this security
        :param currencyConverter: Currency converter used to convert CashAmount     instances into units of the account currency
        :param registeredTypes: Provides all data types registered in the algorithm
        """
        ...

    @typing.overload
    def SetFilter(self, minExpiry: datetime.timedelta, maxExpiry: datetime.timedelta) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified expiration range values
        
        :param minExpiry: The minimum time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in more than 10 days
        :param maxExpiry: The maximum time until expiry to include, for example, TimeSpan.FromDays(10) would exclude contracts expiring in less than 10 days
        """
        ...

    @typing.overload
    def SetFilter(self, minExpiryDays: int, maxExpiryDays: int) -> None:
        """
        Sets the ContractFilter to a new instance of the filter
        using the specified expiration range values
        
        :param minExpiryDays: The minimum time, expressed in days, until expiry to include, for example, 10 would exclude contracts expiring in more than 10 days
        :param maxExpiryDays: The maximum time, expressed in days, until expiry to include, for example, 10 would exclude contracts expiring in less than 10 days
        """
        ...

    @typing.overload
    def SetFilter(self, universeFunc: typing.Callable[[QuantConnect.Securities.FutureFilterUniverse], QuantConnect.Securities.FutureFilterUniverse]) -> None:
        """
        Sets the ContractFilter to a new universe selection function
        
        :param universeFunc: new universe selection function
        """
        ...

    @typing.overload
    def SetFilter(self, universeFunc: typing.Any) -> None:
        """
        Sets the ContractFilter to a new universe selection function
        
        :param universeFunc: new universe selection function
        """
        ...


class FutureCache(QuantConnect.Securities.SecurityCache):
    """Future specific caching support"""


class FutureExchange(QuantConnect.Securities.SecurityExchange):
    """Future exchange class - information and helper tools for future exchange properties"""

    @property
    def TradingDaysPerYear(self) -> int:
        """Number of trading days per year for this security, 252."""
        ...

    def __init__(self, exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> None:
        """
        Initializes a new instance of the FutureExchange class using the specified
        exchange hours to determine open/close times
        
        :param exchangeHours: Contains the weekly exchange schedule plus holidays
        """
        ...


class FutureMarginModel(QuantConnect.Securities.SecurityMarginModel):
    """Represents a simple margin model for margin futures. Margin file contains Initial and Maintenance margins"""

    class MarginRequirementsEntry(System.Object):
        """This class has no documentation."""

        @property
        def Date(self) -> datetime.datetime:
            """Date of margin requirements change"""
            ...

        @Date.setter
        def Date(self, value: datetime.datetime):
            """Date of margin requirements change"""
            ...

        @property
        def InitialOvernight(self) -> float:
            """Initial overnight margin for the contract effective from the date of change"""
            ...

        @InitialOvernight.setter
        def InitialOvernight(self, value: float):
            """Initial overnight margin for the contract effective from the date of change"""
            ...

        @property
        def MaintenanceOvernight(self) -> float:
            """Maintenance overnight margin for the contract effective from the date of change"""
            ...

        @MaintenanceOvernight.setter
        def MaintenanceOvernight(self, value: float):
            """Maintenance overnight margin for the contract effective from the date of change"""
            ...

        @property
        def InitialIntraday(self) -> float:
            """Initial intraday margin for the contract effective from the date of change"""
            ...

        @InitialIntraday.setter
        def InitialIntraday(self, value: float):
            """Initial intraday margin for the contract effective from the date of change"""
            ...

        @property
        def MaintenanceIntraday(self) -> float:
            """Maintenance intraday margin for the contract effective from the date of change"""
            ...

        @MaintenanceIntraday.setter
        def MaintenanceIntraday(self, value: float):
            """Maintenance intraday margin for the contract effective from the date of change"""
            ...

    @property
    def EnableIntradayMargins(self) -> bool:
        """True will enable usage of intraday margins."""
        ...

    @EnableIntradayMargins.setter
    def EnableIntradayMargins(self, value: bool):
        """True will enable usage of intraday margins."""
        ...

    @property
    def InitialOvernightMarginRequirement(self) -> float:
        """Initial Overnight margin requirement for the contract effective from the date of change"""
        ...

    @property
    def MaintenanceOvernightMarginRequirement(self) -> float:
        """Maintenance Overnight margin requirement for the contract effective from the date of change"""
        ...

    @property
    def InitialIntradayMarginRequirement(self) -> float:
        """Initial Intraday margin for the contract effective from the date of change"""
        ...

    @property
    def MaintenanceIntradayMarginRequirement(self) -> float:
        """Maintenance Intraday margin requirement for the contract effective from the date of change"""
        ...

    def __init__(self, requiredFreeBuyingPowerPercent: float = 0, security: QuantConnect.Securities.Security = None) -> None:
        """
        Initializes a new instance of the FutureMarginModel
        
        :param requiredFreeBuyingPowerPercent: The percentage used to determine the required unused buying power for the account.
        :param security: The security that this model belongs to
        """
        ...

    def GetLeverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the current leverage of the security
        
        :param security: The security to get leverage for
        :returns: The current leverage in the security
        """
        ...

    def SetLeverage(self, security: QuantConnect.Securities.Security, leverage: float) -> None:
        """
        Sets the leverage for the applicable securities, i.e, futures
        
        :param leverage: The new leverage
        """
        ...

    def GetMaximumOrderQuantityForTargetBuyingPower(self, parameters: QuantConnect.Securities.GetMaximumOrderQuantityForTargetBuyingPowerParameters) -> QuantConnect.Securities.GetMaximumOrderQuantityResult:
        """
        Get the maximum market order quantity to obtain a position with a given buying power percentage.
        Will not take into account free buying power.
        
        :param parameters: An object containing the portfolio, the security and the target signed buying power percentage
        :returns: Returns the maximum allowed market order quantity and if zero, also the reason
        """
        ...

    def GetInitialMarginRequiredForOrder(self, parameters: QuantConnect.Securities.InitialMarginRequiredForOrderParameters) -> float:
        """
        Gets the total margin required to execute the specified order in units of the account currency including fees
        
        This method is protected.
        
        :param parameters: An object containing the portfolio, the security and the order
        :returns: The total margin in terms of the currency quoted in the order
        """
        ...

    def GetMaintenanceMargin(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the margin currently alloted to the specified holding
        
        This method is protected.
        
        :param security: The security to compute maintenance margin for
        :returns: The maintenance margin required for the
        """
        ...

    def GetInitialMarginRequirement(self, security: QuantConnect.Securities.Security, quantity: float) -> float:
        """
        The margin that must be held in order to increase the position by the provided quantity
        
        This method is protected.
        """
        ...


class FuturesExpiryFunctions(System.Object):
    """Calculate the date of a futures expiry given an expiry month and year"""

    DairyReportDates: System.Collections.Generic.Dictionary[datetime.datetime, datetime.datetime] = ...
    """
    The USDA publishes a report containing contract prices for the contract month.
    You can generate the report dates here: https://mpr.datamart.ams.usda.gov/menu.do?path=Products\\Dairy\\All%20Dairy\\(DY_CL102)%20National%20Dairy%20Products%20Prices%20-%20Monthly
    And you can see future publication dates at https://usda.library.cornell.edu/concern/publications/zs25x847n
    These dates are erratic and requires maintenance of a separate list instead of using holiday entries in MHDB.
    """

    EnbridgeNoticeOfShipmentDates: System.Collections.Generic.Dictionary[datetime.datetime, datetime.datetime] = ...
    """Enbridge's Notice of Shipment report dates. Used to calculate the last trade date for CSW"""

    FuturesExpiryDictionary: System.Collections.Generic.Dictionary[QuantConnect.Symbol, typing.Callable[[datetime.datetime], datetime.datetime]] = ...
    """
    Dictionary of the Functions that calculates the expiry for a given year and month.
    It does not matter what the day and time of day are passed into the Functions.
    The Functions is responsible for calculating the day and time of day given a year and month
    """

    @staticmethod
    def FuturesExpiryFunction(symbol: typing.Union[QuantConnect.Symbol, str]) -> typing.Callable[[datetime.datetime], datetime.datetime]:
        """Method to retrieve the Function for a specific future symbol"""
        ...


class FuturesExpiryUtilityFunctions(System.Object):
    """Class to implement common functions used in FuturesExpiryFunctions"""

    @staticmethod
    def AddBusinessDays(time: datetime.datetime, n: int, useEquityHolidays: bool = True, holidayList: System.Collections.Generic.IEnumerable[datetime.datetime] = None) -> datetime.datetime:
        """
        Method to retrieve n^th succeeding/preceding business day for a given day
        
        :param time: The current Time
        :param n: Number of business days succeeding current time. Use negative value for preceding business days
        :param useEquityHolidays: Use LEAN's USHoliday definitions as holidays to exclude
        :param holidayList: Enumerable of holidays to exclude. These should be sourced from the MarketHoursDatabase
        :returns: The date-time after adding n business days
        """
        ...

    @staticmethod
    def NthLastBusinessDay(time: datetime.datetime, n: int, holidayList: System.Collections.Generic.IEnumerable[datetime.datetime] = None) -> datetime.datetime:
        """
        Method to retrieve the n^th last business day of the delivery month.
        
        :param time: DateTime for delivery month
        :param n: Number of days
        :param holidayList: Additional holidays to use while calculating n^th business day. Useful for MHDB entries
        :returns: Nth Last Business day of the month
        """
        ...

    @staticmethod
    def NthBusinessDay(time: datetime.datetime, nthBusinessDay: int, holidayList: System.Collections.Generic.IEnumerable[datetime.datetime] = None) -> datetime.datetime:
        """
        Calculates the n^th business day of the month (includes checking for holidays)
        
        :param time: Month to calculate business day for
        :param nthBusinessDay: n^th business day to get
        :param holidayList: Additional user provided holidays to not count as business days
        :returns: Nth business day of the month
        """
        ...

    @staticmethod
    def SecondFriday(time: datetime.datetime) -> datetime.datetime:
        """
        Method to retrieve the 2nd Friday of the given month
        
        :param time: Date from the given month
        :returns: 2nd Friday of given month
        """
        ...

    @staticmethod
    def ThirdFriday(time: datetime.datetime) -> datetime.datetime:
        """
        Method to retrieve the 3rd Friday of the given month
        
        :param time: Date from the given month
        :returns: 3rd Friday of given month
        """
        ...

    @staticmethod
    def NthFriday(time: datetime.datetime, n: int) -> datetime.datetime:
        """
        Method to retrieve the Nth Friday of the given month
        
        :param time: Date from the given month
        :param n: The order of the Friday in the period
        :returns: Nth Friday of given month
        """
        ...

    @staticmethod
    def ThirdWednesday(time: datetime.datetime) -> datetime.datetime:
        """
        Method to retrieve third Wednesday of the given month (usually Monday).
        
        :param time: Date from the given month
        :returns: Third Wednesday of the given month
        """
        ...

    @staticmethod
    def NthWeekday(time: datetime.datetime, n: int, dayOfWeek: System.DayOfWeek) -> datetime.datetime:
        """
        Method to retrieve the Nth Weekday of the given month
        
        :param time: Date from the given month
        :param n: The order of the Weekday in the period
        :param dayOfWeek: The day of the week
        :returns: Nth Weekday of given month
        """
        ...

    @staticmethod
    def LastWeekday(time: datetime.datetime, dayOfWeek: System.DayOfWeek) -> datetime.datetime:
        """
        Method to retrieve the last weekday of any month
        
        :param time: Date from the given month
        :param dayOfWeek: the last weekday to be found
        :returns: Last day of the we
        """
        ...

    @staticmethod
    def LastThursday(time: datetime.datetime) -> datetime.datetime:
        """
        Method to retrieve the last weekday of any month
        
        :param time: Date from the given month
        :returns: Last day of the we
        """
        ...

    @staticmethod
    def NotHoliday(time: datetime.datetime) -> bool:
        """
        Method to check whether a given time is holiday or not
        
        :param time: The DateTime for consideration
        :returns: True if the time is not a holidays, otherwise returns false
        """
        ...

    @staticmethod
    def NotPrecededByHoliday(thursday: datetime.datetime) -> bool:
        """
        This function takes Thursday as input and returns true if four weekdays preceding it are not Holidays
        
        :param thursday: DateTime of a given Thursday
        :returns: False if DayOfWeek is not Thursday or is not preceded by four weekdays,Otherwise returns True
        """
        ...

    @staticmethod
    def DairyLastTradeDate(time: datetime.datetime, lastTradeTime: typing.Optional[datetime.timedelta] = None) -> datetime.datetime:
        """
        Gets the last trade date corresponding to the contract month
        
        :param time: Contract month
        :param lastTradeTime: Time at which the dairy future contract stops trading (usually should be on 17:10:00 UTC)
        """
        ...

    @staticmethod
    def ExpiresInPreviousMonth(underlying: str) -> int:
        """
        Returns the number of months prior to the contract month that the future expires
        
        :param underlying: The future symbol
        :returns: The number of months prior it expires
        """
        ...

    @staticmethod
    def GetDatesFromDateTimeList(dateTimeList: System.Collections.Generic.IEnumerable[datetime.datetime]) -> System.Collections.Generic.List[datetime.datetime]:
        """
        Extracts Date portion of list of DateTimes for
        
        :param dateTimeList: List of DateTimes (with optional time portion) to filter
        :returns: List of DateTimes with default time (00:00:00)
        """
        ...


class FutureSymbol(System.Object):
    """Static class contains common utility methods specific to symbols representing the future contracts"""

    @staticmethod
    def IsStandard(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Determine if a given Futures contract is a standard contract.
        
        :param symbol: Future symbol
        :returns: True if symbol expiration matches standard expiration
        """
        ...

    @staticmethod
    def IsWeekly(symbol: typing.Union[QuantConnect.Symbol, str]) -> bool:
        """
        Returns true if the future contract is a weekly contract
        
        :param symbol: Future symbol
        :returns: True if symbol is non-standard contract
        """
        ...


class EmptyFutureChainProvider(System.Object, QuantConnect.Interfaces.IFutureChainProvider):
    """An implementation of IFutureChainProvider that always returns an empty list of contracts"""

    def GetFutureContractList(self, symbol: typing.Union[QuantConnect.Symbol, str], date: datetime.datetime) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Gets the list of future contracts for a given underlying symbol
        
        :param symbol: The underlying symbol
        :param date: The date for which to request the future chain (only used in backtesting)
        :returns: The list of future contracts
        """
        ...


