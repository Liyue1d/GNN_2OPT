f = open("troyes.txt", "r")
a = open("xml.txt", "w")
for x in f:
	line = x.split(',')
	start = int(line[0].replace("(","")) + 1
	end = int(line[1]) + 1
	cost = float(line[2].replace("[",""))
	a.write("<EDGE_MISSION id =\"1\" src=\"%d\" dst=\"%d\" distance=\"%f\" time=\"0\" fare=\"0\" energy=\"0\"/>\n"%(start,end,cost))

a.close()
f.close()
