with open("TrueOrFalse.csv", encoding="utf8") as file:
    short_answer_array = file.readlines()

i = 0
for line in short_answer_array:
    i += 1
    line_array = line.strip().split(",")
    question = line_array[0]
    answer_string = line_array[1]
    if answer_string in {"T", "对"}:
        answer = "1"
    else:
        answer = "2"

    config_string = "{}\n\nN/A\nN/A\nN/A\nN/A\n{}\n".format(question, answer)
    with open("data/tf/{}.config".format(i), "w", encoding="utf8", newline="\n") as file:
        file.write(config_string)
