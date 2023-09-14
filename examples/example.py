if __name__ == "__main__":
    from fx import *
    d = Data()
    a = d.getTickData("EURUSD", "2023", "1")
    b = d.getCandleData("EURUSD", "2023", "2", Frequency.MINUTE)
