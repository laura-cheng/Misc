phi = 23662270311503602529211462628663973377651035055221337186547659666520360329842954292759496973737109678655075242892199643594552737098393308599593056828393459168374450665246772208443010635514095222872450488941067111566431597659514538203376236380298940327397320377486921733162063179848071474045388486658414200

e = 65537
def extgcd(a, b, x, y):
    # return d, x, y
    if b == 0:
        return a, 1, 0
    else:
        d, y, x = extgcd(b, a % b, x, y)
        y -= (a // b) * x
        return d, x, y

dd, x, y = extgcd(e, phi, 0, 0)
print("d = ", x)