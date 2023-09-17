if __name__ == "__main__":
    from fx import *
    if os.getcwd().split("/")[-1] == "examples":
        os.chdir("../")
    d = Data()
    d.keepCSV = False
    d.keepGZIP = False
    d.outputCSV = True

    e = d.getData("EURUSD", datetime(2020, 1, 2), datetime(2020, 2, 5), _type=DataType.CANDLE, fq=Frequency.MINUTE)
    #a = d.getTickData("EURUSD", "2023", "1")
    #print(a)
    #b = d.getCandleData("EURUSD", "2023", "2", Frequency.MINUTE) 21 40
