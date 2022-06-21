import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

if __name__ == "__main__":
    
    placeid='' #추천의 타겟이 되는 장소의 id 입력
    category='' #카테고리명 입력
    filtering='' #휠체어 사용여부에 따른 필터링정보 입력

    data = pd.read_csv(f'{category}.csv')
    data=data.fillna(" ")
    
    placeidx=data[data['id']==int(placeid)].index
    placename=data.loc[placeidx,'place_name']
    
    if(filtering=='1'):
        idx=data[data['wheelchair']=='n'].index
        data.drop(idx, inplace=True)
    
    tfidf_vector = TfidfVectorizer()
    tfidf_matrix = tfidf_vector.fit_transform(data['place_name'] + " " + data['category_name']+ " "+data['keyword']).toarray()
    tfidf_matrix_feature = tfidf_vector.get_feature_names()
    tfidf_matrix = pd.DataFrame(tfidf_matrix, columns=tfidf_matrix_feature, index = data.place_name)
    #장소의 이름, 상세카테고리, 키워드를 tf-idf의 방식으로 벡터값으로 만든다. 

    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, index = data.place_name, columns = data.place_name)
    #장소들 간의 코사인 유사도를 계산한다.
    
    recom_idx = cosine_sim_df.loc[:, placename].values.reshape(1, -1).argsort()[:, ::-1].flatten()[1:6]
    recom_id=data.iloc[recom_idx, :].id.values
    recom_category_code = data.iloc[recom_idx, :].category_group_code.values
    d = {'id' : recom_id, 'category_group_code':recom_category_code}
    df=pd.DataFrame(d)
    #상위 5개의 유사도를 가진 장소를 반환한다.

    df.to_csv(f'rcmd{placeid}.csv',index=False)