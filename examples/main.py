if __name__ == "__main__":
    from fxdata import *
    fd = FXData()
    df = fd.getData("EURUSD",
                    datetime(2023, 10, 4),
                    datetime(2023, 10, 23),
                    dataType=DataType.TICK
                    )
    print(df)
