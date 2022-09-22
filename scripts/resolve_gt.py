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
        
    gt, dp1 = data[9].split(':')
    if dp1 == '.':
        dp1 = '0,0'
    cnt = ""
    if gt.startswith(("1/1", "1|1")):
        cnt += "1"
    else:
        cnt += "0"
    cnt += "|"
    gt, dp2 = data[10].split(':')
    if dp2 == '.':
        dp2 = '0,0'
    if gt.startswith(("1/1", "1|1")):
        cnt += "1"
    else:
        cnt += "0"
    dp = dp1 + ',' + dp2
    sys.stdout.write("\t".join(data[:9]) + "\t" + cnt + ":" + dp + "\n")
