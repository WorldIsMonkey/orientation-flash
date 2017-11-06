folderPath = "./"
csvPath = folderPath + "ShortAnswer.csv"
with open(csvPath, encoding="utf8") as file:
    shortAnswerArray = file.readlines()

i = 0
for line in shortAnswerArray:
    i += 1
    lineArray = line.strip().split(",")
    question = lineArray[0]
    answer = lineArray[1]
    configString = "{0}\n\n{1}\nN/A\nN/A\nN/A\n-1".format(question, answer)
    with open("{0}data/sq/{1}.config".format(folderPath, i), 'w', encoding="utf8") as file:
        file.write(configString)
