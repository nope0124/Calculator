from django.shortcuts import render
from django.http import JsonResponse
import ast
import base64
import cv2
import numpy as np
import keras
#from keras.models import load_model
from tensorflow.keras.models import load_model

def img2frm(img):
    W = 1000
    H = 300
    SP = 3
    ans = ""
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for i in range(H):
        for j in range(W):
            gray_img[i][j] = 255 - gray_img[i][j]
    ret, bin_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)
#    model = keras.models.load_model('model.h5', compile=False)
    model = load_model('model.h5', compile = False)
    num2code = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        7: "7",
        8: "8",
        9: "9",
        10: "+",
        11: "-",
        12: "*",
        13: "/",
    }

    for sp in range(SP):
        
        bw = [0 for i in range(W)]
        for i in range(10, H // SP):
            for j in range(W):
                if bin_img[i + sp * H // SP][j] == 255:
                    bw[j] = 1
                    
        lr = []
        s = -1
        for i in range(W):
            if bw[i] == 1:
                if s == -1:
                    s = i
            elif bw[i] == 0:
                if s != -1:
                    lr.append([s, i - 1])
                    s = -1
        if s != -1:
            lr.append([s, W - 1])
            
        ud = []
        
        for p in lr:
            s = 2147483647
            t = -1
            for i in range(10, H // SP):
                for j in range(p[0], p[1] + 1):
                    if bin_img[i + sp * H // SP][j] == 255:
                        s = min(s, i)
                        t = max(t, i)
            ud.append([s, t])

        pixels_test = []

        for p in range(len(lr)):
            tmp_img = np.zeros((ud[p][1] - ud[p][0] + 1 + 30, lr[p][1] - lr[p][0] + 1 + 30), dtype='uint8')
            for i in range(ud[p][0], ud[p][1] + 1):
                for j in range(lr[p][0], lr[p][1] + 1):
                    tmp_img[i + 15 - ud[p][0]][j + 15 - lr[p][0]] = bin_img[i + sp * H // SP][j]
            pixels_test.append(cv2.resize(tmp_img, (28, 28)))
        S = np.array(pixels_test) / 255
        S = S.reshape(-1, 28, 28, 1)
        if len(S) == 0:
            continue
        ans += "<br>"
        st = ""
        dis = ""
        pred = model.predict(S)
        preds = np.argmax(pred, axis=1)
        for i in preds:
            if i < 10:
                st += num2code[i]
                dis += num2code[i]
            elif i < 12:
                st += " " + num2code[i] + " "
                dis += " " + num2code[i] + " "
            elif i == 12:
                st += " " + num2code[i] + " "
                dis += " × "
            elif i == 13:
                st += " " + num2code[i] + " "
                dis += " ÷ "
        try:
            sum = eval(st)
            ans += dis + " = " + str(sum)
        except ZeroDivisionError:
            ans += dis + " " + "(0除算が発生しています)"
        except SyntaxError:
            ans += dis + " " + "(計算式が間違っています)"
        
    return ans


def index(request):
    if request.method == "GET":
        return render(
            request,
            "ocr/home.html",
            
        )
    elif request.method == "POST":
        # keyword = request.GET["data"]
        # title = [request.POST["title"]]
        # result = model.predict(title)[0]
        # print("result: ", result)
        # pred = idx2category[result]
        keyword = request.body #bodyを取得
        keyword = keyword.decode() #bytes型→str型へ
        keyword = ast.literal_eval(keyword) #str型→dict型へ
        keyword = keyword["data"] #dataを取得
        keyword = keyword.replace('data:image/jpeg;base64,', '')
        # print(keyword)
        keyword = keyword.encode() #str型→bytes型へ
        keyword = base64.b64decode(keyword) #base64をデコード
        jpg=np.frombuffer(keyword, dtype=np.uint8) #raw image <- jpg
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR) #画像を保存する場合
        ans = img2frm(img)
        
        data = {"status":ans}
        
        return JsonResponse(data = data)
