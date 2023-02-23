import mongoengine as me

class BookInfo(me.Document):
    user_id = me.StringField()
    sentence = me.StringField(max_length=50)
    # 书的封面
    cover = me.StringField()
    title = me.StringField(max_length=20)
    author = me.StringField(max_length=20)
    category = me.StringField()