import sys
for line in sys.stdin:
    if line.startswith("##"):
        sys.stdout.write(line)
        continue
    data = line.strip().split('\t')
    if line.startswith("#CHR"):
        data[9] = sys.argv[1]
        sys.stdout.write("\t".join(data[:10]) + '\n')
        continue
        
    cnt = ""
    if data[9] == "1/1":
        cnt += "1"
    else:
        cnt += "0"
    cnt += "|"
    if data[10] == "1/1":
        cnt += "1"
    else:
        cnt += "0"
    sys.stdout.write("\t".join(data[:9]) + "\t" + cnt + "\n")
