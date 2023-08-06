
class TimeSeries:

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

    def setOutputSize(self, size):
        self.size = size
        return self

    def compact(self):
        return self.setOutputSize(TimeSeriesOutputSize.COMPACT)

    def full(self):
        return self.setOutputSize(TimeSeriesOutputSize.FULL)

    def setDataType(self, dataType):
        self.dataType = dataType
        return self

    def json(self):
        return self.setDataType(TimeSeriesDataType.JSON)

    def csv(self):
        return self.setDataType(TimeSeriesDataType.CSV)

    def setApi(self, api):
        self.api = api
        return api

    def __str__(self):
        return str(self.__dict__)
