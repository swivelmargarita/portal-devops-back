import requests


def verify(phone, code):
    url = "http://notify.eskiz.uz/api/message/sms/send"
    headers = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjEwNTMsInJvbGUiOiJ1c2VyIiwiZGF0YSI6eyJpZCI6MTA1MywibmFtZSI6Ik9PTyBLT1NJTU9WIEFSVCBBTkQgSVQgR1JPVVAiLCJlbWFpbCI6ImlrYXNpbW92YWJ1MDBAZ21haWwuY29tIiwicm9sZSI6InVzZXIiLCJhcGlfdG9rZW4iOiJleUowZVhBaU9pSktWMVFpTENKaGJHY2lPaUpJVXpJMU5pSjkuZXlKemRXSWlPakV3TlRNc0luSnZiR1VpT2lKMWMyVnlJaXdpWkdGMFlTSTZleUpwWkNJNk1UQTFNeXdpYm1GdFpTSTZJazlQVHlCTFQxTkpUVTlXSUVGU1ZDQkJUa1FnU1ZRZ1IxSlBWVkFpTENKbGJXRnBiQ0k2SW1scllYTnBiVzkyWVdKMU1EQkFaMjFoYVd3dVkyOXRJaXdpY205c1pTSTZJblZ6WlhJaUxDSmhjR2xmZEc5clpXNGlPaUpsZVVvd1pWaEJhVTlwU2t0V01WRnBURU5LYUciLCJzdGF0dXMiOiJhY3RpdmUiLCJzbXNfYXBpX2xvZ2luIjoiZXNraXoyIiwic21zX2FwaV9wYXNzd29yZCI6ImUkJGsheiIsInV6X3ByaWNlIjo1MCwidWNlbGxfcHJpY2UiOjExNSwidGVzdF91Y2VsbF9wcmljZSI6MTE1LCJiYWxhbmNlIjoyODY2NjAsImlzX3ZpcCI6MCwiaG9zdCI6InNlcnZlcjEiLCJjcmVhdGVkX2F0IjoiMjAyMi0xMC0wNFQxMjoxNzowNC4wMDAwMDBaIiwidXBkYXRlZF9hdCI6IjIwMjMtMDUtMTBUMTU6Mzg6MDUuMDAwMDAwWiIsIndoaXRlbGlzdCI6bnVsbH0sImlhdCI6MTY4Mzg4ODU4NSwiZXhwIjoxNjg2NDgwNTg1fQ.S5STi7kBlKZ_2iIygyY0rrvoM0R4C4_nvBez0DqHX48"}
    data = {
        'mobile_phone': phone,
        'message': code,
        'from': "4546",
        'callback_url': 'http://0.0.0.0.uz/test.php'
    }
    response = requests.post(url=url, data=data, headers=headers)
    return response
