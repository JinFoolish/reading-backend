
class CommonResponse(object):
    code = 0
    ver = 2
    msg = 'ok'
    data = None

    def as_dict(self):
        return {'code': self.code, 'ver': self.ver, 'msg': self.msg, 'data': self.data}


class PageableResponse(CommonResponse):
    count = 0
    list = []

    def as_dict(self):
        return {'code': self.code, 'msg': self.msg, 'data': {'count': self.count, 'list': self.list}}
    

