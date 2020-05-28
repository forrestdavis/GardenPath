N = 100

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
                #file too big break up
                if len(sents) > 150:
                    x = [sents[i:i + N] for i in range(0, len(sents), N)]
                    for sent in x:
                        write_article(article_num, sent)
                        article_num += 1
                else:
                    write_article(article_num, sents)
                    article_num += 1
                sents = []

        sents.append(line)

    write_article(article_num, sents)
