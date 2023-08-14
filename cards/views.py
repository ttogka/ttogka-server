from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from datas.models import Card, Benefit
# from .serializers import 

class SelectBrandView(APIView):
    def get(self, request):
        extra = request.GET.get('extra', False)
        main_brand_list = [
            {"id": 1,	"brand_name": "신한카드"},
            {"id": 2,	"brand_name": "삼성카드"},
            {"id": 3,	"brand_name": "현대카드"},
            {"id": 4,	"brand_name": "KB국민카드"},
            {"id": 5,	"brand_name": "롯데카드`"},
            {"id": 6,	"brand_name": "NH농협카드"},
            {"id": 7,	"brand_name": "우리카드"},
            {"id": 8,	"brand_name": "하나카드"},
            {"id": 9,	"brand_name": "BC 바로카드"},
            {"id": 10,	"brand_name": "IBK기업은행"},
            {"id": 11,	"brand_name": "MG새마을금고"},
            {"id": 12,	"brand_name": "씨티카드"},
        ]
        extra_brand_list = [
            {"id": 13,	"brand_name": "카카오뱅크"},
            {"id": 14,	"brand_name": "카카오페이"},
            {"id": 15,	"brand_name": "토스뱅크"},
            {"id": 16,	"brand_name": "BNK부산은행"},
            {"id": 17,	"brand_name": "DGB대구은행"},
            {"id": 18,	"brand_name": "전북은행"},
            {"id": 19,	"brand_name": "제주은행"},
            {"id": 20,	"brand_name": "SC제일은행"},
            {"id": 21,	"brand_name": "케이뱅크"},
            {"id": 22,	"brand_name": "광주은행"},
            {"id": 23,	"brand_name": "Sh수협은행"},
            {"id": 24,	"brand_name": "SBI저축은행"},
            {"id": 25,	"brand_name": "KB증권"},
            {"id": 26,	"brand_name": "유안타증권"},
            {"id": 27,	"brand_name": "교보증권"},
            {"id": 28,	"brand_name": "SSGPAY. CARD"},
            {"id": 29,	"brand_name": "한패스"},
            {"id": 30,	"brand_name": "현대백화점"},
            {"id": 31,	"brand_name": "신협"},
            {"id": 32,	"brand_name": "우체국"},
            {"id": 33,	"brand_name": "차이"},
            {"id": 34,	"brand_name": "유진투자증권"},
            {"id": 35,	"brand_name": "미래에셋증권"},
            {"id": 36,	"brand_name": "SK증권"},
            {"id": 37,	"brand_name": "한국투자증권"},
            {"id": 38,	"brand_name": "핀트"},
            {"id": 39,	"brand_name": "핀크카드"},
            {"id": 40,	"brand_name": "트래블월렛"},
            {"id": 41,	"brand_name": "토스"},
            {"id": 42,	"brand_name": "코나카드"},
            {"id": 43,	"brand_name": "엔에이치엔페이코"},
            {"id": 44,	"brand_name": "아이오로라"},
            {"id": 45,	"brand_name": "다날"},
            {"id": 46,	"brand_name": "NH투자증권"},
            {"id": 47,	"brand_name": "KG모빌리언스"},
            {"id": 48,	"brand_name": "KDB산업은행"},
            {"id": 49,	"brand_name": "DB금융투자"},
        ]
        brand_list = main_brand_list if not extra else extra_brand_list

        data = {"brand_list": brand_list}
        return Response(data)
