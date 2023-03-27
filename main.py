import requests
import re
import json

from pytz import timezone
from datetime import datetime


def callAWSLamdaSlack(notiNm, notiUrl):
    # AWS Lamda slack 연동 호출
    url_l = "https://k75n5fmeyederwrh3z5bg3ryry0rqrko.lambda-url.us-east-2.on.aws/"

    payload_l = json.dumps({
        "notiNm": notiNm,
        "notiUrl": notiUrl
    })
    print(payload_l)
    files_l = [
    ]
    headers_l = {
        'Content-Type': 'application/json'
    }

    response_l = requests.request(
        "POST", url_l, headers=headers_l, data=payload_l, files=files_l)

    res_l = response_l.text
    print(res_l)


today = datetime.now(timezone('Asia/Seoul'))

kstYMD = today.strftime('%Y%m%d')
print(kstYMD)
#kstYMD = "20230320"  


searchStrs = ['신규시설투자등//신규시설투자등(자율공시)', '주요사항보고서(무상증자결정)']

for search in searchStrs:
    print(search)

    # dart.fss.or.kr 에서 신규시설투자 조회하기
    url = "https://dart.fss.or.kr/dsab007/detailSearch.ax"
    payload = {
        'reportName': search,
        'startDate': kstYMD,
        'endDate': kstYMD
    }
    files = [
    ]
    headers = {
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, files=files)

    res = response.text
    #print(res)

    # 조회결과 있는지 정규식으로 추출

    pattern = "openReportViewer\('(.*)',''\)"
    a = re.findall(pattern, res)
    print(a)
    for row in a:
        # print(row)

        url1 = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo=" + row
        print(url1)
        payload1 = {}
        files1 = [
        ]
        headers1 = {
        }

        response1 = requests.request(
            "GET", url1, headers=headers1, data=payload1, files=files1)

        res1 = response1.text
        # print(res1)

        # rcpNo , dcmNo 추출
        pattern1 = "viewDoc\('(.*)', '(.*)', '0', '0', '0', '(.*)',''\);"
        b = re.findall(pattern1, res1)

        rcpNo = b[0][0]
        dcmNo = b[0][1]
        dtd = b[0][2]
        # print(rcpNo,dcmNo)

        # 회사명 추출

        pattern2 = "style=\"cursor:pointer;\">(.*)</span></div>"
        c = re.findall(pattern2, res1)
        companyNm = c[0]
        # print(companyNm)

        # https://dart.fss.or.kr/report/viewer.do?rcpNo=20230228900646&dcmNo=9028761&eleId=0&offset=0&length=0&dtd=HTML

        # reportUrl = "https://dart.fss.or.kr/report/viewer.do?rcpNo=" + rcpNo + "&dcmNo=" + dcmNo + "&eleId=0&offset=0&length=0&dtd=HTML"
        # print(reportUrl)

        notiNm = companyNm + "-" + search
        notiUrl = "https://dart.fss.or.kr/report/viewer.do?rcpNo=" + \
            rcpNo + "&dcmNo=" + dcmNo + "&eleId=0&offset=0&length=0&dtd=" + dtd
        callAWSLamdaSlack(notiNm, notiUrl)
