import mongoengine as me

class BookInfo(me.Document):
    user_id = me.StringField()
    sentence = me.StringField(max_length=1000)
    # 书的封面
    cover = me.StringField()
    title = me.StringField(max_length=200)
    author = me.StringField(max_length=200)
    introduce = me.StringField(max_length=3000)
    category = me.StringField(max_length=20)
    rating = me.IntField(min_value=0,max_value=5)
    create_time = me.DateTimeField()

class BookSim(me.Document):
    book_id1 = me.StringField()
    book_id2 = me.StringField()
    scrore = me.FloatField()