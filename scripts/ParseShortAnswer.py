import csv
import utils


utils.mkdir("../data/sq")
file_name = utils.ask_file_name()
if file_name:
    with open(file_name, encoding="utf8") as file:
        reader = csv.reader(file)
        i = 0
        for line in reader:
            i += 1
            question = line[0]
            answer = line[1]
            configString = "{0}\n\n{1}\nN/A\nN/A\nN/A\n-1".format(question, answer)
            with open("../data/sq/{}.config".format(i), 'w', encoding="utf8") as config_file:
                config_file.write(configString)
