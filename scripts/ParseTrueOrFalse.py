import csv
import utils


utils.mkdir("../data/tf")
file_name = utils.ask_file_name()
if file_name:
    with open(file_name, encoding="utf8") as file:
        reader = csv.reader(file)
        i = 0
        for line in reader:
            i += 1
            question = line[0]
            answer_string = line[1]
            if answer_string in {"T", "对"}:
                answer = "1"
            else:
                answer = "2"
            config_string = "{}\n\nN/A\nN/A\nN/A\nN/A\n{}\n".format(question, answer)
            with open("../data/tf/{}.config".format(i), "w", encoding="utf8", newline="\n") as file:
                file.write(config_string)
