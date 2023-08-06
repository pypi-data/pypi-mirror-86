class MOOCXING():
    def __init__(self):
        pass

    def initMqtt(self, host="mqtt.16302.com", port=1883):
        from .MXMqtt import MXMqtt
        return MXMqtt(host, port)

    def initMinecraft(self, address="localhost", port=4711):
        from mcpi.minecraft import Minecraft
        try:
            mc = Minecraft.create(address, port)
            print("*** 初始化Minecraft模块")
            return mc
        except:
            print("--- 未检测到Minecraft服务器")

    def initOpenCV(self):
        import cv2
        return cv2

    def initAnalysis(self, paths, nlp=None):
        from .MXAnalysis import MXAnalysis
        return MXAnalysis(paths, nlp)

    def initNLP(self, APP_ID, API_KEY, SECRET_KEY):
        from .MXNLP import MXNLP
        return MXNLP(APP_ID, API_KEY, SECRET_KEY)

    def initSpeech(self, APP_ID, API_KEY, SECRET_KEY):
        from .MXSpeech import MXSpeech
        return MXSpeech(APP_ID, API_KEY, SECRET_KEY)

    def initPinyin(self):
        from .MXPinyin import MXPinyin
        return MXPinyin()

    def initThread(self):
        from .MXThread import MXThread
        return MXThread()

    def initMedia(self):
        from .MXMedia import MXMedia
        return MXMedia()

    def initSerial(self, com=None, bps=9600):
        from .MXSerial import MXSerial
        try:
            if com is None:
                return MXSerial(MXSerial.getCom(), bps)
            else:
                return MXSerial(com, bps)
        except:
            print("--- 未检测到串口")
