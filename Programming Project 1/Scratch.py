f = open("testlevel09.txt","w+")
f.write("S")
for i in range(100):
    for j in range(100):
        f.write("o")
    f.write("\n")
f.write("T")
f.close()