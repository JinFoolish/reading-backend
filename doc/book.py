import mongoengine as me
from app.comm.types import BookCategoryEnum
class BookInfo(me.Document):
    user_id = me.StringField()
    sentence = me.StringField(max_length=50)
    # 书的封面
    cover = me.StringField()
    title = me.StringField(max_length=20)
    author = me.StringField(max_length=20)
    introduce = me.StringField(max_length=300)
    category = me.EnumField(BookCategoryEnum)
    rating = me.IntField(min_value=0,max_value=10)
    create_time = me.DateTimeField()