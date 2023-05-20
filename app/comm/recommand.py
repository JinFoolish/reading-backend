from doc.comment import Similarity
def recommend(similarity_matrix:list[list], user_likes:list, list_of_items:list):
    # 得到用户喜欢物品的索引
    user_likes_idx = [list_of_items.index(item) for item in user_likes]
    
    # 为所有物品初始化一个推荐度列表
    recommendation_scores = [0 for item in list_of_items]
    
    # 遍历用户喜欢的物品
    for item_idx in user_likes_idx:
        # 找到该物品的相似度行
        similar_items = similarity_matrix[item_idx]
        
        # 为相似的物品增加推荐度
        for i in range(len(similar_items)):
            if similar_items[i] > 0.5:
                recommendation_scores[i] += similar_items[i]
                
    # 得到推荐列表                
    recommendations = sorted(enumerate(recommendation_scores), 
                            key=lambda x: x[1], reverse=True)
    
    return recommendations

def sort_dict(d):
    return sorted(d, key=d.get, reverse=True)

def recom(article_ids:list):
    sim_dic = {}
    for article_id in article_ids:
        similaritys = Similarity.objects(article_id1=article_id)
        for similarity in similaritys:
            article_id2 = similarity.article_id2
            score = similarity.score
            if sim_dic.get(article_id2) is None:
                sim_dic[article_id2] = score
            else :
                sim_dic[article_id2] = sim_dic[article_id2]+score
    return sort_dict(sim_dic)