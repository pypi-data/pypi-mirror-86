import re
import time
import json

print("*** 初始化数据分析模块")


class MXAnalysis():
    def __init__(self, paths, nlp=None):
        self.paths = paths
        self.nlp = nlp

        self.keys, self.values, self.items = [], [], []
        self.data, self.nodes, self.links = [], [], []

        self.fileData = ""
        self.allData = []
        self.__getAllData()

    # list去重
    def __setList(self, li):
        newLi = []
        for l in li:
            if not l in newLi:
                newLi.append(l)
        return newLi

    # 读取文件
    def __readFile(self, path):
        with open(path, "r") as f:
            self.fileData = ""
            for d in f.readlines():
                self.fileData += d

    # 正则数据
    def __regexData(self, key="内容"):
        if key == "内容":
            return re.findall(f'[\d][.,，、.](.*?)\n', self.fileData + "\n")
        else:
            return re.findall(f'{key}[:：](.*?)\n', self.fileData + "\n")[0]

    # 获取全部数据
    def __getAllData(self):
        for path in self.paths:
            self.__readFile(path)
            name = self.__regexData("学生姓名")
            contents = self.__regexData("内容")

            if self.nlp != None:
                data = self.nlp.getInfo(contents)
                print("正在读取" + path)
                time.sleep(0.4)
                contents = []
                for d in data:
                    if "nz" in (d["pos"], d["ne"]):
                        contents.append(d["item"].lower())

            self.allData.append({name: contents})

    # 数据预处理
    def __initData(self):
        self.keys, self.values, self.items = [], [], []
        for data in self.allData:
            self.keys += data.keys()
            self.values += data.values()
            self.items += data.items()

    # 获取知识图谱数据
    def getGraphData(self):
        self.__initData()
        for item in self.items:
            for value in list(set(item[1])):
                self.links.append({"source": item[0], "target": value})

        self.values = list(set(sum(self.values, [])))
        for key in self.keys:
            self.nodes.append({"name": key, "symbolSize": 30})
        for value in self.values:
            self.nodes.append({"name": value})

        return self.nodes, self.links

    # 获取词云数据
    def getWordData(self):
        self.__initData()
        self.values = sum(self.values, [])
        for value in list(set(self.values)):
            self.data.append((value, self.values.count(value)))

        return self.data

    # 保存数据
    def saveData(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f)
