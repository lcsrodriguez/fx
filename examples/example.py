if __name__ == "__main__":
    from fx import *
    if os.getcwd().split("/")[-1] == "examples":
        os.chdir("../")
    d = Data()
    d.keepCSV = False
    a = d.getTickData("EURUSD", "2023", "1")
    b = d.getCandleData("EURUSD", "2023", "2", Frequency.MINUTE)
