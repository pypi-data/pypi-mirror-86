class baseEntry(object):
    def __init__(self,id= '' ,code = '', name = ''):
        self.id = id
        self.code = code
        self.name = name

    def loadFromJson(self, obj):
        self.id = obj['id']
        self.code = obj['code']
        self.name = obj['name']