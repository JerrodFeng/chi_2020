import Vue from 'vue'
import VueResource from 'vue-resource'
Vue.use(VueResource)

// Assume the port of the data Server is 5000, for test only
const dataServerUrl = 'http://127.0.0.1:14004'

const $http = Vue.http

function test (callback) {
    const url = `${dataServerUrl}/test`
    $http.get(url).then(response => {
        callback(response.data)
    }, errResponse => {
        console.log(errResponse)
    })
}

function initialization (videoId, callback) {
    const url = `${dataServerUrl}/initialization/${videoId}`
    $http.get(url).then(response => {
        callback(response.data)
    }, errResponse => {
        console.log(errResponse)
    })
}

function lineChart (videoId, callback) {
    const url = `${dataServerUrl}/lineChart/${videoId}`
    $http.get(url).then(response => {
        callback(response.data)
    }, errResponse => {
        console.log(errResponse)
    })
}

function printInfo (callback) {
    const url = `${dataServerUrl}/printInfo`
    $http.get(url).then(response => {
        callback(response.data)
    }, errResponse => {
        console.log(errResponse)
    })
}
function drawMDSLasso (callback) {
    const url = `${dataServerUrl}/drawMDSLasso`
    $http.get(url).then(response => {
        callback(response.data)
    }, errResponse => {
        console.log(errResponse)
    })
}
function fetchArcData (callback) {
    const url = `${dataServerUrl}/fetchArcData`
    $http.get(url).then(response => {
        callback(response.data)
    }, errResponse => {
        console.log(errResponse)
    })
}
function fetchLassoedDataPost(lassoedData, callback) {
    const url = `${dataServerUrl}/fetchLassoedDataPost`
    // console.log('Overview: run function fetchOverviewDataPost()')
    $http.post(url, {
        lassoedData: lassoedData
    }).then(response => {
        callback(response.data)
    }, errResponse => {
        console.log(errResponse)
    })
}
function fetchLassoedDataFromSimilarityViewPost (lassoedDataFromSimilarityView, callback) {
    const url = `${dataServerUrl}/fetchLassoedDataFromSimilarityViewPost`
    $http.post(url, {
        lassoedDataFromSimilarityView: lassoedDataFromSimilarityView
    }).then(response => {
        callback(response.data)
    }, errResponse => {
        console.log(errResponse)
    })
}

export default {
    test,
    initialization,
    lineChart,
    printInfo,
    drawMDSLasso,
    fetchArcData,
    fetchLassoedDataPost,
    fetchLassoedDataFromSimilarityViewPost
}
