if __name__ == "__main__":
    from fx import *
    if os.getcwd().split("/")[-1] == "examples":
        os.chdir("../")
    d = Data()
    d.keepCSV = False
    d.keepGZIP = True

    e = d.getData("EURUSD", datetime(2020, 10, 2), datetime(2021, 11, 2))
    #a = d.getTickData("EURUSD", "2023", "1")
    #b = d.getCandleData("EURUSD", "2023", "2", Frequency.MINUTE)
