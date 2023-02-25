import mongoengine as me

class Article(me.Document):
    user_id = me.StringField()
    create_time = me.DateTimeField()
    detail = me.StringField(max_length=500)
    images = me.ListField(me.StringField())
    book_title = me.StringField(max_length=20)
    book_id = me.StringField()


class LikeArticle(me.Document):
    user_id = me.StringField()
    article_id = me.StringField()


class ArticleComment(me.Document):
    user_id = me.StringField()
    comment = me.StringField(max_length=200)
    article_id = me.StringField()
    create_time = me.DateTimeField()

class LikeComment(me.Document):
    user_id = me.StringField()
    comment_id = me.StringField()


