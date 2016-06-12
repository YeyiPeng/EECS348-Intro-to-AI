execfile("StrokeHmmbasic.py")
x = StrokeLabeler()
x.trainHMMDir("../trainingFiles/") #../ means go back a directory
# x.confusion
# x.labelFile("../trainingFiles/0128_1.6.1.labeled.xml", "resultstest111.txt")
