with open('MultipleChoice.csv', 'r', encoding='utf-8') as file:
    filelines = file.readlines()
i = 0
for line in filelines:
    i = i + 1
    splitted_line = line.split(',')
    question = splitted_line[0]
    option_a = splitted_line[1]
    option_b = splitted_line[2]
    option_c = splitted_line[3]
    option_d = splitted_line[4]
    correct_answer = ord(splitted_line[5]) - ord('A') + 1
    with open('data/mc/%s.config' % i, 'wb') as config_file:
        string = "%s\n\n%s\n%s\n%s\n%s\n%s\n" % (question, option_a, option_b, option_c, option_d, correct_answer)
        config_file.write(string.encode('utf-8'))
    