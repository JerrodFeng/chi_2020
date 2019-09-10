# -*- coding: UTF-8 -*-
from app import app
from app import dataService
import json
import os
from flask import send_file, request, jsonify, send_from_directory


_current_dir = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def _index():
    return json.dumps("video analysis back end")


@app.route('/test')
def _test():
    result = dataService.test()
    return json.dumps(result)


@app.route('/lineChart/<video_name>')
def _lineChart(video_name):
    result = dataService.lineChart()
    return json.dumps(result)


# http://localhost:14005/initialization/BabyFace1_S01E01
@app.route('/initialization/<video_name>')
def _initialization(video_name):
    result = dataService.initialization(video_name)
    return json.dumps(result)


# show video url
@app.route('/video/<video_id>')
def _getVideo(video_id):
    video_folder = os.path.join(_current_dir, '../data/videos')
    return send_from_directory(video_folder, '{}.MOV'.format(video_id))


# show image url
@app.route('/image/<video_id>/<person_id>')
def _getImage(video_id, person_id):
    image_path = os.path.join(_current_dir, '../data/images/{}/{}.jpg'.format(video_id, person_id))
    return send_file(image_path, mimetype='image/jpg')

# new method---------------------------
@app.route('/printInfo')
def _printInfo():
    result = dataService.printInfo()
    return json.dumps(result)

@app.route('/drawMDSLasso')
def _drawMDSLasso():
    result = dataService.drawMDSLasso()
    return json.dumps(result)

@app.route('/fetchArcData')
def _fetchArcData():
    result = dataService.fetchArcData()
    return json.dumps(result)

@app.route('/fetchLassoedDataPost', methods = ['POST'])
def _fetchLassoedDataPost():
    # print('backend: run function fetchOverviewData2()')
    post_data = json.loads(request.data.decode())
    # print('backend: post_data:', post_data)
    lassoedData = post_data['lassoedData']
    # request_data = request.get_json()
    # print('backend: request_data:', request_data)
    result = dataService.fetchLassoedDataPost(lassoedData)
    return json.dumps(result)

@app.route('/fetchLassoedDataFromSimilarityViewPost', methods = ['POST'])
def _fetchLassoedDataFromSimilarityViewPost():
    post_data = json.loads(request.data.decode())
    arcData = post_data['lassoedDataFromSimilarityView']
    result = dataService.fetchLassoedDataFromSimilarityViewPost(arcData)
    return json.dumps(result)

# post method
@app.route('/getDetailViewData', methods = ['POST'])
def _getDetailViewData():
    post_data = json.loads(request.data.decode())

    selectedItem = post_data['selectedItem']
    topKModels = post_data['topKModels']

    result = dataService.getDetailViewData(selectedItem, topKModels)
    return json.dumps(result)

@app.route('/getRiskIdentificationViewData', methods = ['POST'])
def _getRiskIdentificationViewData():
    post_data = json.loads(request.data.decode())

    selectedItem = post_data['selectedItem']
    productDataBefore2017 = post_data['productDataBefore2017']

    result = dataService.getRiskIdentificationViewData(selectedItem, productDataBefore2017)
    return json.dumps(result)

@app.route('/getItemCategoryDictionary')
def _getItemCategoryDictionary():
    result = dataService.getItemCategoryDictionary()
    return json.dumps(result)


if __name__ == '__main__':
    pass
