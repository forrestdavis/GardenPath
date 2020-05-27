def write_article(article_num, sents):
    fname = 'wiki103_'+str(article_num)+'.valid'

    with open(fname, 'w') as out_file:
        for sent in sents:
            out_file.write(sent+'\n')

with open('../wiki103.valid', 'r') as valid_data:

    article_num = 0
    line = valid_data.readline().strip()
    if '=' not in line:
        line = valid_data.readline().strip()
    sents = [line]
    for line in valid_data:
        line = line.strip()
        #flag for article labels
        if line and line[0] == '=':
            if line[2] != '=':
                write_article(article_num, sents)
                sents = [line]
                article_num += 1

        sents.append(line)

    write_article(article_num, sents)
