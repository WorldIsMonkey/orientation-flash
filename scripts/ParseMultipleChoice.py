import csv
import utils


utils.mkdir("../data/mc")
file_name = utils.ask_file_name()
if file_name:
    with open(file_name, encoding="utf-8") as file:
        reader = csv.reader(file)
        i = 0
        for line in reader:
            i = i + 1
            question = line[0]
            option_a = line[1]
            option_b = line[2]
            option_c = line[3]
            option_d = line[4]
            correct_answer = ord(line[5]) - ord('A') + 1
            with open("../data/mc/%s.config" % i, "wb") as config_file:
                string = "%s\n\n%s\n%s\n%s\n%s\n%s\n" % (question, option_a, option_b, option_c, option_d, correct_answer)
                config_file.write(string.encode("utf-8"))
