//
//  ParseShortAnswer.swift
//  ParseShortAnswer
//
//  Created by 夏中洋 on 2017/9/29.
//  Copyright © 2017年 Xia Zhongyang. All rights reserved.
//

import Foundation

let folderPath = "./"
let csvPath = folderPath + "ShortAnswer.csv"
let shortAnswerString = try String(contentsOfFile: csvPath, encoding: String.Encoding.utf8)
let shortAnswerArray = shortAnswerString.components(separatedBy: "\n")

var i = 0
for line in shortAnswerArray {
    i += 1
    let lineArray = line.components(separatedBy: ",")
    let question = lineArray[0]
    let answer = lineArray[1]
    let configString = "\(question)\n\n\(answer)\nN/A\nN/A\nN/A\n-1"
    try configString.write(toFile: "\(folderPath)/data/sq/\(i).config", atomically: false, encoding: String.Encoding.utf8)
}
