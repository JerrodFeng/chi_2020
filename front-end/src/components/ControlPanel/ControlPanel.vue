<template>
    <div id="ControlPanel" class='border'>
        <!-- overview head -->
        <div id='overview_head'>Overview</div>
        <!-- select the month forecasted -->
        <div id='overview_select_start_month'>
            Forecast: 
            <input type='month' name='start_month' id='overview_start_month' value='2018-07'>
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
        <svg id='overview_model_svg' style="width: 316px; height: 400px;"></svg>
        
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
        modelInformation: Array
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
                d.totalWeight = weightArray[0] * d.accuracy + weightArray[1] * d.variance + weightArray[2] * d.topRank
            })

            newModelInformation.sort(function(a, b) {
                return b.totalWeight - a.totalWeight
            })

            console.log('Overview::ranked modelInformation: ', newModelInformation)

            let topKModels = newModelInformation.filter(function(d, i) {
                return i < topK
            })
            this.topKModels = topKModels.map(function(d) {
                return d.modelName
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
        height: 929px;
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
        width: 140px;
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
</style>
