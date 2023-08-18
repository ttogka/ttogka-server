from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from rest_framework import generics

from datas.models import Card, Benefit

import random

BRANDS = [
    {"id": 1,	"brand": "신한카드"},
    {"id": 2,	"brand": "삼성카드"},
    {"id": 3,	"brand": "현대카드"},
    {"id": 4,	"brand": "KB국민카드"},
    {"id": 5,	"brand": "롯데카드`"},
    {"id": 6,	"brand": "NH농협카드"},
    {"id": 7,	"brand": "우리카드"},
    {"id": 8,	"brand": "하나카드"},
    {"id": 9,	"brand": "BC 바로카드"},
    {"id": 10,	"brand": "IBK기업은행"},
    {"id": 11,	"brand": "MG새마을금고"},
    {"id": 12,	"brand": "씨티카드"},
    {"id": 13,	"brand": "카카오뱅크"},
    {"id": 14,	"brand": "카카오페이"},
    {"id": 15,	"brand": "토스뱅크"},
    {"id": 16,	"brand": "BNK부산은행"},
    {"id": 17,	"brand": "DGB대구은행"},
    {"id": 18,	"brand": "전북은행"},
    {"id": 19,	"brand": "제주은행"},
    {"id": 20,	"brand": "SC제일은행"},
    {"id": 21,	"brand": "케이뱅크"},
    {"id": 22,	"brand": "광주은행"},
    {"id": 23,	"brand": "Sh수협은행"},
    {"id": 24,	"brand": "SBI저축은행"},
    {"id": 25,	"brand": "KB증권"},
    {"id": 26,	"brand": "유안타증권"},
    {"id": 27,	"brand": "교보증권"},
    {"id": 28,	"brand": "SSGPAY. CARD"},
    {"id": 29,	"brand": "한패스"},
    {"id": 30,	"brand": "현대백화점"},
    {"id": 31,	"brand": "신협"},
    {"id": 32,	"brand": "우체국"},
    {"id": 33,	"brand": "차이"},
    {"id": 34,	"brand": "유진투자증권"},
    {"id": 35,	"brand": "미래에셋증권"},
    {"id": 36,	"brand": "SK증권"},
    {"id": 37,	"brand": "한국투자증권"},
    {"id": 38,	"brand": "핀트"},
    {"id": 39,	"brand": "핀크카드"},
    {"id": 40,	"brand": "트래블월렛"},
    {"id": 41,	"brand": "토스"},
    {"id": 42,	"brand": "코나카드"},
    {"id": 43,	"brand": "엔에이치엔페이코"},
    {"id": 44,	"brand": "아이오로라"},
    {"id": 45,	"brand": "다날"},
    {"id": 46,	"brand": "NH투자증권"},
    {"id": 47,	"brand": "KG모빌리언스"},
    {"id": 48,	"brand": "KDB산업은행"},
    {"id": 49,	"brand": "DB금융투자"},
]

class SelectBrandView(APIView):
    def get(self, request):
        extra = request.GET.get('extra', False)

        main_brand_list = BRANDS[:12]
        extra_brand_list = BRANDS[12:]
        brand_list = main_brand_list if not extra else extra_brand_list

        data = {"brand_list": brand_list}
        return Response(data)

# 카드 리스트
class CardListView(APIView):
    def get(self, request, pk):
        cate = request.GET.get('cate', 'CRD')

        crd_data_list = []
        chk_data_list = []
        data_list = []
        brand = BRANDS[pk-1]["brand"]
        obj = Card.objects.filter(brand=brand).values()
        for i in range(len(obj)):
            instance = {"id": obj[i]["id"], "card": obj[i]["card"], "brand": obj[i]["brand"], "image": obj[i]["image"], "view_count": obj[i]["view_count"]}
            if obj[i]["cate"] == "CRD":
                crd_data_list.append(instance)
            if obj[i]["cate"] == "CHK":
                chk_data_list.append(instance)

        crd_data_list.sort(key=lambda x : -x["view_count"])
        chk_data_list.sort(key=lambda x : -x["view_count"])
        data_list = chk_data_list[:10] if cate == 'CHK' else crd_data_list[:10]

        data = {"card_list": data_list}
        print(f'{brand} 카드사 순위 GET 성공!')
        return Response(data)

# 카드 상세
class CardDetailView(APIView):
    def post(self, request, pk):
        view_count = request.POST.get('view_count')
        card_obj = Card.objects.get(id=pk)
        card_obj.view_count = view_count
        card_obj.save()
        bene_obj = Benefit.objects.filter(card_id=pk).values()
        bene_list = []
        for i in range(len(bene_obj)):
            bene_instance = {"category": bene_obj[i]["category"], "category_code": bene_obj[i]["category_code"], "content": bene_obj[i]["content"]}
            bene_list.append(bene_instance)

        data = {"id": card_obj.id, "card": card_obj.card, "brand": card_obj.brand, "image": str(card_obj.image), "view_count":card_obj.view_count, "benefit_list": bene_list}
        print(f'{card_obj.id} {card_obj.card}: 카드 상세 POST 성공!')
        return Response(data)
        
# 분야별 순위
class CategoryRankView(APIView):
    def get(self, request):
        category_code = request.GET.get('category', 3)
        card_id_list = []
        data_list = []
        bene_obj = Benefit.objects.filter(category_code=category_code).values()
        for i in range(len(bene_obj)):
            if bene_obj[i]["card_id"] not in  card_id_list:
                card_id_list.append(bene_obj[i]["card_id"])
        for n in card_id_list:
            card_obj = Card.objects.get(id=n)
            print(card_obj)
            instane = {"id": card_obj.id, "card": card_obj.card, "brand": card_obj.brand, "image": str(card_obj.image), "view_count": card_obj.view_count}
            data_list.append(instane)

        data_list.sort(key=lambda x : -x["view_count"])
        
        data = {"card_list": data_list[:10]}
        print(f'{category_code} 분야별 순위 GET 성공!')
        return Response(data)

# 광고
class AdvertiseView(CardDetailView):
    def post(self, request):
        ad_card = [121, 2441, 1487, 2330] # 광고 카드 리스트
        id = ad_card[random.randrange(len(ad_card))]

        view_count = request.POST.get('view_count')
        card_obj = Card.objects.get(id=id)
        card_obj.view_count = view_count
        card_obj.save()
        bene_obj = Benefit.objects.filter(card_id=id).values()
        bene_list = []
        for i in range(len(bene_obj)):
            bene_instance = {"category": bene_obj[i]["category"], "category_code": bene_obj[i]["category_code"], "content": bene_obj[i]["content"]}
            bene_list.append(bene_instance)

        data = {"id": card_obj.id, "card": card_obj.card, "brand": card_obj.brand, "image": str(card_obj.image), "view_count":card_obj.view_count, "benefit_list": bene_list}
        print(f'{card_obj.id} {card_obj.card}: 광고 카드 POST 성공!')
        return Response(data)