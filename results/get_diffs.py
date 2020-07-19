new_header = ['model_type', 'surp']
RC_surp = -4

ref_f = "ref_raw.csv"
temp_f = "temp_raw.csv"
def_f = "def_raw.csv"

reduced_shuffled = []
reduced_ordered = []
unreduced_shuffled = []
unreduced_ordered = []

with open(temp_f, 'r') as temp:

    header = temp.readline().strip().split(',')
    assert header[RC_surp] == "RC_surp"

    for line in temp:
        line = line.strip().split(',')
        if line[1] == "shuffled":
            if line[2] == 'reduced':
                reduced_shuffled.append(line[RC_surp])
            else:
                unreduced_shuffled.append(line[RC_surp])
        else:
            if line[2] == 'reduced':
                reduced_ordered.append(line[RC_surp])
            else:
                unreduced_ordered.append(line[RC_surp])

with open(ref_f, 'r') as ref:

    header = ref.readline().strip().split(',')
    assert header[RC_surp] == "RC_surp"

    for line in ref:
        line = line.strip().split(',')
        if line[1] == "shuffled":
            if line[2] == 'reduced':
                reduced_shuffled.append(line[RC_surp])
            else:
                unreduced_shuffled.append(line[RC_surp])
        else:
            if line[2] == 'reduced':
                reduced_ordered.append(line[RC_surp])
            else:
                unreduced_ordered.append(line[RC_surp])

with open(def_f, 'r') as def_data:
    header = def_data.readline().strip().split(',')

    for line in def_data:
        line = line.strip().split(',')
        if line[1] == "shuffled":
            if line[2] == 'reduced':
                #reduced_shuffled.append(line[RC_surp])
                reduced_shuffled.append(line[-1])
            else:
                #unreduced_shuffled.append(line[RC_surp])
                unreduced_shuffled.append(line[-1])
        else:
            if line[2] == 'reduced':
                #reduced_ordered.append(line[RC_surp])
                reduced_ordered.append(line[-1])
            else:
                #unreduced_ordered.append(line[RC_surp])
                unreduced_ordered.append(line[-1])

out_str = ''
out_str += ','.join(new_header)+'\n'
for x in range(len(reduced_shuffled)):
    shuffled = float(reduced_shuffled[x])-float(unreduced_shuffled[x])
    shuffled = str(shuffled)
    out_str += ','.join(['shuffled', shuffled]) + '\n'
    ordered = float(reduced_ordered[x])-float(unreduced_ordered[x])
    ordered = str(ordered)
    out_str += ','.join(['ordered', ordered]) + '\n'

with open('reduced_unreduced.csv', 'w') as o:
    o.write(out_str)
