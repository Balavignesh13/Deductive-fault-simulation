def fanout_fault(x, y, z, faultlist_x):
    return list(set().union(faultlist_x, [10*ord(z) + int(not(y))]))


def xorgate_faultlist(x, y, z, a, faultlist_x, faultlist_y):
    if((x == 0 and y == 1) or (x == 1 and y == 0)):
        temp1 = list(set(faultlist_x).difference(faultlist_y))
        temp2 = list(set(faultlist_y).difference(faultlist_x))
        faultlist_z = list(set().union(
            temp1, temp2, [10*ord(a) + int(not(z))]))
    else:
        temp = list(set().union(faultlist_x, faultlist_y))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))
    return faultlist_z


def andgate_faultlist(x, y, z, a, faultlist_x, faultlist_y):
    if(x == 0 and y == 0):
        temp = list(set(faultlist_x).intersection(faultlist_y))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))
    elif(x == 0 and y == 1):
        temp = list(set(faultlist_x).difference(faultlist_y))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))

    elif(x == 1 and y == 0):
        temp = list(set(faultlist_y).difference(faultlist_x))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))

    elif(x == 1 and y == 1):
        temp = list(set().union(faultlist_x, faultlist_y))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))

    return faultlist_z


def orgate_faultlist(x, y, z, a, faultlist_x, faultlist_y):
    if(x == 0 and y == 0):
        temp = list(set().union(faultlist_x, faultlist_y))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))
    elif(x == 0 and y == 1):
        temp = list(set(faultlist_y).difference(faultlist_x))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))

    elif(x == 1 and y == 0):
        temp = list(set(faultlist_x).difference(faultlist_y))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))

    elif(x == 1 and y == 1):
        temp = list(set(faultlist_x).intersection(faultlist_y))
        faultlist_z = list(set().union(temp, [10*ord(a) + int(not(z))]))
    return faultlist_z


for cc in range(8):
    if len(bin(cc)[2:]) == 1:
        a = 0
        b = 0
        x = int(str(bin(cc)[2:])[0])
    elif len(bin(cc)[2:]) == 2:
        a = 0
        b = int(str(bin(cc)[2:])[0])
        x = int(str(bin(cc)[2:])[1])
    else:
        a = int(str(bin(cc)[2:])[0])
        b = int(str(bin(cc)[2:])[1])
        x = int(str(bin(cc)[2:])[2])

    # primary inputs fault list
    faultlist_a = [10*ord('a') + int(not(a))]
    faultlist_b = [10*ord('b') + int(not(b))]
    faultlist_x = [10*ord('x') + int(not(x))]

    # fanouts
    c = a
    faultlist_c = fanout_fault(a, c, 'c', faultlist_a)
    e = a
    faultlist_e = fanout_fault(a, e, 'e', faultlist_a)
    d = b
    faultlist_d = fanout_fault(b, d, 'd', faultlist_b)
    f = b
    faultlist_f = fanout_fault(b, f, 'f', faultlist_b)

    # Xor gates
    h = c ^ d
    faultlist_h = xorgate_faultlist(c, d, h, 'h', faultlist_c, faultlist_d)

    i = e & f
    faultlist_i = andgate_faultlist(e, f, i, 'i', faultlist_e, faultlist_f)

    j = h
    faultlist_j = fanout_fault(h, j, 'j', faultlist_h)
    l = h
    faultlist_l = fanout_fault(h, l, 'l', faultlist_h)
    k = x
    faultlist_k = fanout_fault(x, k, 'k', faultlist_x)
    m = x
    faultlist_m = fanout_fault(x, m, 'm', faultlist_x)

    # XOR
    n = j ^ k  # sum
    faultlist_n = xorgate_faultlist(j, k, n, 'n', faultlist_j, faultlist_k)

    o = l & m
    faultlist_o = andgate_faultlist(l, m, o, 'o', faultlist_l, faultlist_m)

    p = o | i  # carry
    faultlist_p = orgate_faultlist(o, i, p, 'p', faultlist_o, faultlist_i)

    print('\n#####--------- j0 means line j stuck at 0 and j1 means line j stuck at 1 ---------#####')
    sumline_faultlist = []
    for fault in faultlist_n:
        quo = int(fault/10)
        sumline_faultlist.append(chr(quo)+str(fault % 10))

    carryline_faultlist = []
    for fault in faultlist_p:
        quo = int(fault/10)
        carryline_faultlist.append(chr(quo)+str(fault % 10))

    print("\nFor input -", a, b, x)
    print("Sum fault list:", sumline_faultlist)
    print("Carry fault list:", carryline_faultlist)
