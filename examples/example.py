if __name__ == "__main__":
    from fx import *
    a = Data.getTickData("EURUSD", "2023", "1")
    print(a)
    b = Data.getCandleData("EURUSD", "2023", "1", Frequency.MINUTE)
    print(b)