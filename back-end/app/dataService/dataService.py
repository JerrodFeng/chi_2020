# -*- coding: utf-8 -*-
import json
import os
from pymongo import MongoClient
import numpy as np
import pandas as pd
import json
import csv
from collections import Counter# 很重要主要是为了给字典排序

DB_NMAE = 'Dong_chi_2020'
_current_dir = os.path.dirname(os.path.abspath(__file__))

class DataService(object):
    def __init__(self):
        self.emotion_list = ['angry', 'surprise', 'happy', 'neutral', 'sad', 'disgust', 'fear']
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[DB_NMAE]
        return

    def test(self):
        with open(os.path.join(_current_dir, '../data/test.json'), 'r') as rf:
            result = json.load(rf)
        return result

    def lineChart(self):
        with open(os.path.join(_current_dir, '../data/lineChart.json'), 'r') as rf:
            result = json.load(rf)
        return result

    def initialization(self, video_name):
        print('video_name: ', video_name)
        self.video_data = self.readVideoData(video_name)
        self.people_data = self.readPeopleData(video_name)
        # self.video_data = self.genVideoData(video_name)
        # self.people_data = self.genPeopleData(video_name)
        result = {'videoData': self.video_data, 'peopleData': self.people_data}
        return result

    def readVideoData(self, video_name):
        print('readVideoData')
        with open(os.path.join(os.path.dirname(__file__), '../data/{}_videoData.json'.format(video_name)), 'r') as rf:
            result = json.load(rf)
        return result

    def readPeopleData(self, video_name):
        print('readPeopleData')
        with open(os.path.join(os.path.dirname(__file__), '../data/{}_peopleData.json'.format(video_name)), 'r') as rf:
            result = json.load(rf)
        return result

    def printInfo (self):
        with open(os.path.join(_current_dir, '../data/infoData.json'), 'r') as rf:
            result = json.load(rf)
        print('printInfo: ')
        print(result)
        return result
    def drawMDSLasso (self):
        with open(os.path.join(_current_dir, '../data/lassoedDataIndex.json'), 'r') as rf:
            result = json.load(rf)
        # print('coords: ')
        # print(result)
        return result
    
    def fetchArcData (self):
        with open(os.path.join(_current_dir, '../data/arcData.json'), 'r') as rf:
            result = json.load(rf)
        # print('arcData: ')
        # print(result)
        return result 
    def fetchLassoedDataPost (self, lassoedData):
        # 数组
        # print('fromOverView::', lassoedData)
        productViewIndex = []
        tmp = {}
        for i in range(len(lassoedData)):
            tmp['endPeriod']=lassoedData[i]['endPeriod']
            # print('----enperiod----',tmp)
            tmp['item']= lassoedData[i]['item']
            # print('----item----',tmp)
            # print(tmp)
            productViewIndex.append(tmp)
            tmp = {}
            # print('productViewIndex::', productViewIndex, 'tmp::', tmp)
        result = {'data': productViewIndex}
        # result::{'data': [{'endPeriod': 201806, 'item': 'item2352'}, {'endPeriod': 201806, 'item': 'item2352'}]}
        return result
    def fetchLassoedDataFromSimilarityViewPost(self, lassoedDataFromSimilarityView):
        # print('this data is from prductViewPost::', lassoedDataFromSimilarityView)
        # {'SimilarityViewData': {'data': [{'endPeriod': 201805, 'item': 'item2356'}, {'endPeriod': 201805, 'item': 'item2356'}]}}
        # print('changed data::', lassoedDataFromSimilarityView['SimilarityViewData']['data'])
        
        # 求acc
        similarityDataIndex = lassoedDataFromSimilarityView['SimilarityViewData']['data']
        endPeriodDict ={'data': [{'endPeriod': similarityDataIndex[0]['endPeriod']}]}
        collectionKey = {}
        newEndPeriod = {}
        dfItemInfo = []
        # productPresentInfo = {'accuracy': [], 'variance':[], 'applicability':[]}
        for i in range(len(similarityDataIndex)):
            # itemInfo = {'data':[]}
            if similarityDataIndex[i]['endPeriod'] not in endPeriodDict['data']:
                newEndPeriod['endPeriod'] = similarityDataIndex[i]['endPeriod']
                endPeriodDict['data'].append(newEndPeriod)
            month = similarityDataIndex[i]['endPeriod']
            collectionKey = {'data':[{'collection': 'collection_'+str(month)}]}
            collection = self.db[collectionKey['data'][0]['collection']]
            itemResults = collection.find({'item':similarityDataIndex[i]['item']})#.sort('accuracy', -1)
            for itemResult in itemResults:
                if float(itemResult['accuracy'])>-0.01:
                    itemResult['endPeriod'] = similarityDataIndex[i]['endPeriod']
                    itemResult['_id'] = ''
                    dfItemInfo.append(itemResult)
        dfItemInfo = pd.DataFrame(dfItemInfo)

        modelName= ["GMNR", "ada", "arima", "arimax", "cat", "elnet", "extra", "gbdt", "knn", "lasso", "lgb", "lr", "myarima", "myarimax", "rf", "ridge", "svr", "xgb", "arima_ts", "exps_ts", "myarima_ts", "lstm_classic", "maml", "rl2", "rnn_classic"]
        models = {'models': modelName}
        ModelAcc = []
        for i in range(len(modelName)):
            tmp = {}
            dfModelAcc = dfItemInfo.loc[dfItemInfo.model == models['models'][i]]
            dfModelAcc['accuracy'] = pd.to_numeric(dfModelAcc['accuracy'],errors='coerce')
            acc = dfModelAcc['accuracy'].mean(axis = 0)
            tmp['model'] = models['models'][i]
            tmp['acc'] = acc
            ModelAcc.append(tmp)
        lassoedDataModelAccList = sorted(ModelAcc, key=lambda k: k['acc'], reverse=True)
        # print(lassoedDataModelAccList)
        lassoedDataModelAccDict = {'lassoedDataModelAcc':lassoedDataModelAccList}
        dfLassoedDataModelAccList = pd.DataFrame(lassoedDataModelAccList)
        # print(lassoedDataModelAccDict)

        # 求 variance# variance 进行计算  最终版
        monthArray = [201708, 201709, 201710, 201711, 201712, 201801, 201802, 201803, 201804, 201805, 201806, 201807]
        modelName= ["GMNR", "ada", "arima", "arimax", "cat", "elnet", "extra", "gbdt", "knn", "lasso", "lgb", "lr", "myarima", "myarimax", "rf", "ridge", "svr", "xgb", "arima_ts", "exps_ts", "myarima_ts", "lstm_classic", "maml", "rl2", "rnn_classic"]
        models = {'models': modelName}
        # 统计次数构造全0
        modelRankDict = {}
        for i in range(len(modelName)):
            modelRankDict[modelName[i]] = 0
        similarityDataIndex = lassoedDataFromSimilarityView['SimilarityViewData']['data']
        endPeriodDict ={'data': [{'endPeriod': similarityDataIndex[0]['endPeriod']}]}
        # endPeriodDict.append(201909)
        # print(type(endPeriodDict['data']))
        collectionKey = {}
        newEndPeriod = {}
        modelVariance = {}
        tmpVariance ={}
        lassoedDataSummary = []
        # lassoedDataInfo = {'data':[]}
        # productPresentInfo = {'accuracy': [], 'variance':[], 'applicability':[]}
        for i in range(len(similarityDataIndex)):
            print('=========',i,'========',similarityDataIndex[i]['item'],'=================')
            lassoPointInfo = []
            if similarityDataIndex[i]['endPeriod'] not in endPeriodDict['data']:
                newEndPeriod['endPeriod'] = similarityDataIndex[i]['endPeriod']
                endPeriodDict['data'].append(newEndPeriod)
            month = similarityDataIndex[i]['endPeriod']
            collectionKey = {'data':[{'collection': 'collection_'+str(month)}]}
            collection = self.db[collectionKey['data'][0]['collection']]
            # 第一次找无所谓判断是否在，肯定在
            lassoPointResults = collection.find({'item':similarityDataIndex[i]['item']})#.sort('accuracy', -1)
            # if eachMonthResults.count()!=0:
            for lassoPointResult in lassoPointResults:
                lassoPointResult['endPeriod'] = similarityDataIndex[i]['endPeriod']
                if float(lassoPointResult['accuracy'])>-0.01:
                    # print(lassoPointResult['accuracy'])
                    lassoPointInfo.append(lassoPointResult)
            if len(lassoPointInfo) != 0:
                dfLassoPointInfo = pd.DataFrame(lassoPointInfo)           
                modelItemVar = []
                # print('-********',dfLassoPointInfo['item'],'********')
                
                for j in range(dfLassoPointInfo.shape[0]):
                    endPeriod = dfLassoPointInfo.iloc[j]['endPeriod']
                    monthIndex = monthArray.index(endPeriod)
                    tmpAcc = []
                    for p in range(10):
                        currentMonth = monthArray[monthIndex-p]
            #             print('------',currentMonth,'-------')
                        collectionKey = {'data':[{'collection': 'collection_'+str(currentMonth)}]}
                        collection = self.db[collectionKey['data'][0]['collection']]
                        # existItemResults = collection.distinct('item')
                        # for existItemResult in existItemResults:

                        eachMonthResults= collection.find({'$and':[{'item':dfLassoPointInfo.iloc[j]['item']},{'model':dfLassoPointInfo.iloc[j]['model']}]})
                        eachCollectionAcc = []
                        if eachMonthResults.count()!=0:
                            for eachMonthResult in eachMonthResults:
                                if float(eachMonthResult['accuracy'])>-0.01:
                                    # print(eachMonthResult['accuracy'])
                                    eachCollectionAcc.append(eachMonthResult['accuracy'])
                            tmp =np.array(eachCollectionAcc)
                            tmp = tmp.astype(float)
                            # np.where(tmp>-0.01)
                            eachMonthMeanAcc = np.nanmean(tmp)
                            tmpAcc.append(eachMonthMeanAcc)
                        # else:
                        #     print('@@@@@@@@@@@@@@@@@@@@@@@')
                    # print(tmpAcc)
                    eachLassoedPointModelItemVar = np.nanvar((np.array(tmpAcc)).astype(float))
                    modelItemVar.append(eachLassoedPointModelItemVar)
                    np.array(modelItemVar)
                dfLassoPointInfo.insert(7,'modelItemVar', modelItemVar)
                for m in range(dfLassoPointInfo.shape[0]):
                    if i == 0:
                        tmpVariance[dfLassoPointInfo.iloc[m]['model']] =[dfLassoPointInfo.iloc[m]['modelItemVar']]
        #                 modelVariance.append(tmpVariance)
                    else:
                        tmpVariance[dfLassoPointInfo.iloc[m]['model']].append(dfLassoPointInfo.iloc[m]['modelItemVar'])  
                        # dfModelItemVar = dfLassoPointInfo[['model', 'item', 'modelItemVar', ]]
                # print('+++++variance++++',modelItemVar )
                dfLassoPointInfoDescending = dfLassoPointInfo.sort_values(by='accuracy', ascending=False)
                lassoPointInfoDescendingDict = dfLassoPointInfoDescending.to_dict(orient='records')
                # print('%%%%%%%%%%%%',lassoPointInfoDict)
                for q in range(5):
                    tmpModel = dfLassoPointInfoDescending.iloc[q]['model']
                    modelRankDict[tmpModel]=modelRankDict[tmpModel]+1
                # lassoPointInfoDescending
                dfLassoPointInfoDescending= dfLassoPointInfoDescending.loc[:,['item', 'endPeriod', 'model','accuracy', 'modelItemVar', 'predictValue', 'realValue' ]]
                lassoPointInfoDescendingDict = dfLassoPointInfoDescending.to_dict(orient='records')
                # print(lassoPointInfoDescendingDict)
                tmpLassoPointInfoDescendingDict = {}
                tmpLassoPointInfoDescendingDict['item'] = lassoPointInfoDescendingDict[0]['item']
                tmpLassoPointInfoDescendingDict['endPeriod'] = lassoPointInfoDescendingDict[0]['endPeriod']
                for w in range(len(lassoPointInfoDescendingDict)):
                    if w == 0:                
                        keys = ('model','accuracy', 'modelItemVar', 'predictValue', 'realValue')
                        tmpLassoPointInfoModel =  {k: lassoPointInfoDescendingDict[w][k] for k in keys}
                        tmpLassoPointInfoDescendingDict['model'] = [tmpLassoPointInfoModel]
                    else:
                        keys = ('model','accuracy', 'modelItemVar', 'predictValue', 'realValue')
                        tmpLassoPointInfoModel =  {k: lassoPointInfoDescendingDict[w][k] for k in keys}                
                        tmpLassoPointInfoDescendingDict['model'].append(tmpLassoPointInfoModel)
                lassoedDataSummary.append(tmpLassoPointInfoDescendingDict)    

                # print(lassoPointInfoDescendingDict)
        modelRankDict=dict(Counter(modelRankDict).most_common())         
        # print(modelRankDict)  
        for i in range(len(modelName)):
            modelVariance[modelName[i]]=np.mean(tmpVariance[modelName[i]])
        # print('+++++',modelVariance,'++++')
        modelInfo = []
        for i in range( len(modelName)):
            tmpModelInfo = {}
            tmpModelInfo['modelName'] = modelName[i]
            tmp = dfLassoedDataModelAccList.loc[(dfLassoedDataModelAccList['model']==modelName[i]),['acc']].values
            tmpModelInfo['accuracy'] = tmp[0][0]
            tmpModelInfo['variance'] = modelVariance[modelName[i]]
            tmpModelInfo['topRank'] = modelRankDict[modelName[i]]
            modelInfo.append(tmpModelInfo)
        print(modelInfo)
        print('----------分割线-------------')
        print(lassoedDataSummary)
        result = {'modelInfomation': modelInfo, 'lassoedDataInformation': lassoedDataSummary}



        # result = {'data':{ {'Acc':lassoedDataModelAccDict}, {'Variance': lassoPointInfoDict}, {'ModelRank': modelRankDict}}}
        # print(result)
        
        print('finish')
        return result

        
    
if __name__ == '__main__':
    print('start')
    dataService = DataService()
    result = dataService.test()
    print(result)

    result = dataService.initialization('BabyFace1_S01E01')
    print(result)
    # print('MongoClient: ', MongoClient)
