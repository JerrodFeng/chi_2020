    #  计算欧拉距离
    def distance(length, vector1,vector2):
        d=0
        for index, a, b in zip(range(length), vector1, vector2):
            d+=((a-b)**2)  
        return d**0.5
    
    def getRiskIdentificationViewData(self, selectedItem, productDataBefore2017):
        # client = MongoClient('localhost', 27017)
        # mydb = client['Dong_chi_2020']
        # mydb = client['Dong_chi_2020']
        # selectedItem = {'endPeriod': 201806, 'item': 'item1213'}
        # productDataBefore2017 = [{"endPeriod": 201806, "item": "item1220"},{"endPeriod": 201806, "item": "item1213"}, {"endPeriod": 201805, "item": "item1213"},{"endPeriod": 201807, "item": "item1214"}]
        # topKModels = ["GMNR", "ada", "arima", "arimax", "cat"]
        curEndperiod = selectedItem['endPeriod']
        curItem = selectedItem['item']
        hisDemand = []
        collection = self.db['originalDataDict']
        selectedResults = collection.find({'$and':[{'item': curItem}, {'period_id':{'$lt': (curEndperiod +1)}}]}).sort('period_id')
        for selectedResult in selectedResults:
            hisDemand.append(selectedResult['qty'])
        # print(hisDemand)
        selectedItemData = {}
        selectedItemData['item'] = curItem
        selectedItemData['end_period'] = curEndperiod
        selectedItemData['historical_demand'] = hisDemand

        # print(selectedItemData)
        tmpProductDataBefore = []
        for i in range(len(productDataBefore2017)):
            curTmpItem = productDataBefore2017[i]['item']
            curTmpEndPeriod = productDataBefore2017[i]['endPeriod']
            selectedResults = collection.find({'$and':[{'item': curTmpItem}, {'period_id':{'$lt': (curTmpEndPeriod +1)}}]}).sort('period_id')
            tmpHisDemand = []
            for selectedResult in selectedResults:
                tmpHisDemand.append(selectedResult['qty'])
            tmpItemData = {}
            tmpItemData['item'] = curTmpItem
            tmpItemData['end_period'] = curTmpEndPeriod
            tmpItemData['historical_demand'] = tmpHisDemand
            tmpProductDataBefore.append(tmpItemData)

        # print(tmpProductDataBefore)


        for i in range(len(tmpProductDataBefore)):
            tmpSeries = tmpProductDataBefore[i]['historical_demand']
            
            tmpLength = min(len(tmpSeries), len(selectedItemData['historical_demand']))
            vector1 = tmpSeries[-tmpLength :]
            vector2 = selectedItemData['historical_demand'][-tmpLength :]
            tmpSimilarity = distance(tmpLength, vector1,vector2)
            tmpProductDataBefore[i]['similarity'] = tmpSimilarity
        newTmpProductDataBefore = sorted(tmpProductDataBefore,key=lambda keys:keys['similarity'])
        # print('---', newTmpProductDataBefore)

        returnedData = []
        returnedData.append(selectedItemData)
        for i in range(len(newTmpProductDataBefore)):
            returnedData.append(newTmpProductDataBefore[i])

            
        # print(returnedData)
        return {
            'data' : returnedData
        }


