import mongoengine as me

class User(me.Document):
    openid = me.StringField(unique=True)
    username = me.StringField()
    # 头像url
    avatar = me.StringField()
    city = me.StringField()
    country = me.StringField()


class UserFollow(me.Document):
    user_id = me.StringField()
    follow_id = me.StringField()


class UserBook(me.Document):
    user_id = me.StringField()
    book_id = me.StringField()