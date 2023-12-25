if __name__ == "__main__":
    from fxdata import *
    d = FXData()
    e = d.getData("EURUSD", 
                  datetime(2023, 10, 4), 
                  datetime(2023, 10, 31), 
                  dataType=DataType.TICK
                  )
    print(e)
