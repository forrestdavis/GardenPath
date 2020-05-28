import math
import glob 
import numpy

def get_surp_rows(article_data):

    rows = 0
    surp_total = 0
    with open(article_data, 'r') as data:

        #skip header
        data.readline()
        for line in data:
            line = line.strip().split()
            if not line:
                continue
            if '===' in line[0]:
                break

            rows += 1
            surp = float(line[4])
            surp_total += surp

    return surp_total, rows

shuffs = []
ordered = []

values = ['a', 'b', 'c', 'd', 'e']

for value in values:

    direct = 'order_'+value+'/*'

    total_surp = 0
    total_rows = 0
    for article_data in glob.glob(direct):
        surp, row = get_surp_rows(article_data)
        if row == 0:
            print(article_data)
        total_surp += surp
        total_rows += row

    ppl = math.pow(2, total_surp/total_rows)
    ordered.append(ppl)

    direct = 'shuff_'+value+'/*'

    total_surp = 0
    total_rows = 0
    for article_data in glob.glob(direct):
        surp, row = get_surp_rows(article_data)
        total_surp += surp
        total_rows += row

    ppl = math.pow(2, total_surp/total_rows)
    shuffs.append(ppl)

print('shuffled:', shuffs, sum(shuffs)/len(shuffs), numpy.std(shuffs))
print('ordered:', ordered, sum(ordered)/len(ordered), numpy.std(ordered))
