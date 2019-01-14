import numpy as np
bedcount = np.zeros(shape=7, dtype=np.int64)
lotcount = np.zeros(shape=7, dtype=np.int64)
beds = 0
plots = 0
f = open("input.txt", "r")
out = open("output.txt", "w")
sspace = np.array([])
sp = np.array([])
pspace = np.array([])
total = np.array([])
age = np.array([])

iplines = f.readlines()
lines = [x.strip() for x in iplines]
b = int(lines[0])
p = int(lines[1])

l = int(lines[2])
for line in lines[3:l+3]:
    sspace = np.append(sspace, line)
    sp = np.append(sp, int(line))

l2 = int(lines[3+l])
for line in lines[4+l:4+l+l2]:
    pspace = np.append(pspace, line)
    sp = np.append(sp, int(line))

t = int(lines[4+l+l2])
for line in lines[5+l+l2:5+l+l2+t]:
    total = np.append(total, line)

sp[:] = [x - 1 for x in sp]
sspace = np.sort(sspace)
pspace = np.sort(pspace)

if l > 0:
    i = 0
    beds = 0
    for line in total:
        if line[0:5] == sspace[i]:
            m = 13
            for k in range(7):
                bedcount[k] = bedcount[k] + int(line[m])
                beds = beds + int(line[m])
                m = m+1
            i = i + 1
            if i == l:
                break

if l2 > 0:
    i = 0
    plots = 0
    for line in total:
        if line[0:5] == pspace[i]:
            m = 13
            for k in range(7):
                lotcount[k] = lotcount[k] + int(line[m])
                plots = plots + int(line[m])
                m = m+1
            i = i + 1
            if i == l2:
                break
tot = np.copy(total)

total = np.delete(total, sp)

index = np.array([])
i = 0
for line in total:
    m = 13
    for k in range(7):
        if int(line[m]) + lotcount[k] > p:
            index = np.append(index, i)
            break
        m = m + 1
    i = i + 1

total = np.delete(total,index)

spla = np.array([])
common = np.array([])
lahsa = np.array([])

for line in total:
    if line[10:13] == 'NYY':
        spla = np.append(spla, line)
        age = np.append(age, int(line[6:9]))
count = np.array([])

for line in total:
    if line[9] == 'N' and line[5] == 'F' and int(line[6:9]) > 17:
        lahsa = np.append(lahsa, line)

i = 0
for line in spla:
    if line[9] == 'N' and line[5] == 'F' and age[i] > 17:
        common = np.append(common, line)
    i = i+1


def fun(total, spla, lahsa, maxormin, lotcount, bedcount, beds, plots, depth):
    # print(str(maxormin) +str(beds)+ '--' + str(plots)+'--'+  str(depth) +'--'+np.array2string(total) + ' \n')

    if depth == 0:
        return None, plots - beds

    if maxormin:
        flag = True
        v = float("-inf")
        node = None
        for person in spla:
            if not np.isin(person, total):
                continue
            if can_place(person, lotcount, p):
                flag = False
                m = 13
                c = 0
                for k in range(7):
                    lotcount[k] = lotcount[k] + int(person[m])
                    c = c + int(person[m])
                    m = m + 1
                # print(total.size)

                total = np.delete(total, np.where(total == person))

                #add persons lot count to lotcount
                # print(total.size)
                if depth == 5:
                    tmpval = fun(total,spla,lahsa, False, lotcount, bedcount, beds, plots + c, depth - 1)
                else:
                    tmpval = fun(total, spla, lahsa, False, lotcount, bedcount, beds, plots + c, depth - 1)

                # print(str(tmpval[0]) +'   ' + str(tmpval[1]) + 'val' + np.array2string(person) + str(depth) + ' \n')
                if tmpval[1] > v:
                    v = tmpval[1]
                    node = person

                total = np.append(total, person)
                m = 13
                for k in range(7):
                    lotcount[k] = lotcount[k] - int(person[m])
                    m = m + 1
        if flag:
            return fun(total,spla, lahsa, False, lotcount, bedcount, beds, plots, depth - 1)
        return node, v
    else:

        valid = True
        v = float("inf")
        node = None
        for person in lahsa:
            if not np.isin(person, total):
                continue
            if can_place(person, bedcount, b):
                valid = False
                m = 13
                c = 0
                for k in range(7):
                    bedcount[k] = bedcount[k] + int(person[m])
                    c = c + int(person[m])
                    m = m + 1
                # print(total.size)


                total = np.delete(total, np.where(total == person))
                # print(total.size)

                tmpval = fun(total,spla,lahsa, True, lotcount, bedcount, beds + c, plots, depth - 1)
                total = np.append(total, person)
                m = 13
                for k in range(7):
                    bedcount[k] = bedcount[k] - int(person[m])
                    m = m + 1
                if tmpval[1] < v:
                    v = tmpval[1]
                    node = person
        if valid:
            return fun(total, spla, lahsa, True, lotcount, bedcount, beds, plots, depth - 1)

        return node, v


def can_place(person, tmp, max_allowed):
    m = 13
    used_count = np.copy(tmp)
    for k in range(7):
        used_count[k] = used_count[k] + int(person[m])
        if used_count[k] > max_allowed:
            return False
        m = m + 1
    return True



id = fun(total, spla, lahsa, True, lotcount, bedcount, beds, plots, 5)[0][0:5]
out.write(id)