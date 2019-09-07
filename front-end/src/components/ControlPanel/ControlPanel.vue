<template src='./ControlPanel.html'></template>

<script>
// /* global d3 */
// import pipeService from '../../service/pipeService'
// import dataService from '../../service/dataService'
// import DrawVideo from './drawVideo.js'
export default {
    name: 'ControlPanel',
    components: {
    },
    // props: ['message'],
    data: function() {
        return {
            msg: 'Jerrod shuai'
        }
    },
    watch: {

    },
    methods: {
        sendMsgToParent: function() {
            // this.$emit('listenToChildEvent', 'this message is from child')
            this.$emit('listenToChildEvent', this.msg)
        }
    },
    mounted: function() {
    }
}
</script>

<style>
    #ControlPanel {
        
        /* height: 100%;
        width: 350px; */
        margin: 0 auto;
        width: 400px;
        height: 929px;
        
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
