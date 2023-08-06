from xpinyin import Pinyin

print("*** 初始化拼音模块")


class MXPinyin:
    def __init__(self):
        self.pinyin = Pinyin()

    def getPinyin(self, text, splitter=""):
        return self.pinyin.get_pinyin(text, splitter)


if __name__ == "__main__":
    p = MXPinyin()
    p.getPinyin("上海")
