f2 = open('type_from_commitmessage.txt', 'a')
with open ("commitMessages.txt") as f1:
    for line in f1:
        if line.startswith("fix"):
            f2.write("fix\n")
        elif line.startswith("feat"):
            f2.write("feat\n")
        elif line.startswith("build"):
            f2.write("build\n")
        elif line.startswith("docs"):
            f2.write("docs\n")
        elif line.startswith("test"):
            f2.write("test\n")
        elif line.startswith("ci"):
            f2.write("ci\n")
        elif line.startswith("release"):
            f2.write("release\n")
        elif line.startswith("chore"):
            f2.write("chore\n")
        else:
            f2.write("none\n")
