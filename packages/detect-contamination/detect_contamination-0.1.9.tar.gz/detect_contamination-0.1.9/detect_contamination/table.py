from texttable import Texttable

def table(result):
    total = 0
    t = Texttable()
    t.add_row(["Name", "Percentage"])

    for item in result:
        result[item] = result[item] * 100
        total += result[item]
        t.add_row([item, result[item]])

    other = 0

    if total != 100:
        other = 100 - total
        t.add_row(["other", other])

    print(t.draw())