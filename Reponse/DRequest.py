def DRequest(request, name):
    RequestLineSplit = request.split('\n')

    Result = []
    for requestLine in RequestLineSplit:
        if name in requestLine:
            cleaned = requestLine.replace(name+":", "").strip()
            Result.append(cleaned)

    if(len(Result)>1):
        return Result
    else:
        return Result[0]