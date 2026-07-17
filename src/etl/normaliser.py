def normalize_year(year):
    return int(str(year).strip())


def normalize_ticker(ticker):
    return str(ticker).strip().upper()
  
if __name__ == "__main__":
    print(normalize_year("2024"))
    print(normalize_ticker(" tcs "))  