#
# Getting query param, assuming there can be None-object
#
def getQueryStringParam(flashRequest, param):
    p = flashRequest.args.get(param)
    if None==p:
        return ''
    else:
        return p.strip()
