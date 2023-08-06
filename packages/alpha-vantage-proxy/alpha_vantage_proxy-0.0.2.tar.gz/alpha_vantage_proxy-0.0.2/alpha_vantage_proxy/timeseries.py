
import requests
from alpha_vantage_proxy.models import TimeSeriesFunction, TimeSeriesOutputSize, TimeSeriesDataType

class TimeSeries:

    function = None
    symbol = None
    apikey = None
    outputsize = None 
    datatype = None

    def setFunction(self, function):
        self.function = function
        return self

    def intraday(self):
        return self.setFunction(TimeSeriesFunction.INTRADAY)

    def intradayExtended(self):
        return self.setFunction(TimeSeriesFunction.INTRADAY_EXTENDED)

    def daily(self):
        return self.setFunction(TimeSeriesFunction.DAILY)

    def dailyAdjusted(self):
        return self.setFunction(TimeSeriesFunction.DAILY_ADJUSTED)

    def weekly(self):
        return self.setFunction(TimeSeriesFunction.WEEKLY)

    def weeklyAdjusted(self):
        return self.setFunction(TimeSeriesFunction.WEEKLY_ADJUSTED)

    def monthly(self):
        return self.setFunction(TimeSeriesFunction.MONTHLY)

    def monthlyAdjusted(self):
        return self.setFunction(TimeSeriesFunction.MONTHLY_ADJUSTED)

    def setSymbol(self, symbol):
        self.symbol = symbol
        return self

    def setOutputSize(self, outputsize):
        self.outputsize = outputsize
        return self

    def compact(self):
        return self.setOutputSize(TimeSeriesOutputSize.COMPACT)

    def full(self):
        return self.setOutputSize(TimeSeriesOutputSize.FULL)

    def setDataType(self, datatype):
        self.datatype = datatype
        return self

    def json(self):
        return self.setDataType(TimeSeriesDataType.JSON)

    def csv(self):
        return self.setDataType(TimeSeriesDataType.CSV)

    def setKey(self, apikey):
        self.apikey = apikey
        return self

    def get(self):

        url = "https://www.alphavantage.co/query?"

        for key in self.__dict__:
            value = self.__dict__[key] if type(self.__dict__[key]) == str else self.__dict__[key].value
            url += key + "=" + value + "&"

        url = url[:-1]

        return requests.get(url)      


    def __str__(self):
        return str(self.__dict__)
