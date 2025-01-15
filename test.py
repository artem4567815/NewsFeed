print(2)
a = "*" * 200
c = 0
while ("****") in a or ("???") in a:
    if "****" in a:
        a = a.replace("****", "???", 1)
        c += 3
    a = a.replace("??", "*", 1)

print(c)