from cryptography.fernet import Fernet

class encryption:
    def encrypt(text):
        data = open("sensitiveData.txt","r+")
        ekey = open("ekey.txt", "r+")
        key = Fernet.generate_key()
        keyList = ekey.readlines()
        ekey.writeline(key)
        keyNum = len(keyList)
        ekey.write(key + "\n")
        fernet = Fernet(key)
        encryptedtext = fernet.encrypt(text.encode())
        data.write(encryptedtext + "," + keyNum + "\n")
    def getEncrypted(index):
        data = open("sensitiveData.txt","r+")
        dataList = data.readlines()
        return dataList[index]
    def decrypt(text):
        data = open("sensitiveData.txt","r+")
        ekey = open("ekey.txt", "r+")
        keyList = ekey.readlines()
        encText = text.split(",")
        fernet = Fernet(keyList[int(encText[1])])
        decMessage = fernet.decrypt(encText[0]).decode()
        return decMessage
    def shuffle():
        data = open("sensitiveData.txt","r+")
        ekey = open("ekey.txt", "r+")
        with open("ekey.txt", "w") as file:
            pass
        keyList = ekey.readlines()
        newKeyList = []
        dataList = data.readlines()
        oldDataList = []
        newDataList = []
        for i in range(len(dataList)):
            oldData = dataList[i].split(",")
            fernet = Fernet(keyList[int(encText[1])])
            decMessage = fernet.decrypt(encText[0]).decode()
            oldDataList.append(decMessage)
        for i in range(len(dataList)):
            key = Fernet.generate_key()
            keyList = ekey.readlines()
            ekey.writeline(key)
            keyNum = len(keyList)
            ekey.write(key + "\n")
            fernet = Fernet(key)
            encryptedtext = fernet.encrypt(text.encode())
            data.write(encryptedtext + "," + keyNum + "\n")