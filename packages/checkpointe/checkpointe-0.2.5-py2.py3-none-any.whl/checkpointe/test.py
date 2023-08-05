import functions as check

check.start(summary=True, verbose=True, memory=True)

add = 2 + 2

check.point("ADDITION")

mult = 2 * 2

check.point("MULTIPLICATION")

exp = 2 ** 2

check.point("EXPONENTIAL")

check.stop()