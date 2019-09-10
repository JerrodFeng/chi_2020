<template>
    <div id="ControlPanel" class='border'>
        <!-- overview head -->
        <div id='overview_head'>Overview</div>
        <!-- select the month forecasted -->
        <div id='overview_select_start_month'>
            Forecast: 
            <input type='month' name='start_month' id='overview_start_month' value='2018-08'>
        </div>
        <!-- sliders for parameters -->
        <div id='overview_parameter_head'>
            Parameters
        </div>
        <div id='accuracy_slider_div'>
            <input id='accuracy_slider' class='range-slider' type='hidden' value='0'/><br>
        </div>
        <div id='variance_slider_div'>
            <input id='variance_slider' class='range-slider' type='hidden' value='0'/><br>
        </div>
        <div id='applicability_slider_div'>
            <input id='applicability_slider' class='range-slider' type='hidden' value='0'/><br>
        </div>
        <div id='top_k_slider_div'>
            <input id='top_k_slider' class='range-slider' type='hidden' value='0'/><br>
        </div>
        <svg id='overview_slider_svg' style="width: 316px; height: 190px;"></svg>
        <!-- the ranked list of models -->
        <div id='overview_model_head'>
            Models
        </div>
        <div id='overview_model_svg_div'>
            <svg id='overview_model_svg'></svg>
        </div>
        
    </div>
</template>

<script>
/* global d3, $ */
// import pipeService from '../../service/pipeService'
// import dataService from '../../service/dataService'
// import DrawVideo from './drawVideo.js'
import 'jRange/jquery.range.css'
import 'jRange/jquery.range.js'

export default {
    name: 'ControlPanel',
    components: {
    },
    props: {
        modelInformation: Array,
        maxModelVariance: Number
    },
    data: function() {
        return {
            msg: 'Jerrod shuai',
            accuracyWeight: 0.5,
            varianceWeight: 0.5,
            applicabilityWeight: 0.5,
            topK: 5,
            topKModels: []
        }
    },
    watch: {
        modelInformation: function(newValue, oldValue) {
            console.log('Overview::modelInformation change to: ', newValue)
            if (newValue.length !== 0) {
                this.drawModelList()
            }
        },

        accuracyWeight: function(newValue, oldValue) {
            this.weightChanged()
        },

        varianceWeight: function(newValue, oldValue) {
            this.weightChanged()
        },

        applicabilityWeight: function(newValue, oldValue) {
            this.weightChanged()
        },

        topK: function(newValue, oldValue) {
            console.log('Overview::topK change to: ', newValue)
        },

        topKModels: function(newValue, oldValue) {
            console.log('Overview::topKModels change to: ', newValue)
            this.$emit('changeTopKModels', newValue)
        }
    },
    methods: {
        sendMsgToParent: function() {
            // this.$emit('listenToChildEvent', 'this message is from child')
            this.$emit('listenToChildEvent', this.msg)
        },

        drawModelList: function() {
            let newModelInformation = []
            for (let i = 0; i < this.modelInformation.length; i++) {
                let currentModel = this.modelInformation[i] // object
                let newCurrentModel = Object.assign({}, currentModel)
                newModelInformation.push(newCurrentModel)
            }
            let weightArray = [this.accuracyWeight, this.varianceWeight, this.applicabilityWeight]
            let topK = this.topK

            // rank the models
            newModelInformation.forEach(function(d) {
                d.totalWeight = weightArray[0] * d.accuracy + weightArray[1] * (1 - d.variance) + weightArray[2] * d.topRank
            })

            newModelInformation.sort(function(a, b) {
                return b.totalWeight - a.totalWeight
            })

            console.log('Overview::ranked modelInformation: ', newModelInformation)

            let topKModels = newModelInformation.filter(function(d, i) {
                return i < topK
            })
            topKModels = topKModels.map(function(d) {
                return d.modelName
            })

            this.topKModels = topKModels

            // draw the overview
            let modelGap = 40
            let barWidth = 35
            let barHeight = 12
            let firstBarX = 105
            let circleRadius = 11
            let barCircleGap = 30
            let circleX = firstBarX + barWidth + barCircleGap
            let secondBarX = circleX + circleRadius * 2 + barCircleGap

            let totalWidth = 316
            let height = modelGap * newModelInformation.length
            let margin = {top: 15, right: 10, bottom: 10, left: 10}
            // let width = totalWidth - margin.left - margin.right
            let totalHeight = height + margin.top + margin.bottom

            d3.select('#overview_model_svg').html('')
            var svg = d3.select('#overview_model_svg')
                .attr('width', totalWidth)
                .attr('height', totalHeight)
                .append('g')
                .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

            let modelGroup = svg.selectAll('.model_group')
                .data(newModelInformation)
                .enter()
                .append('g')
                .attr('class', 'model_group')
                .attr('transform', function(d, i) {
                    let translateX = 0
                    let translateY = i * modelGap

                    return 'translate(' + translateX + ', ' + translateY + ')'
                })

            // model text
            modelGroup.append('g')
                .attr('class', 'model_name')
                .append('text')
                .attr('y', 0)
                .attr('x', 85)
                .attr('dy', 9)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 14)
                .text(function (d) {
                    // console.log(d)
                    return d.modelName + ': '
                })

            let x = d3.scaleLinear().range([0, barWidth])
                .domain([0, 1])
            let z = d3.scaleOrdinal()
                    .range([
                        '#fbb4ae', // red
                        '#b3cde3', // blue
                        '#ccebc5', // green
                        '#decbe4', // purple
                        '#fed9a6' // orange
                    ])
            z.domain(topKModels)

            // draw accuracy bar
            modelGroup.append('g')
                .attr('class', 'model_accuracy_rectangle')
                .append('rect')
                .attr('x', function(d) {
                    return firstBarX
                })
                .attr('y', function(d) {
                    return 0
                })
                .attr('width', function(d) {
                    return x(d.accuracy)
                })
                .attr('height', function(d) {
                    return barHeight
                })
                .style('fill', function(d) {
                    if (topKModels.includes(d.modelName)) {
                        return z(d.modelName)
                    } else {
                        return '#d9d9d9'
                    }
                })

            // draw variance circle
            let whiteColor = d3.rgb('#FFFFFF')
            let yellowColor = d3.rgb('#f16913') // orange
            let computeYellowColor = d3.interpolate(whiteColor, yellowColor)
            let linearYellowColor = d3.scaleLinear()
                .domain([0, 1])
                .range([0, 1])

            modelGroup.append('g')
                .attr('class', 'model_variance_circle')
                .append('circle')
                .attr('r', function(d, i) {
                    return circleRadius
                })
                .attr('cx', function(d, i) {
                    return circleX + circleRadius
                })
                .attr('cy', function(d, i) {
                    return barHeight / 2
                })
                .style('fill', function(d, i) {
                    return computeYellowColor(linearYellowColor(d.variance))
                })
                .style('stroke', function(d, i) {
                    return '#d9d9d9'
                })
                .style('stroke-width', function(d, i) {
                    return 1
                })

            // draw top K bar
            modelGroup.append('g')
                .attr('class', 'model_top_k_rectangle')
                .append('rect')
                .attr('x', function(d) {
                    return secondBarX
                })
                .attr('y', function(d) {
                    return 0
                })
                .attr('width', function(d) {
                    return x(d.topRank)
                })
                .attr('height', function(d) {
                    return barHeight
                })
                .style('fill', function(d) {
                    if (topKModels.includes(d.modelName)) {
                        return z(d.modelName)
                    } else {
                        return '#d9d9d9'
                    }
                })
        },

        weightChanged: function() {
            let weightArray = [this.accuracyWeight, this.varianceWeight, this.applicabilityWeight]
            console.log('weightArray: ', weightArray)
            if (this.modelInformation.length !== 0) {
                this.drawModelList()
            }
        },

        createSlider: function() {
            let myThis = this

            // accuracy slider
            {
                let currentSlider = '#accuracy_slider'
                $(currentSlider).jRange({
                    from: 0,
                    to: 1,
                    step: 0.01,
                    scale: [0, 0.25, 0.5, 0.75, 1],
                    format: '%s',
                    width: 190,
                    showLabels: true,
                    snap: true,
                    theme: 'theme-model-parameter'
                })
                $(currentSlider).jRange('setValue', 0.5 + '')
                $(currentSlider).change(function() {
                    let currentValue = parseFloat($(currentSlider).val())
                    // console.log(currentSlider + ' value change to: ', currentValue)
                    myThis.accuracyWeight = currentValue
                })
            }

            // variance slider
            {
                let currentSlider = '#variance_slider'
                $(currentSlider).jRange({
                    from: 0,
                    to: 1,
                    step: 0.01,
                    scale: [0, 0.25, 0.5, 0.75, 1],
                    format: '%s',
                    width: 190,
                    showLabels: true,
                    snap: true,
                    theme: 'theme-model-parameter'
                })
                $(currentSlider).jRange('setValue', 0.5 + '')
                $(currentSlider).change(function() {
                    let currentValue = parseFloat($(currentSlider).val())
                    // console.log(currentSlider + ' value change to: ', currentValue)
                    myThis.varianceWeight = currentValue
                })
            }

            // applicability slider
            {
                let currentSlider = '#applicability_slider'
                $(currentSlider).jRange({
                    from: 0,
                    to: 1,
                    step: 0.01,
                    scale: [0, 0.25, 0.5, 0.75, 1],
                    format: '%s',
                    width: 190,
                    showLabels: true,
                    snap: true,
                    theme: 'theme-model-parameter'
                })
                $(currentSlider).jRange('setValue', 0.5 + '')
                $(currentSlider).change(function() {
                    let currentValue = parseFloat($(currentSlider).val())
                    // console.log(currentSlider + ' value change to: ', currentValue)
                    myThis.applicabilityWeight = currentValue
                })
            }

            // top k slider
            {
                let currentSlider = '#top_k_slider'
                $(currentSlider).jRange({
                    from: 1,
                    to: 10,
                    step: 1,
                    scale: [1, 4, 7, 10],
                    format: '%s',
                    width: 190,
                    showLabels: true,
                    snap: true,
                    theme: 'theme-model-parameter'
                })
                $(currentSlider).jRange('setValue', 5 + '')
                $(currentSlider).change(function() {
                    let currentValue = parseInt($(currentSlider).val())
                    // console.log(currentSlider + ' value change to: ', currentValue)
                    myThis.topK = currentValue
                })
            }
        }
    },
    mounted: function() {
        this.$nextTick(() => {
            d3.select('#overview_head')
                .attr('class', 'similarity_view_heading')
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'start')
                .attr('font-size', 16)

            d3.select('#overview_slider_svg')
                .append('text')
                .attr('x', 95)
                .attr('y', 22)
                .attr('dy', 0)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 14)
                .text('Accuracy:')

            d3.select('#overview_slider_svg')
                .append('text')
                .attr('x', 95)
                .attr('y', 22 + 50)
                .attr('dy', 0)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 14)
                .text('Variance:')

            d3.select('#overview_slider_svg')
                .append('text')
                .attr('x', 95)
                .attr('y', 22 + 50 + 50)
                .attr('dy', 0)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 14)
                .text('Applicability:')

            d3.select('#overview_slider_svg')
                .append('text')
                .attr('x', 95)
                .attr('y', 22 + 50 + 50 + 50)
                .attr('dy', 0)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 14)
                .text('Top k:')

            this.createSlider()

            console.log('modelInformation: ', this.modelInformation)
        })
    }
}
</script>

<style>
    #ControlPanel {
        margin: 2px;
        width: 316px;
        /* height: 929px; */
    }

    #ControlPanel #overview_head {
        margin: 1px 6px; 
        padding: 0px 0px 0px 0px;
    }

    #ControlPanel #overview_select_start_month {
        margin: 5px 15px; 
        padding: 0px 0px 0px 0px;
    }

    #ControlPanel #overview_start_month {
        margin-left: 6px;
        margin-top: 4px;
        width: 160px;
        border-radius: 5px;
        outline: none;
        border: 1px solid #ccc;
    }

    #ControlPanel #overview_parameter_head {
        margin: 12px 15px; 
        padding: 0px 0px 0px 0px;
        border-bottom: 1px solid #bdbdbd;
    }

    #ControlPanel #accuracy_slider_div {
        position: absolute;
        top: 130px; 
        left: 105px;
        display: block;
    }

    #ControlPanel #variance_slider_div {
        position: absolute;
        top: 180px; /* 130 + 50 */
        left: 105px;
        display: block;
    }

    #ControlPanel #applicability_slider_div {
        position: absolute;
        top: 230px; /* 130 + 50 + 50 */
        left: 105px;
        display: block;
    }

    #ControlPanel #top_k_slider_div {
        position: absolute;
        top: 280px; /* 130 + 50 + 50 + 50 */
        left: 105px;
        display: block;
    }

    #ControlPanel #overview_model_head {
        margin: 2px 15px; 
        padding: 0px 0px 0px 0px;
        border-bottom: 1px solid #bdbdbd;
    }

    #ControlPanel #overview_model_svg_div {
        width: 316px;
        height: 590px;
        overflow-y: auto;
        overflow-x: hidden;
    }

    #ControlPanel .card {
        margin-bottom: 5px;
        margin-top: 5px;
        height: 842px;
        width: 100%;
        border-radius: 0;
    }

    /* #ControlPanel .card-header {
        width: 100%;
        font-size: 12px;
        padding: 6px 12px;
    } */

    #ControlPanel .card-block {
        padding: 0px;
        position: relative;
        /* height: 100%; */
        /* width: 100%; */
    }

    /* #videoview text {
        font-weight: 300;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serf;
        font-size: 14px;
    }

    #videoview .node rect {
        stroke: #333;
        fill: #fff;
        stroke-width: 1.5px;
    } */

    /* #videoview .edgePath path {
        stroke: #333;
        stroke-width: 1.5px;
    } */

    /* #videoview .node text {
        pointer-events: none;
    } */

    /* #videoview .g_main {
        cursor: pointer;
        pointer-events: all
    } */

    /* #videoview div.tooltip {
        position: absolute;
        text-align: center;
        width: 120px;
        height: 20px;
        padding: 2px;
        font: 12px sans-serif;
        background: lightsteelblue;
        border: 0px;
        border-radius: 8px;
        pointer-events: none;
    }

    #my-player {
        position: absolute;
        height: 100%;
        width: 100%;
    }

    .vjs-tech {
        pointer-events: none;
    } */

    /* #labelsContainer {
        position: absolute;
        top: 0px;
        height: 100%;
        width: 100%;
        pointer-events: none;
    } */

    /* #personFaceSelectionList {
        position: absolute;
        top: 0px;
        left: 0px;
        width: 320px;
        height: 280px;
        background-color: #EEEEEE;
        opacity: 1.0;
        border: 3px solid #fe6271;
        z-index: 10000;
    } */

    /* .singlePersonProfile {
        margin: 4px 4px 4px 4px;
        display: inline-block;
        width: 60px;
    } */

    /* .singleEmotion {
        margin: 4px 4px 4px 4px;
        display: inline-block;
        width: 60px;
    } */

    /* .faceListContainer {
        padding-top: 7px;
        padding-left: 20px;
        padding-right: 6px;
        height: 200px;
        overflow-y: scroll;
        
        border-bottom: 3px solid #fe6271;
        border-radius: 0px;
    } */

    /* .emotionListContainer {
        padding-top: 7px;
        padding-left: 20px;
        padding-right: 20px;
        height: 200px;
        overflow-y: scroll;
        
        border-top: 5px;
        border-bottom: 3px solid #fe6271;
        border-radius: 0px;
    } */

    /* .faceSelectionButtons {
        padding: 4px 10px 4px 10px;
    }

    .faceSelectionButtons button {
        float: right;
        margin: 4px 4px 2px 4px;
    }

    .faceSelectionButtons .prob {
        float: left;
        margin: 4px 4px 2px 4px;
        font-size: 12px;
    }

    .btn {
        padding: 3px 6px 3px 6px;
    }
    .imageList {
        border: 2px solid rgba(250, 5, 5, 0);
    }

    .selectedPersonOnList {
        border: 2px solid rgba(250, 5, 5, 1);
    }

    .selectedEmotionOnList {
        border: 2px solid rgba(250, 5, 5, 1);
    } */

    /* width */
    ::-webkit-scrollbar {
    width: 4px;
    }

    /* Track */
    ::-webkit-scrollbar-track {
    background: #f1f1f1; 
    }
    
    /* Handle */
    ::-webkit-scrollbar-thumb {
    background: #888; 
    }

    /* Handle on hover */
    ::-webkit-scrollbar-thumb:hover {
    background: #555; 
    }
</style>
