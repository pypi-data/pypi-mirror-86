# python-shukujitsu
Japanese holidays library based on static data published by Cabinet Office, Government of Japan

[![image](https://img.shields.io/pypi/l/python-shukujitsu.svg)](https://pypi.org/project/python-shukujitsu/)
[![image](https://img.shields.io/pypi/dm/python-shukujitsu.svg)](https://pypi.org/project/python-shukujitsu/)
[![image](https://img.shields.io/pypi/v/python-shukujitsu.svg)](https://pypi.org/project/python-shukujitsu/)
[![image](https://img.shields.io/pypi/pyversions/python-shukujitsu.svg)](https://pypi.org/project/python-shukujitsu/)

Usage is similar with [python-holidays](https://github.com/dr-prodigy/python-holidays) package but note that this [python-shukujitsu](https://github.com/sakurai-youhei/python-shukujitsu) package covers only holidays in Japan **from year 1955 to 2021** as of today.

```python
import shukujitsu

jp_holidays = shukujitsu.Japan()
# or:
# jp_holidays = shukujitsu.JP()
# or:
# jp_holidays = shukujitsu.CountryHoliday('JP')

date(2020, 7, 24) in jp_holidays  # True
date(2019, 7, 24) in jp_holidays  # False

# The Holiday class will also recognize strings of any format
# and int/float representing a Unix timestamp
'2014-01-01' in jp_holidays  # True
'1/1/2014' in jp_holidays    # True
1388597445 in jp_holidays    # True

jp_holidays.get('2014-01-01')  # "元日"

jp_holidays['2014-01-01': '2014-01-03']  # [date(2014, 1, 1)]
```

## Important Notice

### Source Data

This library is based on following data. (Japanese - 本ライブラリは以下のデータを加工して作成しています。) License of Source Data is [CC BY](https://creativecommons.org/licenses/by/4.0/legalcode.ja) compatible; Exact rule is described at [内閣府ホームページ利用規約](https://www.cao.go.jp/notice/rule.html).

- [内閣府ホームページ](https://www.cao.go.jp/)の[「国民の祝日」について](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html)で公開されている「[昭和30年（1955年）から令和3年（2021年）国民の祝日（csv形式：19KB）](https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv)」（内閣府） （[https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv](https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv)）

### Source Code

This `python-shukujitsu` package may contain copy of and/or modified code from [python-holidays](https://github.com/dr-prodigy/python-holidays) package which is licensed under [MIT License](https://github.com/dr-prodigy/python-holidays/blob/master/LICENSE).

### Relation to Government of Japan

Nothing - NEVER EVER imagine relation to Government of Japan. This is just a personal project.
