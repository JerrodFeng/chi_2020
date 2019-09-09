# -*- coding: utf-8 -*-
import json
import os
from pymongo import MongoClient
import numpy as np
import pandas as pd
import csv
from collections import Counter# 很重要主要是为了给字典排序

import random

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import adfuller

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

    def fetchLassoedDataFromSimilarityViewPost2(self, lassoedDataFromSimilarityView):
        # print('this data is from prductViewPost::', lassoedDataFromSimilarityView)
        # {'SimilarityViewData': {'data': [{'endPeriod': 201805, 'item': 'item2356'}, {'endPeriod': 201805, 'item': 'item2356'}]}}
        # print('changed data::', lassoedDataFromSimilarityView['SimilarityViewData']['data'])
        
        similarityDataIndex = lassoedDataFromSimilarityView['SimilarityViewData']['data']
        endPeriodDict ={'data': [{'endPeriod': similarityDataIndex[0]['endPeriod']}]}
        collectionKey = {}
        newEndPeriod = {}
        dfItemInfo = []
        predictMonth = 201807
        for i in range(len(similarityDataIndex)):
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
        dfItemInfo = pd.DataFrame(dfItemInfo) #所有lasso点的信息每个点25条数据

        modelName= ["GMNR", "ada", "arima", "arimax", "cat", "elnet", "extra", "gbdt", "knn", "lasso", "lgb", "lr", "myarima", "myarimax", "rf", "ridge", "svr", "xgb", "arima_ts", "exps_ts", "myarima_ts", "lstm_classic", "maml", "rl2", "rnn_classic"]
        models = {'models': modelName}
        ModelAcc = []
        ModelVar = []
        for i in range(len(modelName)):
            tmp = {}
            dfModelAcc = dfItemInfo.loc[(dfItemInfo.model == models['models'][i])&(dfItemInfo.endPeriod != predictMonth)]
            dfModelAcc['accuracy'] = pd.to_numeric(dfModelAcc['accuracy'],errors='coerce')
            acc = dfModelAcc['accuracy'].mean(axis = 0)
            var = dfModelAcc['accuracy'].var(axis = 0)
            tmp['model'] = models['models'][i]
            tmp['acc'] = acc
            tmp['variance'] = var
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
        collectionKey = {}
        newEndPeriod = {}
        # modelVariance = {}
        tmpVariance ={}
        lassoedDataSummary = []   
        for i in range(len(similarityDataIndex)):
            print('=========',i,'========',similarityDataIndex[i]['item'],'=================')
            lassoPointInfo = []
            if similarityDataIndex[i]['endPeriod'] not in endPeriodDict['data']:
                newEndPeriod['endPeriod'] = similarityDataIndex[i]['endPeriod']
                endPeriodDict['data'].append(newEndPeriod)
            month = similarityDataIndex[i]['endPeriod']
            collectionKey = {'data':[{'collection': 'collection_'+str(month)}]}
            collection = self.db[collectionKey['data'][0]['collection']]
            lassoPointResults = collection.find({'item':similarityDataIndex[i]['item']})#.sort('accuracy', -1)
            for lassoPointResult in lassoPointResults:
                lassoPointResult['endPeriod'] = similarityDataIndex[i]['endPeriod']
                if float(lassoPointResult['accuracy'])>-0.01:
                    # print(lassoPointResult['accuracy'])
                    lassoPointInfo.append(lassoPointResult)
            if len(lassoPointInfo)!= 0:
                dfLassoPointInfo = pd.DataFrame(lassoPointInfo)           
                modelItemVar = []
                # print('-********',dfLassoPointInfo['item'],'********')
                for j in range(dfLassoPointInfo.shape[0]):
                    endPeriod = dfLassoPointInfo.iloc[j]['endPeriod']
                    monthIndex = monthArray.index(endPeriod)
                    tmpAcc = []
                    for p in range(10):
                        currentMonth = monthArray[monthIndex-p]
                        collectionKey = {'data':[{'collection': 'collection_'+str(currentMonth)}]}
                        collection = self.db[collectionKey['data'][0]['collection']]
                        eachMonthResults= collection.find({'$and':[{'item':dfLassoPointInfo.iloc[j]['item']},{'model':dfLassoPointInfo.iloc[j]['model']}]})
                        eachCollectionAcc = []
                        if eachMonthResults.count()!=0:
                            for eachMonthResult in eachMonthResults:
                                if float(eachMonthResult['accuracy'])>-0.01:
                                    eachCollectionAcc.append(eachMonthResult['accuracy'])
                            tmp =np.array(eachCollectionAcc)
                            tmp = tmp.astype(float)
                            eachMonthMeanAcc = np.nanmean(tmp)
                            tmpAcc.append(eachMonthMeanAcc)
                    eachLassoedPointModelItemVar = np.nanvar((np.array(tmpAcc)).astype(float))
                    modelItemVar.append(eachLassoedPointModelItemVar)
                    np.array(modelItemVar)
                dfLassoPointInfo.insert(7,'modelItemVar', modelItemVar)
                for m in range(dfLassoPointInfo.shape[0]):
                    if i == 0:
                        tmpVariance[dfLassoPointInfo.iloc[m]['model']] =[dfLassoPointInfo.iloc[m]['modelItemVar']]
                    else:
                        tmpVariance[dfLassoPointInfo.iloc[m]['model']].append(dfLassoPointInfo.iloc[m]['modelItemVar'])  
                # print('+++++variance++++',modelItemVar )
                dfLassoPointInfoDescending = dfLassoPointInfo.sort_values(by='accuracy', ascending=False)
                lassoPointInfoDescendingDict = dfLassoPointInfoDescending.to_dict(orient='records')
                if lassoPointInfoDescendingDict[0]['endPeriod'] != predictMonth:
                    for q in range(5):
                        tmpModel = dfLassoPointInfoDescending.iloc[q]['model']
                        modelRankDict[tmpModel]=modelRankDict[tmpModel]+1
                dfLassoPointInfoDescending= dfLassoPointInfoDescending.loc[:,['item', 'endPeriod', 'model','accuracy', 'modelItemVar', 'predictValue', 'realValue' ]]
                lassoPointInfoDescendingDict = dfLassoPointInfoDescending.to_dict(orient='records')
                # print(lassoPointInfoDescendingDict)
                tmpLassoPointInfoDescendingDict = {}
                tmpLassoPointInfoDescendingDict['item'] = lassoPointInfoDescendingDict[0]['item']
                tmpLassoPointInfoDescendingDict['endPeriod'] = lassoPointInfoDescendingDict[0]['endPeriod']
                for w in range(len(lassoPointInfoDescendingDict)):
                    if w == 0:                
                        keys = ('model','accuracy', 'modelItemVar', 'predictValue', 'realValue', 'endPeriod', 'item')
                        tmpLassoPointInfoModel =  {k: lassoPointInfoDescendingDict[w][k] for k in keys}
                        tmpLassoPointInfoDescendingDict['model'] = [tmpLassoPointInfoModel]
                    else:
                        keys = ('model','accuracy', 'modelItemVar', 'predictValue', 'realValue', 'endPeriod', 'item')
                        tmpLassoPointInfoModel =  {k: lassoPointInfoDescendingDict[w][k] for k in keys} 
                        # if w%2 ==0:
                        tmpLassoPointInfoDescendingDict['model'].append(tmpLassoPointInfoModel)
                lassoedDataSummary.append(tmpLassoPointInfoDescendingDict)    

                # print(lassoPointInfoDescendingDict)
        modelRankDict=dict(Counter(modelRankDict).most_common())         
        print(modelRankDict)  
        tmpmaxModelVarianceList = []
        for i in range(len(lassoedDataModelAccDict['lassoedDataModelAcc'])):
            tmpmaxModelVarianceList.append(lassoedDataModelAccDict['lassoedDataModelAcc'][i]['variance'])
        maxModelVariance = max(tmpmaxModelVarianceList)
        print('maxModelVariance: ', maxModelVariance)
        # print('+++++',modelVariance,'++++')
        modelInfo = []
        for i in range( len(modelName)):
            tmpModelInfo = {}
            tmpModelInfo['modelName'] = modelName[i]
            tmp = dfLassoedDataModelAccList.loc[(dfLassoedDataModelAccList['model']==modelName[i]),['acc']].values
            tmpVarianceLast = dfLassoedDataModelAccList.loc[(dfLassoedDataModelAccList['model']==modelName[i]),['variance']].values
            tmpModelInfo['accuracy'] = tmp[0][0]
            tmpModelInfo['variance'] = tmpVarianceLast[0][0]/maxModelVariance
            tmpModelInfo['topRank'] = (modelRankDict[modelName[i]])/max(modelRankDict.values())
            modelInfo.append(tmpModelInfo)
        # print(modelInfo)
        # print('----------fengexian-------------')
        # print(lassoedDataSummary)
        result = {'modelInformation': modelInfo, 'lassoedDataInformation': lassoedDataSummary}


        print('finish')
        return result

    def fetchLassoedDataFromSimilarityViewPost(self, lassoedDataFromSimilarityView):
        similarityDataIndex = lassoedDataFromSimilarityView['SimilarityViewData']['data']
        endPeriodDict ={'data': [{'endPeriod': similarityDataIndex[0]['endPeriod']}]}
        collectionKey = {}
        newEndPeriod = {}
        dfItemInfo = []
        predictMonth = 201807
        for i in range(len(similarityDataIndex)):
            if similarityDataIndex[i]['endPeriod'] not in endPeriodDict['data']:
                newEndPeriod['endPeriod'] = similarityDataIndex[i]['endPeriod']
                endPeriodDict['data'].append(newEndPeriod)
            month = similarityDataIndex[i]['endPeriod']
            collectionKey = {'data':[{'collection': 'collection_'+str(month)}]}
            collection = self.db[collectionKey['data'][0]['collection']]
            itemResults = collection.find({'item':similarityDataIndex[i]['item']})
            for itemResult in itemResults:
                if float(itemResult['accuracy'])>-0.01:
                    itemResult['endPeriod'] = similarityDataIndex[i]['endPeriod']
                    itemResult['_id'] = ''
                    dfItemInfo.append(itemResult)
        dfItemInfo = pd.DataFrame(dfItemInfo) #所有lasso点的信息每个点25条数据

        modelName= ["GMNR", "ada", "arima", "arimax", "cat", "elnet", "extra", "gbdt", "knn", "lasso", "lgb", "lr", "myarima", "myarimax", "rf", "ridge", "svr", "xgb", "arima_ts", "exps_ts", "myarima_ts", "lstm_classic", "maml", "rl2", "rnn_classic"]
        models = {'models': modelName}
        ModelAcc = []
        for i in range(len(modelName)):
            tmp = {}
            dfModelAcc = dfItemInfo.loc[(dfItemInfo.model == models['models'][i])&(dfItemInfo.endPeriod != predictMonth)]
            dfModelAcc['accuracy'] = pd.to_numeric(dfModelAcc['accuracy'],errors='coerce')
            acc = dfModelAcc['accuracy'].mean(axis = 0)
            var = dfModelAcc['accuracy'].var(axis = 0)
            tmp['model'] = models['models'][i]
            tmp['acc'] = acc
            tmp['variance'] = var
            ModelAcc.append(tmp)    
        lassoedDataModelAccList = sorted(ModelAcc, key=lambda k: k['acc'], reverse=True)
        # print(lassoedDataModelAccList)
        lassoedDataModelAccDict = {'lassoedDataModelAcc':lassoedDataModelAccList}
        dfLassoedDataModelAccList = pd.DataFrame(lassoedDataModelAccList)
        # print(lassoedDataModelAccDict)

        # 求 variance# variance 
        monthArray = [201708, 201709, 201710, 201711, 201712, 201801, 201802, 201803, 201804, 201805, 201806, 201807]
        modelName= ["GMNR", "ada", "arima", "arimax", "cat", "elnet", "extra", "gbdt", "knn", "lasso", "lgb", "lr", "myarima", "myarimax", "rf", "ridge", "svr", "xgb", "arima_ts", "exps_ts", "myarima_ts", "lstm_classic", "maml", "rl2", "rnn_classic"]
        models = {'models': modelName}
        # 统计次数构造全0
        modelRankDict = {}
        for i in range(len(modelName)):
            modelRankDict[modelName[i]] = 0
        similarityDataIndex = lassoedDataFromSimilarityView['SimilarityViewData']['data']
        endPeriodDict ={'data': [{'endPeriod': similarityDataIndex[0]['endPeriod']}]}
        collectionKey = {}
        newEndPeriod = {}
        lassoedDataSummary = []
        # similarityDataIndex     [{'endPeriod': 201807, 'item': 'item2210'},{'endPeriod': 201807, 'item': 'item2283'}]
        for i in range(len(similarityDataIndex)):
            print('=========',i,'========',similarityDataIndex[i]['item'],'=================')
            lassoPointInfo = []
            collection = self.db['lassoedDataInformation']
            results= collection.find({'$and':[{'item':similarityDataIndex[i]['item']},{'endPeriod':similarityDataIndex[i]['endPeriod']}]})
            if results.count()!=0:  
                for result in results:
                    result.pop('_id')
                    lassoPointInfo.append(result)     
                dfLassoPointInfoDescending = pd.DataFrame(lassoPointInfo[0]['model'])

                if lassoPointInfo[0]['model'][0]['endPeriod'] != predictMonth:
                    for q in range(5):
                        tmpModel = dfLassoPointInfoDescending.iloc[q]['model']
                        modelRankDict[tmpModel]=modelRankDict[tmpModel]+1
                # lassoPointInfoDescending
                dfLassoPointInfoDescending= dfLassoPointInfoDescending.loc[:,['item', 'endPeriod', 'model','accuracy', 'modelItemVar', 'predictValue', 'realValue' ]]
                lassoPointInfoDescendingDict = dfLassoPointInfoDescending.to_dict(orient='records')
                tmpValue = {}
                tmpValue['model'] = lassoPointInfoDescendingDict
                tmpValue['item']=lassoPointInfoDescendingDict[0]['item']
                tmpValue['endPeriod']=lassoPointInfoDescendingDict[0]['endPeriod']
                if i == 0:
                    lassoedDataSummary = [tmpValue]
                else:
                    lassoedDataSummary.append(tmpValue)
                # print(lassoPointInfoDescendingDict)

                
        modelRankDict=dict(Counter(modelRankDict).most_common())         
        print(modelRankDict)  
        tmpmaxModelVarianceList = []
        for i in range(len(lassoedDataModelAccDict['lassoedDataModelAcc'])):
            tmpmaxModelVarianceList.append(lassoedDataModelAccDict['lassoedDataModelAcc'][i]['variance'])
        maxModelVariance = max(tmpmaxModelVarianceList)
        # print('+++++',modelVariance,'++++')
        modelInfo = []
        for i in range( len(modelName)):
            tmpModelInfo = {}
            tmpModelInfo['modelName'] = modelName[i]
            tmp = dfLassoedDataModelAccList.loc[(dfLassoedDataModelAccList['model']==modelName[i]),['acc']].values
            tmpVarianceLast = dfLassoedDataModelAccList.loc[(dfLassoedDataModelAccList['model']==modelName[i]),['variance']].values
            tmpModelInfo['accuracy'] = tmp[0][0]
            tmpModelInfo['variance'] = tmpVarianceLast[0][0]/maxModelVariance
            tmpModelInfo['topRank'] = (modelRankDict[modelName[i]])/max(modelRankDict.values())
            modelInfo.append(tmpModelInfo)

        result = {'modelInformation': modelInfo, 'lassoedDataInformation': lassoedDataSummary, 'maxModelVariance': maxModelVariance}
        print('finish')
        return result

    def getDetailViewData(self, selectedItem, topKModels):
        modelPerformanceData = []
        # generate the model accuracy data
        for modelIndex in range(0, len(topKModels)):
            currentModelPerformance = {}
            currentModel = topKModels[modelIndex]
            currentModelPerformance['model'] = currentModel
            currentModelPerformance['accuracy'] = []
            beginNoneNumber = random.randint(0, 4)
            endNoneNumber = random.randint(0, 2)
            middleNumber = 10 - beginNoneNumber - endNoneNumber

            for i in range(0, beginNoneNumber):
                currentModelPerformance['accuracy'].append({
                    'model': currentModel,
                    'index': i,
                    'accuracy': -1
                })
            for i in range(beginNoneNumber, beginNoneNumber + middleNumber):
                currentModelPerformance['accuracy'].append({
                    'model': currentModel,
                    'index': i,
                    'accuracy': random.randint(50, 100) / 100
                })
            for i in range(beginNoneNumber + middleNumber, 10):
                currentModelPerformance['accuracy'].append({
                    'model': currentModel,
                    'index': i,
                    'accuracy': -1
                })

            modelPerformanceData.append(currentModelPerformance)

        # generate the real demand and historical demand
        monthNumber = random.randint(30, 43)

        print('monthNumber: ', monthNumber)

        demandData = []

        historicalDemand = {}
        historicalDemand['type'] = 'real'
        historicalDemand['demand'] = []
        for monthIndex in range(0, monthNumber):
            historicalDemand['demand'].append({
                'type': 'real',
                'index': monthIndex,
                'demand': random.randint(50, 100) / 100
            })

        if selectedItem['endPeriod'] == 201807:
            historicalDemand['demand'][len(historicalDemand['demand']) - 1]['demand'] = None

        demandData.append(historicalDemand)

        for modelIndex in range(0, len(topKModels)):
            currentModelForecastedDemand = {}
            currentModel = topKModels[modelIndex]

            currentModelForecastedDemand['type'] = currentModel
            currentModelForecastedDemand['demand'] = []

            forecastedDemandNumber = random.randint(5, 10)
            print('forecastedDemandNumber: ', forecastedDemandNumber)

            for monthIndex in range(0, monthNumber - forecastedDemandNumber):
                currentModelForecastedDemand['demand'].append({
                    'type': currentModel,
                    'index': monthIndex,
                    'demand': None
                })
            for monthIndex in range(monthNumber - forecastedDemandNumber, monthNumber):
                currentModelForecastedDemand['demand'].append({
                    'type': currentModel,
                    'index': monthIndex,
                    'demand': random.randint(50, 100) / 100
                })

            demandData.append(currentModelForecastedDemand)

        return {
                'modelPerformanceData': modelPerformanceData, 
                'demandData': demandData, 
                'selectedItem': selectedItem,
                'topKModels': topKModels
            }
    
    def getRiskIdentificationViewData(self, selectedItem, productDataBefore2017):
        # generate the time series
        timeSeriesNumber = len(productDataBefore2017) + 1
        minTimeSeriesLength = 30
        maxTimeSeriesLength = 43

        dataArray = []
        for i in range(0, timeSeriesNumber):
            currentTimeSeries = []
            currentLength = random.randint(minTimeSeriesLength, maxTimeSeriesLength)
            for j in range(0, currentLength):
                currentDemand = random.randint(0, 10000) / 10000
                currentTimeSeries.append(currentDemand)
            print('length: ', len(currentTimeSeries))
            itemName = ''
            if i == 0:
                itemName = selectedItem['item']
            else:
                itemName = productDataBefore2017[i - 1]['item']
            dataArray.append({
                'historical_demand': currentTimeSeries,
                'item': itemName,
                'end_period': random.randint(201805, 201806)
            })

        # with open('RiskIdentificationView_data_20190910_002959.json', 'w') as outFile:
        #     json.dump({'data': dataArray}, outFile)

        # data processing
        for i in range(0, len(dataArray)):
            currentDataObject = dataArray[i]
            currentItem = currentDataObject['item']
            currentEndPeriod = currentDataObject['end_period']
            # historical demand
            currentHistoricalDemand = currentDataObject['historical_demand']

            print('currentItem: ', currentItem)
            print('currentEndPeriod: ', currentEndPeriod)
            print('currentHistoricalDemand: ', currentHistoricalDemand)
            print('currentHistoricalDemand length: ', len(currentHistoricalDemand))

            decomposeResult = seasonal_decompose(currentHistoricalDemand, model='additive', freq=12)
        #     decomposeResult.plot()
        #     plt.show()

            trend = decomposeResult.trend
            # seasonal
            seasonal = decomposeResult.seasonal.tolist()

            trend[np.isnan(trend)] = 100
            # trend
            trend = [None if x > 99 else x for x in trend]
            print('trend: ', trend)
            print('trend length: ', len(trend))
            print('seasonal: ', seasonal)
            print('seasonal length: ', len(seasonal))

            acfResult = acf(np.array(currentHistoricalDemand), nlags=len(currentHistoricalDemand) - 1, alpha=0.05)
        #     print('acfResult: ', acfResult)

            # acf data
            acfData = acfResult[0].tolist()
            print('acfData: ', acfData)
            print('acfData length: ', len(acfData))
            # acf confidence intervals
            acfConfidenceIntervals = acfResult[1].tolist()
            print('acfConfidenceIntervals: ', acfConfidenceIntervals)
            print('acfConfidenceIntervals length: ', len(acfConfidenceIntervals))

            # adf test p-value
            adfResult = adfuller(currentHistoricalDemand)
            print('adfResult (p-value): ', adfResult[1])

            # enlarge the data:
            # 1. currentHistoricalDemand
            # 2. trend
            # 3. seasonal
            # 4. acf data
            # 5. acf confidence intervals
            # 6. adf test p-value
            finalTimeSeriesLength = 43
            needLength = finalTimeSeriesLength - len(currentHistoricalDemand)
            print('needLength: ', needLength)

            # 1. historical demand
            currentDataObject['new_historical_demand'] = []
            for newIndex in range(0, needLength):
                currentDataObject['new_historical_demand'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'historical_demand': None
                })
            for newIndex in range(needLength, finalTimeSeriesLength):
                historicalDemandIndex = newIndex - needLength
                currentDataObject['new_historical_demand'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'historical_demand': currentHistoricalDemand[historicalDemandIndex]
                })
            # print('currentDataObject[\'new_historical_demand\']: ', currentDataObject['new_historical_demand'])

            # 2. trend
            currentDataObject['trend'] = []
            for newIndex in range(0, needLength):
                currentDataObject['trend'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'trend': None
                })
            for newIndex in range(needLength, finalTimeSeriesLength):
                trendIndex = newIndex - needLength
                currentDataObject['trend'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'trend': trend[trendIndex]
                })
            # print('currentDataObject[\'trend\']: ', currentDataObject['trend'])

            # 3. seasonal
            currentDataObject['seasonal'] = []
            for newIndex in range(0, needLength):
                currentDataObject['seasonal'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'seasonal': None
                })
            for newIndex in range(needLength, finalTimeSeriesLength):
                seasonalIndex = newIndex - needLength
                currentDataObject['seasonal'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'seasonal': seasonal[seasonalIndex]
                })
            # print('currentDataObject[\'seasonal\']: ', currentDataObject['seasonal'])

            # 4. acf data
            # 5. acf confidence intervals
            currentDataObject['acf_data'] = []
            currentDataObject['acf_confidence_intervals'] = []
            for newIndex in range(0, needLength):
                currentDataObject['acf_data'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'acf_data': None
                })
                currentDataObject['acf_confidence_intervals'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'acf_confidence_intervals': None
                })
            for newIndex in range(needLength, finalTimeSeriesLength):
                acfIndex = newIndex - needLength
                currentDataObject['acf_data'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'acf_data': acfData[acfIndex]
                })
                currentDataObject['acf_confidence_intervals'].append({
                    'index': newIndex,
                    'item': currentItem,
                    'end_period': currentEndPeriod,
                    'acf_confidence_intervals': acfConfidenceIntervals[acfIndex]
                })
            # print('currentDataObject[\'acf_data\']: ', currentDataObject['acf_data'])
            # print('currentDataObject[\'acf_confidence_intervals\']: ', currentDataObject['acf_confidence_intervals'])

            # 6. adf test p-value
            currentDataObject['adf_test_p_value'] = adfResult[1]
            print('currentDataObject[\'adf_test_p_value\']: ', currentDataObject['adf_test_p_value'])

        # generate the top k model data
        k = 5
        topKModelData = []
        models = []
        for modelIndex in range(0, k):
            currentModel = {}
            modelName = 'model ' + str(modelIndex + 1)
            models.append(modelName)
            currentModel['model_name'] = modelName
            currentModel['accuracy'] = []
            currentModel['variance'] = []
            for itemIndex in range(0, timeSeriesNumber - 1):
                currentAccuracy = {}
                currentAccuracy['model_name'] = modelName
                currentAccuracy['index'] = itemIndex
                currentVariance = {}
                currentVariance['model_name'] = modelName
                currentVariance['index'] = itemIndex

                isAnormal = random.randint(0, 30) > 25
                if not isAnormal:
                    currentAccuracy['accuracy'] = random.randint(50, 100) / 100
                    currentVariance['variance'] = random.randint(0, 300) / 100
                else:
                    currentAccuracy['accuracy'] = -1
                    currentVariance['variance'] = -1

                currentModel['accuracy'].append(currentAccuracy)
                currentModel['variance'].append(currentVariance)

            topKModelData.append(currentModel)

        return {
            'data': dataArray,
            'topKModelData': topKModelData,
            'selectedItem': selectedItem,
            'productDataBefore2017': productDataBefore2017,
            'who': 'I\'m the back-end of function getRiskIdentificationViewData()'
        }


if __name__ == '__main__':
    print('start')
    dataService = DataService()
    result = dataService.test()
    print(result)

    result = dataService.initialization('BabyFace1_S01E01')
    print(result)
    # print('MongoClient: ', MongoClient)
