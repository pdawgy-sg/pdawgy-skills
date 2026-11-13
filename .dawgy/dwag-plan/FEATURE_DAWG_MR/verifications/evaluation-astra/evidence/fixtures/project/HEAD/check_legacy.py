from average import average
try:
    average([])
except ZeroDivisionError:
    print("legacy exception PASS")
else:
    raise AssertionError("legacy consumer expects ZeroDivisionError")
