# coding: UTF-8
import csv

tp = 0
fp = 0
fn = 0
tn = 0

types = ["build", "ci", "docs", "feat", "fix", "test", "release"]

with open('type_comparison.csv') as f:
    reader = csv.reader(f)
    l = [row for row in reader]

none_number = 0
print("######全体######")
for type in types:
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for i in range(len(l)):
        if l[i][0] != "none":
            if l[i][0] == type and l[i][1] == type:
                tp = tp + 1
            elif l[i][1] == type and l[i][0] != type:
                fp = fp + 1
            elif l[i][0] == type and l[i][1] != type:
                fn = fn + 1
            elif l[i][1] != type and l[i][0] != type:
                tn = tn + 1 
            none_number += 1

    print("##############")
    print(type)
    print("<TP>")
    print(tp)
    print("<FP>")
    print(fp)
    print("<FN>")
    print(fn)
    print("<TN>")
    print(tn)

print("合計コミット数")
print(len(l))
print("none以外のコミット数")
print(none_number/7)

print("######7タイプのみ######")
six_only_len = 0
for type in types:
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for i in range(len(l)):
        if l[i][0] == "build" or l[i][0] == "ci" or l[i][0] == "docs" or l[i][0] == "feat" or l[i][0] == "fix" or l[i][0] == "test" or l[i][0] == "release":
            six_only_len += 1
            if l[i][0] == type and l[i][1] == type:
                tp = tp + 1
            elif l[i][1] == type and l[i][0] != type:
                fp = fp + 1
            elif l[i][0] == type and l[i][1] != type:
                fn = fn + 1 
            elif l[i][1] != type and l[i][0] != type:
                tn = tn + 1 

    print("##############")
    print(type)
    print("<TP>")
    print(tp)
    print("<FP>")
    print(fp)
    print("<FN>")
    print(fn)
    print("<TN>")
    print(tn)

print("合計コミット数")
print(six_only_len/7)