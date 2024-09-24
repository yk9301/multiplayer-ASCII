import os
os.system("")  # enables ansi escape characters in terminal

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

print(COLOR["GREEN"], "Testing Green!!", COLOR["ENDC"])
a = "1,2,30;"
print(int(a[0]), int(a[2]), int(a[4:-1]))