from django.shortcuts import render
from django.http import HttpResponse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs

from .models import Card, Benefit

from time import sleep

# 카드고릴라 크롤링
def card_view(request):
    if request.method == 'GET':
        options = webdriver.ChromeOptions()
        options.add_argument("headless") # 크롬 창 안띄우기
        driver = webdriver.Chrome(options=options)

        # 웹 페이지의 URL을 지정합니다.
        for code in range(1501, 2573):
            # 상세링크
            url = f"https://www.card-gorilla.com/card/detail/{code}"
            driver.get(url)

            # 웹 페이지 호출 상태 점검
            if driver.page_source:
                print("웹 페이지 가져오기 성공!")
            else:
                print("웹 페이지 가져오기 실패!")
            print(code)

            # 변수 초기화
            card = "-"
            brand = "-"
            # able = "-"
            src = "-"
            fee1 = "-"
            fee2 = "-"
            pre_perform = "-"
            bnf = ["-" for _ in range(4)]
            bene_category = ["-" for _ in range(21)]
            bene_content = ["-" for _ in range(21)]
            idx = 1

            # 태그 class 경로
            soup = bs(driver.page_source, 'lxml')
            detail_con = soup.find("div", attrs={"class": "detail_con"})
            if detail_con: # 존재하지 않는 인덱스 예외 처리
                card_top = detail_con.find("article", attrs={"class": "card_top"})
                data_area = card_top.find("div", attrs={"class": "data_area"})
                tit = data_area.find("div", attrs={"class": "tit"})

                # 카드명과 회사명
                card = tit.find("strong", attrs={"class": "card"}).get_text()
                # print(f"카드명: {card}")
                brand = tit.find("p", attrs={"class": "brand"}).get_text()
                # print(f"회사명: {brand}")

                # 이미지
                card_img = card_top.find("img")
                src = card_img['src']

                bnf2 = card_top.find("div", attrs={"class": "bnf2"})
                # 연회비
                fee = bnf2.find("dl")
                fee1_tag = fee.find("span")
                if fee1_tag:
                    fee1 = fee1_tag.get_text()
                    fee2_tag = fee.find("span").next_sibling
                    if fee2_tag:
                        fee2 = fee2_tag.get_text()

                # 전월실적
                pre_perform_tag = fee.next_sibling
                if pre_perform_tag:
                    pre_perform = pre_perform_tag.get_text()
                

                # 주요 혜택들
                bnf1 = data_area.find("div", attrs={"class": "bnf1"})
                bnfs = bnf1.find_all("dl")

                idx = 1
                for b in bnfs:
                    bnf[idx] = b.get_text()
                    # print(f"주요혜택{idx}: {bnf[idx]}")
                    idx += 1

                # 상세 혜택들
                bene_area = detail_con.find("div", attrs={"class": "bene_area"})
                benefits = bene_area.find_all("dl")

                idx = 0
                for benefit in benefits:
                    temp = benefit.find("dt") # 혜택 전체
                    bene_category[idx] = temp.find("p").get_text() # 혜택 카테고리
                    bene_content[idx] = temp.find("i").get_text() # 혜택 내용
                    idx += 1

            ##############f 객체 생성 #################

            card_obj = Card.objects.create(
                card = card,
                brand = brand,
                image = src,
                fee1 = fee1,
                fee2 = fee2,
                pre_perform = pre_perform,
                bnf1 = bnf[1],
                bnf2 = bnf[2],
                bnf3 = bnf[3],
                link_url = url,
                # able = able,
            )

            for i in range(idx):
                benefit_obj = Benefit.objects.create(
                    card = card_obj,
                    category = bene_category[i],
                    category_code = get_code(bene_category[i]),
                    content = bene_content[i],
                )
                print(i, end=', ')

        print("작업이 끝나서 드라이버를 종료합니다.")
        driver.quit()

    return HttpResponse('')

# 카테고리 분류하기
def get_code(category):
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
    for index in range(26):
        if category in CATEGORY[index]:
            return index
    return 25

# 신용카드/체크카드 데이터 받아오기
def get_cate(request):
    if request.method == 'GET':
        driver = webdriver.Chrome()

        # 웹 페이지의 URL을 지정합니다.
        code = "CHK"
        url = f"https://card-gorilla.com/search/card?cate={code}"
        driver.get(url)
        idx = 1
        while 1:
            soup = bs(driver.page_source, 'lxml')
            try:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="q-app"]/section/div[1]/section/div/article[1]/article/a')))
                element.click()
                print(f"{idx}번째 카드 더보기")
                idx += 1
            except TimeoutException:
                break

        soup = bs(driver.page_source, 'lxml')
        soup = soup.find("article", attrs={"class": "results_lst"})
        soup = soup.find("ul", attrs={"class": "lst"})
        lsts = soup.find_all("li")
        idx = 1
        for lst in lsts:
            benefit = lst.find("a", attrs={"class": "b_view"})
            href = benefit.attrs['href']
            find_code = href.split('/')
            code = int(find_code[-1])
            try:
                card = Card.objects.get(pk=code)
                # 데이터 넣기
                card.cate = code
                card.save()
                print(f'{idx}번: 카드 {code} 가져오기 성공!')
            except Card.DoesNotExist:
                # 레코드가 존재하지 않는 경우에 대한 처리
                print(f"카드 pk={code}는 존재하지 않습니다.")
            idx += 1

        print("작업이 끝나서 드라이버를 종료합니다.")
        driver.quit()
    return HttpResponse('')

# 신한카드 url 가져오기
def get_url(request):
    if request.method == 'GET':
        options = webdriver.ChromeOptions()
        options.add_argument("headless") # 크롬 창 안띄우기
        driver = webdriver.Chrome(options=options)
        
        # 신용카드
        # url = f"https://www.shinhancard.com/pconts/html/card/credit/MOBFM281/MOBFM281R11.html?crustMenuId=ms581"
        # 체크카드
        # url = f"https://www.shinhancard.com/pconts/html/card/check/MOBFM282R11.html?crustMenuId=ms52"
        # 프리미엄카드
        url = f"https://www.shinhancard.com/pconts/html/card/premium/MOBFM278R01.html?crustMenuId=ms237"
        driver.get(url)
        sleep(7)

        soup = bs(driver.page_source, 'lxml')
        contents = soup.find("section", attrs={"class": "contents"})
        tab_wrap = contents.find("div", attrs={"class": "tab_wrap"})
        card_list_common = tab_wrap.find("div", attrs={"class": "card_list_common"})
        cardlist = card_list_common.find("ul", attrs={"class": "card_thumb_list_wrap"})
        lsts = cardlist.find_all("li")

        for lst in lsts:
            card_name = lst.find("a", attrs={"class": "card_name"})
            ############## 객체 가져오기 #################
            for code in range(1, 2573):
                card_obj = Card.objects.get(pk=code)

                if card_obj.brand == '신한카드':
                    if card_obj.card == card_name.get_text():
                        card_obj.link_url = "https://www.shinhancard.com" + card_name.attrs['href']
                        card_obj.save()
                        print(f'카드{code}: "{card_obj.card}" 업데이트 성공!')
                        break
                    # else:
                    #     print(f'"{card_obj.card}" 찾지 못함 ㅠ')

        print("작업이 끝나서 드라이버를 종료합니다.")
        driver.quit()
    return HttpResponse('')