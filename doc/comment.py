import mongoengine as me

class Article(me.Document):
    user_id = me.StringField()
    create_time = me.DateTimeField()
    detail = me.StringField(max_length=5000)
    images = me.ListField(me.StringField())
    book_title = me.StringField(max_length=200)
    book_id = me.StringField()


class LikeArticle(me.Document):
    user_id = me.StringField()
    article_id = me.StringField()


class ArticleComment(me.Document):
    user_id = me.StringField()
    comment = me.StringField(max_length=2000)
    article_id = me.StringField()
    create_time = me.DateTimeField()

class LikeComment(me.Document):
    user_id = me.StringField()
    comment_id = me.StringField()


# 定义相似度Schema
class Similarity(me.Document):
    article_id1 = me.StringField()
    article_id2 = me.StringField()
    score = me.FloatField()