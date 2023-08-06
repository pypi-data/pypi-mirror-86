import csv

print("*** 初始化CSV模块")


class MXCsv:
    def readData(self,path, num):
        Data = []
        data = csv.reader(open(path, "r", encoding='UTF-8-sig'))
        for d in data:
            if d != []:
                if num == -1:
                    Data.append(d)
                else:
                    Data.append(d[num])

        return Data

    def writeData(self, path, data):
        with open(path, 'a+', encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(data)

    def wData(self, path, data):
        with open(path, 'w', encoding="utf-8", newline="") as f:
            csv.writer(f).writerow(data)

    def getRowCol(self, data):
        return len(data[0]), len(data)
