from django.shortcuts import render
from django.http import JsonResponse
import ast
import base64
import cv2
import numpy as np
# import pandas as pd
# import pickle

# category_data = pd.read_csv("idx2category.csv")
# idx2category = {row.k: row.v for idx, row in category_data.iterrows()}

# with open("rdmf.pickle", mode = "rb") as f:
#     model = pickle.load(f)

# def ajax_post_search(request):
#     keyword = request.GET.get('title')

#     # 検索キーワードがあればそれで絞り込み、なければ全ての記事
#     # JSONシリアライズするには、Querysetをリストにする必要あり
#     if keyword:
#         title_list = [post.title for post in Post.objects.filter(title__icontains=keyword)]  # タイトルにキーワードを含む。大文字小文字の区別なし
#     else:
#         title_list = [post.title for post in Post.objects.all()]

#     d = {
#         'title_list': title_list,
#     }
#     return JsonResponse(d)



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
        keyword = keyword.replace('data:image/png;base64,', '')
        keyword = keyword.encode() #str型→bytes型へ
        keyword = base64.b64decode(keyword) #base64をデコード
        jpg=np.frombuffer(keyword, dtype=np.uint8) #raw image <- jpg
        img = cv2.imdecode(jpg, cv2.IMREAD_COLOR) #画像を保存する場合
        print(img)

        
        
        # if keyword == None:
        #     return 1
        data = {"status":"hello"}
        
        return JsonResponse(data = data)
        # return render(
        #     request,
        #     "ocr/home.html",
        #     {"title":100}
        # )
        
