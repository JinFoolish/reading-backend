
from mongoengine import connect
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from doc.comment import Article,Similarity
from doc.book import BookInfo
# 连接到MongoDB
connect('recommender_system') 



# 获取所有文章
articles = Article.objects().all() 

# 对文章详细信息进行分词
for article in articles:
    article.detail = ' '.join(jieba.cut(article.detail))

# 计算Tfidf,得到词频矩阵
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform([article.detail for article in articles])

# 计算相似度,得到相似度矩阵
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# 将相似度大于0.3的文章相似度写入MongoDB
for i in range(len(cosine_sim)):
    for j in range(i+1, len(cosine_sim[i])):
        if cosine_sim[i][j] > 0.3:
            sim = Similarity(article_id1=articles[i].id, 
                             article_id2=articles[j].id,
                             score=cosine_sim[i][j]).save() 
            

books = BookInfo.objects().all()
# 对文章详细信息进行分词
for book in books:
    book.introduce = ' '.join(jieba.cut(article.detail))

# 计算Tfidf,得到词频矩阵
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform([book.introduce for book in books])

# 计算相似度,得到相似度矩阵
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


for i in range(len(cosine_sim)):
    for j in range(i+1, len(cosine_sim[i])):
        if cosine_sim[i][j] > 0.3:
            sim = Similarity(book_id1=books[i].id, 
                             book_id2=books[j].id,
                             score=cosine_sim[i][j]).save() 
            
