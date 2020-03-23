# -*- coding: utf-8 -*-
"""
Created on Sun May  5 11:01:11 2019

@author: Lestat

包含K最近邻分类器及K最近邻回归分析，K-Means聚类，线性回归四种回归分析算法，save()和load()用于保存和加载算法模型
"""
import numpy as np
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib


# 按目标值y计算K最近邻回归及K最近领分类
def kneighbors(X, y, n, model_type='classifier'):
    # 使用y作为目标值拟合数据
    # X, y: X需要计算的维度数据, y每条数据的目标值(标签值当为数值类型)
    # n: K
    # model_type: classifier--返回分类模型, regressor--返回回归模型
    # return K-Means model
    X, y = np.array(X), np.array(y)
    if model_type == 'classifier':
        neigh = KNeighborsClassifier(n_neighbors=n)
        neigh.fit(X, y)
        return neigh
    elif model_type == 'regressor':
        neigh = KNeighborsRegressor(n_neighbors=n)
        neigh.fit(X, y)
        return neigh

# K-Means聚类
def kmeans(X, n_clusters):
    # 对样本X进行聚类，X中列数必须大于2列
    X = np.array(X)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
    """
    kmeans: .predict() ;.labels_ ;.cluster_centers_
    """
    
    return kmeans


# LinearRegression
def linear_regression(X, y):
    
    X, y = np.array(X), np.array(y)
    reg = LinearRegression()
    reg.fit(X, y)
    # reg: reg.coef_:模型偏置系数[b1,b2,b3,...]; reg.intercept_:模型偏置截距c
    # y = b1*x_1+b2*x_2+b3*x_3+...+c
    
    return reg


def predict(model, X):
    y = model.predict(X)
    return y


def save(model, path=['train.m']):
    #保存模型
    joblib.dump(model, path)

def load(path):
    # 加载模型
    return joblib.load(path)

# Help
def help():
    print('-'*80,'\n','kneighbors: X:[[x00,x01,x02,...], [x10,x11,x12,...],...];\ny:[y0,y1,...];\n'\
          'model_type: classifier(分类)/regressor(回归)\n\n'\
          'kmeans: X-[[x00,x01,...],[x10,x11,...],...], n_clusters-目标聚簇数'
          'linear_regression: Ibid.\n'\
          ''
          )


if __name__ == '__main__':
#    拟合线性模型
    X = [[121.178238661025], [121.178238661025], [121.061017795139], [121.052313096789], [121.159051920573], [121.090329589844], [121.090329589844], [121.090329589844], [121.090329589844], [121.090329589844], [121.090329589844], [121.090329589844], [121.068244357639], [121.068244357639], [121.073049316407], [30.142063802084], [30.142063802084], [30.151528862848], [30.168381347657], [30.035534667969], [30.096067979601], [30.096067979601], [30.096067979601], [30.096067979601], [30.096067979601], [30.096067979601], [30.096067979601], [30.228468695747], [30.228468695747], [29.892603081598]]
    y = [[121.182658420139], [121.182658420139], [121.065501302084], [121.05677842882], [121.16350124783], [121.094847276476], [121.094847276476], [121.094847276476], [121.094847276476], [121.094847276476], [121.094847276476], [121.094847276476], [121.072747938369], [121.072747938369], [121.077532552084], [30.139698350695], [30.139698350695], [30.149234754775], [30.166071777344], [30.033203667535], [30.093802083334], [30.093802083334], [30.093802083334], [30.093802083334], [30.093802083334], [30.093802083334], [30.093802083334], [30.226188964844], [30.226188964844], [29.890320638021]]
    model_lng = linear_regression(X[:15], y[:15])
    model_lat = linear_regression(X[15:], y[15:])
    
    print('y = {0} * X + {1}'.format(model_lng.coef_[0][0], model_lng.intercept_))
    print('y = {0} * X + {1}'.format(model_lat.coef_[0][0], model_lat.intercept_))
    
    print(predict(model_lng, [[121.073049316407]]))

#==============================================================================
#    K最近邻分类器及K最近邻回归预测
    X2 = [[1.1,1.1], [1.5,1.5], [2.3,2.2], [2.6,2.4], [5.9,5.3]
    , [5.1,5.5], [2.9,2.4], [6.7,6.2], [6.4,6.5], [8.1, 8]
    , [3.3, 3.5], [4.5,4.1], [7.2, 7.5], [9.9,9.8], [10.1,10]
    , [9.1, 9.5], [10.5,10.1]]
    y2 = [[1], [1], [1], [1], [2]
    , [2], [1], [2], [2], [2]
    , [1], [2], [2], [3], [3]
    , [3], [3]]
    
    classifier_model = kneighbors(X2, y2, 3)
#    save(classifier_model, 'classifier_model.m')
#    
#    classifier_model = load('classifier_model.m')
#    print(classifier_model.kneighbors())
    print(predict(classifier_model, [[9.3,8.5]]))
    print(classifier_model.predict_proba([[9.3,8.5]]))
    regressor_model = kneighbors(X2, y2, 3, model_type='regressor')
    print(predict(regressor_model, [[9.3,8.5]]))
#==============================================================================
#    K-Means聚类
    X = [[1.1,1.1], [1.5,1.5], [2.3,2.2], [2.6,2.4], [5.9,5.3]
    , [5.1,5.5], [2.9,2.4], [6.7,6.2], [6.4,6.5], [8.1, 8]
    , [3.3, 3.5], [4.5,4.1], [7.2, 7.5], [9.9,9.8], [10.1,10]
    , [9.1, 9.5], [10.5,10.1]]
    kmeans = kmeans(X, n_clusters=3)
    print(kmeans.labels_)
    print(kmeans.cluster_centers_)
    print(kmeans.predict([[2.5,3.6]]))
    
