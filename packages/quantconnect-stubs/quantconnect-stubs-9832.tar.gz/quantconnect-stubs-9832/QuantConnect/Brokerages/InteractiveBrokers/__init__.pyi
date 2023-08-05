import datetime
import typing

import QuantConnect
import QuantConnect.Brokerages
import QuantConnect.Brokerages.InteractiveBrokers
import QuantConnect.Brokerages.InteractiveBrokers.Client
import QuantConnect.Brokerages.InteractiveBrokers.FinancialAdvisor
import QuantConnect.Data
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Packets
import QuantConnect.Securities
import System
import System.Collections.Concurrent
import System.Collections.Generic

System_EventHandler = typing.Any
ContractDetails = typing.Any


class InteractiveBrokersBrokerage(QuantConnect.Brokerages.Brokerage, QuantConnect.Interfaces.IDataQueueHandler, QuantConnect.Interfaces.IDataQueueUniverseProvider):
    """The Interactive Brokers brokerage"""

    @property
    def IsConnected(self) -> bool:
        """Returns true if we're currently connected to the broker"""
        ...

    @property
    def IsFinancialAdvisor(self) -> bool:
        """Returns true if the connected user is a financial advisor or non-disclosed broker"""
        ...

    @property
    def Client(self) -> QuantConnect.Brokerages.InteractiveBrokers.Client.InteractiveBrokersClient:
        """Provides public access to the underlying IBClient instance"""
        ...

    @staticmethod
    def IsMasterAccount(account: str) -> bool:
        """
        Returns true if the account is a financial advisor or non-disclosed broker master account
        
        :param account: The account code
        :returns: True if the account is a master account
        """
        ...

    @typing.overload
    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator) -> None:
        """
        Creates a new InteractiveBrokersBrokerage using values from configuration:
            ib-account (required)
            ib-host (optional, defaults to LOCALHOST)
            ib-port (optional, defaults to 4001)
            ib-agent-description (optional, defaults to Individual)
        
        :param algorithm: The algorithm instance
        :param orderProvider: An instance of IOrderProvider used to fetch Order objects by brokerage ID
        :param securityProvider: The security provider used to give access to algorithm securities
        :param aggregator: consolidate ticks
        """
        ...

    @typing.overload
    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator, account: str) -> None:
        """
        Creates a new InteractiveBrokersBrokerage for the specified account
        
        :param algorithm: The algorithm instance
        :param orderProvider: An instance of IOrderProvider used to fetch Order objects by brokerage ID
        :param securityProvider: The security provider used to give access to algorithm securities
        :param account: The account used to connect to IB
        """
        ...

    @typing.overload
    def __init__(self, algorithm: QuantConnect.Interfaces.IAlgorithm, orderProvider: QuantConnect.Securities.IOrderProvider, securityProvider: QuantConnect.Securities.ISecurityProvider, aggregator: QuantConnect.Data.IDataAggregator, account: str, host: str, port: int, ibDirectory: str, ibVersion: str, userName: str, password: str, tradingMode: str, agentDescription: str = ...) -> None:
        """
        Creates a new InteractiveBrokersBrokerage from the specified values
        
        :param algorithm: The algorithm instance
        :param orderProvider: An instance of IOrderProvider used to fetch Order objects by brokerage ID
        :param securityProvider: The security provider used to give access to algorithm securities
        :param aggregator: consolidate ticks
        :param account: The Interactive Brokers account name
        :param host: host name or IP address of the machine where TWS is running. Leave blank to connect to the local host.
        :param port: must match the port specified in TWS on the Configure>API>Socket Port field.
        :param ibDirectory: The IB Gateway root directory
        :param ibVersion: The IB Gateway version
        :param userName: The login user name
        :param password: The login password
        :param tradingMode: The trading mode: 'live' or 'paper'
        :param agentDescription: Used for Rule 80A describes the type of trader.
        """
        ...

    def PlaceOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Places a new order and assigns a new broker ID to the order
        
        :param order: The order to be placed
        :returns: True if the request for a new order has been placed, false otherwise
        """
        ...

    def UpdateOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Updates the order with the same id
        
        :param order: The new order information
        :returns: True if the request was made for the order to be updated, false otherwise
        """
        ...

    def CancelOrder(self, order: QuantConnect.Orders.Order) -> bool:
        """
        Cancels the order with the specified ID
        
        :param order: The order to cancel
        :returns: True if the request was made for the order to be canceled, false otherwise
        """
        ...

    def GetOpenOrders(self) -> System.Collections.Generic.List[QuantConnect.Orders.Order]:
        """
        Gets all open orders on the account
        
        :returns: The open orders returned from IB
        """
        ...

    def GetAccountHoldings(self) -> System.Collections.Generic.List[QuantConnect.Holding]:
        """
        Gets all holdings for the account
        
        :returns: The current holdings from the account
        """
        ...

    def GetCashBalance(self) -> System.Collections.Generic.List[QuantConnect.Securities.CashAmount]:
        """
        Gets the current cash balance for each currency held in the brokerage account
        
        :returns: The current cash balance for each currency available for trading
        """
        ...

    def GetExecutions(self, symbol: str, type: str, exchange: str, timeSince: typing.Optional[datetime.datetime], side: str) -> System.Collections.Generic.List[QuantConnect.Brokerages.InteractiveBrokers.Client.ExecutionDetailsEventArgs]:
        """
        Gets the execution details matching the filter
        
        :returns: A list of executions matching the filter
        """
        ...

    def Connect(self) -> None:
        """Connects the client to the IB gateway"""
        ...

    def Disconnect(self) -> None:
        """Disconnects the client from the IB gateway"""
        ...

    def Dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def FindContracts(self, contract: typing.Any, ticker: str) -> System.Collections.Generic.IEnumerable[ContractDetails]:
        ...

    def SetJob(self, job: QuantConnect.Packets.LiveNodePacket) -> None:
        """
        Sets the job we're subscribing for
        
        :param job: Job we're subscribing for
        """
        ...

    def Subscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig, newDataAvailableHandler: System_EventHandler) -> System.Collections.Generic.IEnumerator[QuantConnect.Data.BaseData]:
        """
        Subscribe to the specified configuration
        
        :param dataConfig: defines the parameters to subscribe to a data feed
        :param newDataAvailableHandler: handler to be fired on new data available
        :returns: The new enumerator for this subscription request
        """
        ...

    def Unsubscribe(self, dataConfig: QuantConnect.Data.SubscriptionDataConfig) -> None:
        """
        Removes the specified configuration
        
        :param dataConfig: Subscription config to be removed
        """
        ...

    @staticmethod
    def AdjustQuantity(type: QuantConnect.SecurityType, size: int) -> int:
        """Modifies the quantity received from IB based on the security type"""
        ...

    def LookupSymbols(self, lookupName: str, securityType: QuantConnect.SecurityType, includeExpired: bool, securityCurrency: str = None, securityExchange: str = None) -> System.Collections.Generic.IEnumerable[QuantConnect.Symbol]:
        """
        Method returns a collection of Symbols that are available at the broker.
        
        :param lookupName: String representing the name to lookup
        :param securityType: Expected security type of the returned symbols (if any)
        :param includeExpired: Include expired contracts
        :param securityCurrency: Expected security currency(if any)
        :param securityExchange: Expected security exchange name(if any)
        """
        ...

    def CanAdvanceTime(self, securityType: QuantConnect.SecurityType) -> bool:
        """
        Returns whether the time can be advanced or not.
        
        :param securityType: The security type
        :returns: true if the time can be advanced
        """
        ...

    def GetHistory(self, request: QuantConnect.Data.HistoryRequest) -> System.Collections.Generic.IEnumerable[QuantConnect.Data.BaseData]:
        """
        Gets the history for the requested security
        
        :param request: The historical data request
        :returns: An enumerable of bars covering the span specified in the request
        """
        ...

    def ShouldPerformCashSync(self, currentTimeUtc: datetime.datetime) -> bool:
        """
        Returns whether the brokerage should perform the cash synchronization
        
        :param currentTimeUtc: The current time (UTC)
        :returns: True if the cash sync should be performed
        """
        ...


class InteractiveBrokersAccountData(System.Object):
    """This class contains account specific data such as properties, cash balances and holdings"""

    @property
    def AccountProperties(self) -> System.Collections.Concurrent.ConcurrentDictionary[str, str]:
        """The raw IB account properties"""
        ...

    @property
    def CashBalances(self) -> System.Collections.Concurrent.ConcurrentDictionary[str, float]:
        """The account cash balances indexed by currency"""
        ...

    @property
    def AccountHoldings(self) -> System.Collections.Concurrent.ConcurrentDictionary[str, QuantConnect.Holding]:
        """The account holdings indexed by symbol"""
        ...

    @property
    def FinancialAdvisorConfiguration(self) -> QuantConnect.Brokerages.InteractiveBrokers.FinancialAdvisor.FinancialAdvisorConfiguration:
        """The configuration data for the financial advisor account"""
        ...

    def Clear(self) -> None:
        """Clears this instance of InteractiveBrokersAccountData"""
        ...


class InteractiveBrokersSymbolMapper(System.Object, QuantConnect.Brokerages.ISymbolMapper):
    """Provides the mapping between Lean symbols and InteractiveBrokers symbols."""

    @typing.overload
    def __init__(self) -> None:
        """Constructs InteractiveBrokersSymbolMapper. Default parameters are used."""
        ...

    @typing.overload
    def __init__(self, ibNameMap: System.Collections.Generic.Dictionary[str, str]) -> None:
        """
        Constructs InteractiveBrokersSymbolMapper
        
        :param ibNameMap: New names map (IB -> LEAN)
        """
        ...

    @typing.overload
    def __init__(self, ibNameMapFullName: str) -> None:
        """
        Constructs InteractiveBrokersSymbolMapper
        
        :param ibNameMapFullName: Full file name of the map file
        """
        ...

    def GetBrokerageSymbol(self, symbol: typing.Union[QuantConnect.Symbol, str]) -> str:
        """
        Converts a Lean symbol instance to an InteractiveBrokers symbol
        
        :param symbol: A Lean symbol instance
        :returns: The InteractiveBrokers symbol
        """
        ...

    def GetLeanSymbol(self, brokerageSymbol: str, securityType: QuantConnect.SecurityType, market: str, expirationDate: datetime.datetime = ..., strike: float = 0, optionRight: QuantConnect.OptionRight = 0) -> QuantConnect.Symbol:
        """
        Converts an InteractiveBrokers symbol to a Lean symbol instance
        
        :param brokerageSymbol: The InteractiveBrokers symbol
        :param securityType: The security type
        :param market: The market
        :param expirationDate: Expiration date of the security(if applicable)
        :param strike: The strike of the security (if applicable)
        :param optionRight: The option right of the security (if applicable)
        :returns: A new Lean Symbol instance
        """
        ...

    def GetBrokerageRootSymbol(self, rootSymbol: str) -> str:
        """
        IB specific versions of the symbol mapping (GetBrokerageRootSymbol) for future root symbols
        
        :param rootSymbol: LEAN root symbol
        """
        ...

    def GetLeanRootSymbol(self, brokerageRootSymbol: str) -> str:
        """
        IB specific versions of the symbol mapping (GetLeanRootSymbol) for future root symbols
        
        :param brokerageRootSymbol: IB Brokerage root symbol
        """
        ...


class InteractiveBrokersStateManager(System.Object):
    """Holds the brokerage state information (connection status, error conditions, etc.)"""

    @property
    def Disconnected1100Fired(self) -> bool:
        """Gets/sets whether the IB client has received a Disconnect (1100) message"""
        ...

    @Disconnected1100Fired.setter
    def Disconnected1100Fired(self, value: bool):
        """Gets/sets whether the IB client has received a Disconnect (1100) message"""
        ...

    @property
    def PreviouslyInResetTime(self) -> bool:
        """Gets/sets whether the previous reconnection attempt was performed during the IB reset period"""
        ...

    @PreviouslyInResetTime.setter
    def PreviouslyInResetTime(self, value: bool):
        """Gets/sets whether the previous reconnection attempt was performed during the IB reset period"""
        ...

    def Reset(self) -> None:
        """Resets the state to the default values"""
        ...


class HistoricalDataType(System.Object):
    """Historical Data Request Return Types"""

    Trades: str = "TRADES"
    """Return Trade data only"""

    Midpoint: str = "MIDPOINT"
    """Return the mid point between the bid and ask"""

    Bid: str = "BID"
    """Return Bid Prices only"""

    Ask: str = "ASK"
    """Return ask prices only"""

    BidAsk: str = "BID_ASK"
    """Return Bid / Ask price only"""


class InteractiveBrokersBrokerageFactory(QuantConnect.Brokerages.BrokerageFactory):
    """Factory type for the InteractiveBrokersBrokerage"""

    @property
    def BrokerageData(self) -> System.Collections.Generic.Dictionary[str, str]:
        """Gets the brokerage data required to run the IB brokerage from configuration"""
        ...

    def __init__(self) -> None:
        """Initializes a new instance of the InteractiveBrokersBrokerageFactory class"""
        ...

    def GetBrokerageModel(self, orderProvider: QuantConnect.Securities.IOrderProvider) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        Gets a new instance of the InteractiveBrokersBrokerageModel
        
        :param orderProvider: The order provider
        """
        ...

    def CreateBrokerage(self, job: QuantConnect.Packets.LiveNodePacket, algorithm: QuantConnect.Interfaces.IAlgorithm) -> QuantConnect.Interfaces.IBrokerage:
        """
        Creates a new IBrokerage instance and set ups the environment for the brokerage
        
        :param job: The job packet to create the brokerage for
        :param algorithm: The algorithm instance
        :returns: A new brokerage instance
        """
        ...

    def Dispose(self) -> None:
        """
        Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources.
        Stops the InteractiveBrokersGatewayRunner
        """
        ...


