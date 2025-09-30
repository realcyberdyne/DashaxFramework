def DCookieValue(request,name):
    RequestLineSplit = request.split('\n')
    CookiesAsString = ""
    for requestLine in RequestLineSplit:
        if 'Cookie:' in requestLine:
            CookiesAsString = requestLine
            break

    CookiesAsArray = CookiesAsString.split(';')
    for cookie in CookiesAsArray:
        CookieKeyValue = cookie.split('=')
        if CookieKeyValue[0].strip() == name.strip():
            return CookieKeyValue[1]
