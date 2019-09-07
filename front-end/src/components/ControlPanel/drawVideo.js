/* global d3 $ */
import videojs from 'video.js'
import pipeService from '../../service/pipeService'

let DrawVideo = function (id) {
    this.svgHeight = $(id).height()
    this.svgWidth = $(id).width()

    this.personProbThreshold = 0.9

    // console.log('drawVideo, height: ', $(id).height())
    // console.log('drawVideo, width: ', $(id).width())
    this.setupVideo('my-player')

    // pipeService.onConfirmEditInVideo((data) => {
    //     let selectedPersonOnList = data['selectedPersonOnList']
    //     let selectedEmotionOnList = data['selectedEmotionOnList']
    //     let editFaceIdx = -1
    //     for (let i = 0; i < this.videoData['frameInfo'][this.arrayIdx]['faceList'].length; i++) {
    //         if (this.videoData['frameInfo'][this.arrayIdx]['faceList'][i]['faceIdx'] === this.curEditingFaceIdx) {
    //             editFaceIdx = i
    //             break
    //         }
    //     }
    //     if (editFaceIdx !== -1 && selectedPersonOnList) {
    //         this.videoData['frameInfo'][this.arrayIdx]['faceList'][editFaceIdx]['personName'] = selectedPersonOnList
    //     }

    //     if (editFaceIdx !== -1 && selectedEmotionOnList) {
    //         this.videoData['frameInfo'][this.arrayIdx]['faceList'][editFaceIdx]['emotion'] = selectedEmotionOnList
    //         console.log('drawVideo, emotion: ', this.videoData['frameInfo'][this.arrayIdx]['faceList'][editFaceIdx]['emotion'])
    //     }

    //     this.refOfEditingRect = null
    //     // clear
    //     this.curEditingFaceIdx = null
    //     this.personSelectionListFlag = false
    //     pipeService.emitEditPersonInVideo({
    //         'flag': this.personSelectionListFlag,
    //         'editPersonProb': null,
    //         'editEmotionProb': null
    //     })

    //     this.updateDrawingLabelRects(this.arrayIdx)
    // })

    // pipeService.onCancelEditInVideo(() => {
    //     d3.select(this.refOfEditingRect)
    //         .select('rect')
    //         .style('stroke', this.rectBdNormalClr)

    //     this.refOfEditingRect = null
    //     // clear
    //     this.curEditingFaceIdx = null
    //     this.personSelectionListFlag = false
    //     pipeService.emitEditPersonInVideo({
    //         'flag': this.personSelectionListFlag,
    //         'editPersonProb': null,
    //         'editEmotionProb': null
    //     })
    // })

    // pipeService.onDeleteFaceInVideo((deleteFaceIdx) => {
    //     let editFaceIdx = -1
    //     for (let i = 0; i < this.videoData['frameInfo'][this.arrayIdx]['faceList'].length; i++) {
    //         if (this.videoData['frameInfo'][this.arrayIdx]['faceList'][i]['faceIdx'] === deleteFaceIdx) {
    //             editFaceIdx = i
    //             break
    //         }
    //     }
    //     if (editFaceIdx !== -1) {
    //         this.videoData['frameInfo'][this.arrayIdx]['faceList'][editFaceIdx]['personProb'] = 0
    //         console.log('personProb: ', this.videoData['frameInfo'][this.arrayIdx]['faceList'][editFaceIdx])
    //     }

    //     this.refOfEditingRect = null
    //     // clear
    //     this.curEditingFaceIdx = null
    //     this.personSelectionListFlag = false
    //     this.updateDrawingLabelRects(this.arrayIdx)
    // })

    // pipeService.onPersonProbChange((personProbThreshold) => {
    //     this.personProbThreshold = personProbThreshold
    //     this.updateDrawingLabelRects(this.arrayIdx)
    // })
}

DrawVideo.prototype.setupVideo = function (id) {
    const _this = this
    this.myPlayer = videojs(id, {
        controls: true,
        autoplay: false,
        preload: 'auto',
        language: 'en',
        playbackRates: [0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0],
        inactivityTimeout: 0, // Note: showing the control bars once the video is loaded.
        height: this.svgHeight,
        width: this.svgWidth
    })
    // console.log('videoHeight, videoWdith: ', this.videoHeight, this.videoWidth)
    // this.myPlayer.src(url)
    this.myPlayer.ready(function () {
        // console.log('myPlayer is ready: ', _this.myPlayer)
        _this.myPlayer.pause()
        _this.myPlayer.currentTime(0)

        _this.myPlayer.on('ended', function () {
            console.log('the video is ended.')
        })

        _this.myPlayer.on('pause', function () {
            // clear the timer
            clearInterval(_this.refreshIntervalId)

            console.log('the video is pause')
            console.log('curTime', _this.myPlayer.currentTime())
            let curTime = _this.myPlayer.currentTime()
            _this.curTimeToLabeledFrame(curTime)
            _this.updateDrawingLabelRects(_this.arrayIdx)
        })

        _this.myPlayer.on('play', function () {
            console.log('the video is playing')
            _this.removeDrawingLabelRects()

            // set up timer for updating the frameLine
            _this.refreshIntervalId = setInterval(() => {
                let curTime = _this.myPlayer.currentTime()
                _this.curTimeToLabeledFrame(curTime)
                pipeService.emitFrameSelectedFromVideo(_this.arrayIdx)
            }, 500)
        })

        _this.myPlayer.on('seeking', function () {
            let curTime = parseFloat(_this.myPlayer.currentTime().toFixed(2))
            if (curTime !== _this.seekTime) {
                _this.curTimeToLabeledFrame(curTime)
                _this.myPlayer.currentTime(_this.seekTime)  // add for solve the problem?
            }

            if (_this.myPlayer.paused()) {
                _this.updateDrawingLabelRects(_this.arrayIdx)
            } else {
                _this.removeDrawingLabelRects()
            }
        })
        // _this.myPlayer.on('timeupdate', function () {
        //     console.log('the video is timeupdate')
        //     console.log('curTime', _this.myPlayer.currentTime())
        //     _this.updateDrawingLabelRects(_this.myPlayer.currentTime())
        // })
    })

    // pipeService.onFrameSelectedFromTimeBar((arrayIdx) => {
    //     _this.arrayIdx = arrayIdx
    //     _this.seekFrame = _this.frameIdxList[arrayIdx]
    //     _this.seekTime = _this.seekTimeList[arrayIdx]
    //     _this.myPlayer.currentTime(_this.seekTime)
    // })
}

DrawVideo.prototype.layout = function (id, data, url) {
    this.cleanup(id)
    this.videoHeight = data['videoHeight']
    this.videoWidth = data['videoWidth']
    this.videoData = data
    this.fps = data['fps']

    this.myPlayer.src(url)
    // layout
    let containerRatio = this.svgWidth / this.svgHeight
    let videoRatio = this.videoWidth / this.videoHeight

    if (videoRatio > containerRatio) {
        this.videoScreenWidth = this.svgWidth
        this.videoScreenHeight = this.svgWidth / videoRatio
    } else {
        this.videoScreenHeight = this.svgHeight
        this.videoScreenWidth = this.svgHeight * videoRatio
    }

    // setup label environment
    let xOffset = (this.svgWidth - this.videoScreenWidth) / 2
    let yOffset = (this.svgHeight - this.videoScreenHeight) / 2

    this.margin = { top: yOffset, right: xOffset, bottom: yOffset, left: xOffset }

    this.svg = d3.select(id).append('svg')
        .attr('class', 'videoSvg')
        .attr('height', this.svgHeight)
        .attr('width', this.svgWidth)

    this.graphContainer = this.svg.append('g')
        .attr('class', 'g_main')
        .attr('transform', 'translate(' + this.margin.left + ', ' + this.margin.top + ')')

    // global variable in this file
    this.labeledFrameIndex = -1   // initialize it as -1 to indicate no updating

    this.rectBdHighlightClr = '#ff0000'
    this.rectBdNormalClr = '#00ff00'
    this.rectBdWarningClr = 'yellow' // when not sure about the computed baby id
    this.refreshIntervalId = -1

    this.arrayIdx = 0
    this.seekTime = 0
    this.seekFrame = 0
    this.frameIdxList = d3.range(0, this.videoData['totalFrame'] + 1, this.videoData['sampleInterval'])
    // console.log('this.frameIdxList: ', this.frameIdxList)
    this.seekTimeList = this.frameIdxList.map((d) => {
        return parseFloat((d / this.fps).toFixed(2))
    })

    // edit varible
    this.curEditingFaceIdx = null
    this.refOfEditingRect = null
}

DrawVideo.prototype.cleanup = function (id) {
    d3.select(id).selectAll('*').remove()
}

DrawVideo.prototype.removeDrawingLabelRects = function () {
    this.graphContainer.selectAll('*').remove()
}

DrawVideo.prototype.updateDrawingLabelRects = function (arrayIdx) {
    this.removeDrawingLabelRects()
    const _this = this
    console.log('drawVideo arrayIdx: ', arrayIdx)
    if (this.videoData === undefined || this.videoData['frameInfo'] === undefined || this.videoData['frameInfo'].length === 0) {
        console.log('====No face for the whole video===== ')
        return
    }
    pipeService.emitFrameSelectedFromVideo(arrayIdx)

    const frameInfo = this.videoData['frameInfo'][arrayIdx]
    const labeledFrameIndex = frameInfo['frameIdx']  // should equal to frameIndex
    const labeledPeopleList = frameInfo['faceList'].filter((d) => d['personProb'] > this.personProbThreshold)
    this.labeledFrameIndex = labeledFrameIndex  // update the current labeled frame number
    if (labeledPeopleList.length === 0) {
        console.log('======No peope face for the current frame=====', labeledFrameIndex)
        return
    }
    // console.log('frmInfo: ', frameInfo)

    // prepare to draw the rectangles
    this.graphContainer.selectAll('g')
        .attr('class', 'peopleRectLabel')
        .data(labeledPeopleList)
        .enter()
        .append('g')
        .attr('class', person => person['personName'])
        .attr('transform', (person) => {
            const x = person['faceRectangle'][0] * _this.videoScreenWidth
            const y = person['faceRectangle'][1] * _this.videoScreenHeight
            return `translate(${x}, ${y})`
        })
        .each(function drawRect(person) {
            const w = person['faceRectangle'][2] * _this.videoScreenWidth
            const h = person['faceRectangle'][3] * _this.videoScreenHeight
            const gPointer = this
            d3.select(this)
                .append('rect')
                .attr('width', w)
                .attr('height', h)
                .style('fill-opacity', 0.0)
                .style('fill', 'pink')
                .style('stroke', _this.rectBdNormalClr)
                .style('stroke-width', 2) // original one is 4
                .style('pointer-events', 'all')
                .on('mouseover', function rectMouseOver() {
                    d3.select(this).style('stroke', _this.rectBdHighlightClr)
                    d3.select(gPointer).selectAll('image').style('opacity', 1.0) // for editing images
                })
                .on('mouseout', function rectMouseOut() {
                    if (_this.curEditingFaceIdx !== person['faceIdx']) { // if not edited -> normal
                        d3.select(this).style('stroke', _this.rectBdNormalClr)
                    }
                    d3.select(gPointer).selectAll('image').style('opacity', 0.0)
                })
                .on('click', function clickRect() {
                    if (!d3.select(this).classed('selected')) {
                        _this.graphContainer.selectAll('rect').classed('selected', false).style('fill-opacity', 0)
                        d3.select(this).classed('selected', true).style('fill-opacity', 1)
                        pipeService.emitSelectPersonInVideo(person['personName'])
                    } else {
                        d3.select(this).classed('selected', false).style('fill-opacity', 0)
                        pipeService.emitReleasePersonInVideo(person['personName'])
                    }
                    pipeService.emitCancelEditInVideo()
                })
            // show the names
            d3.select(this)
                .append('text')
                .attr('x', w / 3)
                .attr('y', h - 8)
                // .text(person['personName'].split('_').slice(-1) + ',' + person['emotion'])
                .text(person['personName'] + ',' + person['emotion'])
                .attr('font-family', 'sans-serif')
                .attr('font-size', '8px')
                .attr('fill', 'white')

            // show the edit and delete icons
            const iconSize = 20
            d3.select(this)
                .append('image')
                .attr('xlink:href', './static/labeling-icons/edit.png')
                .attr('x', -iconSize / 2)
                .attr('y', -iconSize / 2)
                .attr('width', iconSize)
                .attr('height', iconSize)
                .style('opacity', 0.0)
                .style('pointer-events', 'all')
                .on('mouseover', () => {
                    d3.select(gPointer).selectAll('rect').style('stroke', _this.rectBdHighlightClr)
                    d3.select(gPointer).selectAll('image').style('opacity', 1.0)
                })
                .on('mouseout', () => {
                    if (_this.curEditingFaceIdx !== person['faceIdx']) { // if not edited -> normal
                        d3.select(gPointer).selectAll('rect').style('stroke', _this.rectBdNormalClr)
                    }
                    d3.select(gPointer).selectAll('image').style('opacity', 0.0)
                })
                .on('click', () => {
                    _this.refOfEditingRect = gPointer
                    _this.curEditingFaceIdx = person['faceIdx']
                    _this.personSelectionListFlag = true
                    const xx = person['faceRectangle'][0] * _this.videoScreenWidth
                    const yy = person['faceRectangle'][1] * _this.videoScreenHeight
                    const ww = person['faceRectangle'][2] * _this.videoScreenWidth
                    pipeService.emitEditPersonInVideo({
                        'flag': _this.personSelectionListFlag,
                        'xx': xx,
                        'yy': yy,
                        'ww': ww,
                        'editPersonProb': person['personProb'].toFixed(4),
                        'editEmotionProb': person['emotionProb'].toFixed(4)
                    })
                })
            d3.select(this)
                .append('image')
                .attr('xlink:href', './static/labeling-icons/delete.png')
                .attr('x', w - (iconSize / 2))
                .attr('y', -iconSize / 2)
                .attr('width', iconSize)
                .attr('height', iconSize)
                .style('opacity', 0.0)
                .style('pointer-events', 'all')
                .on('mouseover', () => {
                    d3.select(gPointer).selectAll('rect').style('stroke', _this.rectBdHighlightClr)
                    d3.select(gPointer).selectAll('image').style('opacity', 1.0)
                })
                .on('mouseout', () => {
                    if (_this.curEditingFaceIdx !== person['faceIdx']) { // if not edited -> normal
                        d3.select(gPointer).selectAll('rect').style('stroke', _this.rectBdNormalClr)
                    }
                    d3.select(gPointer).selectAll('image').style('opacity', 0.0)
                })
                .on('click', () => {
                    d3.select(gPointer).remove()
                    pipeService.emitDeleteFaceInVideo(person['faceIdx'])
                })
        })
}

DrawVideo.prototype.curTimeToLabeledFrame = function (curTime) {
    let bisect = d3.bisector(function(d) { return d }).left
    let arrayIdx = bisect(this.seekTimeList, curTime)
    this.seekTime = this.seekTimeList[arrayIdx]
    this.seekFrame = this.frameIdxList[arrayIdx]
    this.arrayIdx = arrayIdx
    return { 'seekTime': this.seekTime, 'seekFrame': this.seekFrame }
}

DrawVideo.prototype.timeToFrame = function (curTime) {
    const fps = this.videoData['fps']  // 30
    const processedFps = this.videoData['processedFps']  // 3
    const samplingRate = parseInt(fps / processedFps, 10)  // 10

    const frameVideoIndex = parseInt(curTime * fps, 10)  // such as 140, the frame index in video
    const frameInfoIndex = parseInt(frameVideoIndex / samplingRate, 10)  // such as 14, index of frame stored in frameInfo

    return { frameVideoIndex, frameInfoIndex }
}
export default DrawVideo
