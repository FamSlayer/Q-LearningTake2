import sys



if __name__ == '__main__':
	file = open(sys.argv[1], "r")
	file2 = open(sys.argv[2], "w")
	input = ""
	
	for line in file:
		line = line.split()
		if(len(line) == 0):
			continue
			
		if (line[0] != "EPISODE") and (line[0] != "AVG"):
			input = ""
			continue
		else:
			if line[0] == "EPISODE":
				#print line[2]
				input = ""
				input+=line[2]
			else:
				#print line[3]
				input+=", "
				input+=line[3]
				input+='\n'
				file2.write(input)
	
	file2.close()
	file2.close()