//
//  ParseTrueOrFalse.swift
//  ParseTrueOrFalse
//
//  Created by 夏中洋 on 2017/9/29.
//  Copyright © 2017年 Xia Zhongyang. All rights reserved.
//

import Foundation

let folderPath = "./"
let csvPath = folderPath + "TrueOrFalse.csv"
let shortAnswerString = try String(contentsOfFile: csvPath, encoding: String.Encoding.utf8)
let shortAnswerArray = shortAnswerString.components(separatedBy: "\n")

var i = 0
for line in shortAnswerArray {
    i += 1
    let lineArray = line.trimmingCharacters(in: .whitespacesAndNewlines).components(separatedBy: ",")
    let question = lineArray[0]
    let answerString = lineArray[1]
    var answer: String
    if answerString == "对" {
        answer = "1"
    } else {
        answer = "2"
    }

    let configString = "\(question)\n\nN/A\nN/A\nN/A\nN/A\n\(answer)\n"
    try configString.write(toFile: "\(folderPath)/data/tf/\(i).config", atomically: false, encoding: String.Encoding.utf8)
}
