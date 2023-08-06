from pkgutil import get_data

# https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
BIN = get_data("shukujitsu.asof20201118", "syukujitsu.csv")
TXT = BIN.decode("cp932")
