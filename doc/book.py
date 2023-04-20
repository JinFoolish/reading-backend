import mongoengine as me

class BookInfo(me.Document):
    user_id = me.StringField()
    sentence = me.StringField(max_length=50)
    # 书的封面
    cover = me.StringField()
    title = me.StringField(max_length=20)
    author = me.StringField(max_length=20)
    introduce = me.StringField(max_length=300)
    category = me.StringField(max_length=20)
    rating = me.IntField(min_value=0,max_value=5)
    create_time = me.DateTimeField()