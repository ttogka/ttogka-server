from django.db import models

# Create your models here.

class CustomAutoField(models.AutoField):
    def get_next_value(self, *args, **kwargs):
        current_max = self.model.objects.all().aggregate(models.Max(self.attname))
        return current_max[self.attname] + 1 if current_max[self.attname] else 1

class Card(models.Model):
    id = CustomAutoField(primary_key=True)

    card = models.CharField(verbose_name='카드명', null=True, blank=True, max_length=20)
    brand = models.CharField(verbose_name='회사명', null=True, blank=True, max_length=10)
    image = models.ImageField(verbose_name='이미지', null=True, blank=True)
    cate = models.CharField(verbose_name='카드유형', null=True, blank=True, max_length=30)
    view_count = models.IntegerField(verbose_name='조회수', default=0)
    mylist_count = models.IntegerField(verbose_name='담긴수', default=0)
    fee1 = models.CharField(verbose_name='연회비1', null=True, blank=True, max_length=30)
    fee2 = models.CharField(verbose_name='연회비2', null=True, blank=True, max_length=30)
    pre_perform = models.CharField(verbose_name='전월실적', null=True, blank=True, max_length=30)
    bnf1 = models.CharField(verbose_name='주요혜택1', null=True, blank=True, max_length=30)
    bnf2 = models.CharField(verbose_name='주요혜택2', null=True, blank=True, max_length=30)
    bnf3 = models.CharField(verbose_name='주요혜택3', null=True, blank=True, max_length=30)
    link_url = models.CharField(verbose_name='상세링크', null=True, blank=True, max_length=60)

class Benefit(models.Model):
    id = CustomAutoField(primary_key=True)

    card = models.ForeignKey(to='Card', verbose_name='카드번호', on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(verbose_name='혜택카테고리', null=True, blank=True, max_length=5)
    category_code = models.IntegerField(verbose_name='카테고리코드', null=True, blank=True)
    content = models.CharField(verbose_name='혜택내용', null=True, blank=True, max_length=60)

"""
CATEGORY = [
    # 0. 모든가맹점
    ('모든가맹점', '국내외가맹점', '하이브리드'),
    # 1. 교통
    ('교통', '대중교통', '기차', '고속버스', '택시'),
    # 2. 주유
    ('주유', '주유소', '충전소'),
    # 3. 통신
    ('통신', 'KT', 'SKT', 'LGU+'),
    # 4. 마트/편의점
    ('마트/편의점', '대형마트', '편의점', '전통시장', 'SSM'),
    # 5. 쇼핑
    ('쇼핑', '멤버십포인트', '온라인쇼핑', '백화점', '홈쇼핑', '소셜커머스', '면세점', '아울렛', '인테리어', 'SPA브랜드', '제휴/PLCC'),
    # 6. 푸드
    ('푸드', '배달앱', '점심', '일반음식점', '패밀리레스토랑', '저녁', '패스트푸드', '주점'),
    # 7. 카페/디저트
    ('카페/디저트', '카페', '베이커리', '아이스크림'),
    # 8. 뷰티/피트니스
    ('뷰티/피트니스', '화장품', '헤어', '드럭스토어', '피트니스'),
    # 9. 무실적/적립
    ('무실적', '적립', '할인', '캐시백', '해피포인트', 'BC TOP', 'OK캐쉬백', 'CJ ONE', '혜택 프로모션', '무이자할부'),
    # 10. 공과금/렌탈
    ('공과금/렌탈', '공과금', '렌탈'), 
    # 11. 병원/약국
    ('병원/약국', '병원'), 
    # 12. 애완동물
    ('애완동물', '동물병원', '펫샵'), 
    # 13. 교육/육아
    ('교육/육아', '국민행복', '학원', '아이행복', '학습지', '문화센터', '어린이집'), 
    # 14. 자동차/하이패스
    ('자동차/하이패스', '자동차', '보험', '보험사', '하이패스', '정비', '차/중고차'), 
    # 15. 레저스포츠
    ('레저/스포츠', '경기관람', '게임', '테마파크', '골프'), 
    # 16. 영화/문화
    ('영화/문화', '영화', '디지털구독', '도서', '공연/전시', '음원사이트'), 
    # 17. 간편결제
    ('간편결제', '카카오페이', 'APP', '네이버페이', '삼성페이'), 
    # 18. 항공마일리지
    ('항공마일리지', '대한항공', '아시아나항공', '저가항공', '제주항공'), 
    # 19. 공항라운지/PP
    ('공항라운지/PP', '공항라운지', '라운지키'), 
    # 20. 프리미엄
    ('프리미엄', '바우처', '프리미엄 서비스'), 
    # 21. 여행/숙박
    ('여행/숙박', '렌터카', '호텔', '여행사', '항공권', '리조트', '온라인 여행사'), 
    # 22. 해외
    ('해외', '수수료우대', '해외이용', '해외직구'), 
    # 23. 비즈니스/금융
    ('비즈니스', '금융', '증권사', '은행사'), 
    # 24. 생활
    ('생활', '직장인', '지역'),
    # 25. 기타
    ('기타', '-', '선택형', '유의사항', '혜택1', '혜택2'), 
]
"""

"""
1.	신한카드
2.	삼성카드
3.	현대카드
4.	KB국민카드
5.	롯데카드`
6.	NH농협카드
7.	우리카드
8.	하나카드
9.	BC 바로카드
10.	IBK기업은행
11.	MG새마을금고
12.	씨티카드
13.	카카오뱅크
14.	카카오페이
15.	토스뱅크
16.	BNK부산은행
17.	DGB대구은행
18.	전북은행
19.	제주은행
20.	SC제일은행
21.	케이뱅크
22.	광주은행
23.	Sh수협은행
24.	SBI저축은행
25.	KB증권
26.	유안타증권
27.	교보증권
28.	SSGPAY. CARD
29.	한패스
30.	현대백화점
31.	신협
32.	우체국
33.	차이
34.	유진투자증권
35.	미래에셋증권
36.	SK증권
37.	한국투자증권
38.	핀트
39.	핀크카드
40.	트래블월렛
41.	토스
42.	코나카드
43.	엔에이치엔페이코
44.	아이오로라
45.	다날
46.	NH투자증권
47.	KG모빌리언스
48.	KDB산업은행
49.	DB금융투자
"""