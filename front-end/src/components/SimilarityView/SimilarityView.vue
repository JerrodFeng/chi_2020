/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */
<template src='./SimilarityView.html'></template>

<script>
// eslint-disable-next-line no-unused-vars
/* global d3, $ */
import dataService from '../../service/dataService'
import * as d3Lasso from 'd3-lasso/build/d3-lasso.min.js'
// import DrawMDSLasso from './drawMDSLasso.js'
// import DrawBarChart from './drawBarChart.js'
// /* global d3 */
// import DrawPeople from './drawPeople.js'
// import dataService from '../../service/dataService'
// import bus from '../../main'
export default {
    name: 'SimilarityView',
    components: {
    },
    props: {
        message: String,
        itemToBeDeleted: Object
    },
    data() {
        return {
            message2: [],
            lassoedData: [],
            lassoedDataFromSimilarityView: [],
            allTheDots: null
        }
    },
    watch: {
        message2(newValue, oldValue) {
            // dataService.printInfo((data) => {
            //     console.log('view002::message: ', data)
            //     this.message = data.data
            //     this.drawBarChart.printInfo(data)
            // })
            this.drawMDSLasso(newValue)
        },
        lassoedData(newValue, oldValue) {
            console.log('SimilarityView::lassoedData change to: ', newValue)
            dataService.fetchLassoedDataPost(newValue, (returnedData) => {
                console.log('SimilarityView::fetchProductViewLassoedDataPost: ', returnedData)

                this.lassoedDataFromSimilarityView = {'SimilarityViewData': returnedData}
                this.$emit('changeLassoedDataFromSimilarityView', this.lassoedDataFromSimilarityView)
            })
        },

        itemToBeDeleted: function(newValue, oldValue) {
            console.log('SimilarityView::itemToBeDeleted change to: ', newValue)
            this.lassoedData = this.lassoedData.filter(function (d, i) {
                return !((d.item === newValue.item) && (d.endPeriod === newValue.endPeriod))
            })

            this.allTheDots.attr('r', function(d, i) {
                console.log('allTheDotsData: ', d)
                if ((d.item === newValue.item) && (d.endPeriod === newValue.endPeriod)) {
                    return 1.5
                } else {
                    return d3.select(this).attr('r')
                }
            })
            .style('opacity', function(d, i) {
                if ((d.item === newValue.item) && (d.endPeriod === newValue.endPeriod)) {
                    return 0.4
                } else {
                    return d3.select(this).style('opacity')
                }
            })
        }
    },
    methods: {
        drawMDSLasso: function(data) {
            var myThis = this
            var svg = d3.select('#MDSLasso_svg')
            var width = svg.attr('width')
            let height = svg.attr('height')
            let dataset = data
            // let dataset = data.map((d) => d['data'])
            console.log('SimilarityView dataset successful')
            console.log('SimilarityView dataset::', dataset)

                // .append('svg')

            let margin = { top: 71.33 - 10, bottom: 30, left: 10, right: 10 }

            var xScale = d3.scaleLinear()
                .domain([d3.min(dataset.map((d) => d['data']), (d) => d[0]), d3.max(dataset.map((d) => d['data']), (d) => d[0])])
                // .domain([-7, 7])
                .range([0, width - margin.left - margin.right])
            var yScale = d3.scaleLinear()
                .domain([d3.max(dataset.map((d) => d['data']), (d) => d[1]), d3.min(dataset.map((d) => d['data']), (d) => d[1])])
                // .domain([-7, 7])
                .range([0, height - margin.top - margin.bottom])
            var scatterMDS = svg.append('g')
                .attr('class', 'scatter_MDS_group')
                .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')
                .attr('width', width - margin.left - margin.right)
                .attr('height', height - margin.top - margin.bottom)

            // var circles = svg.selectAll('circle')
            //     .data(data)
            //     .enter()
            //     .append('circle')
            //     .attr('cx', d => d[0] * w)
            //     .attr('cy', d => d[1] * h)
            //     .attr('r', r)
            var dots = scatterMDS.append('g')
                .selectAll('circle')
                .data(dataset)
                .enter()
                .append('circle')
                .attr('cx', function(d, i) {
                    // let coordsData = (d) => d['data']
                    // console.log('coordsData::', coordsData)
                    return xScale(d['data'][0])
                })
                .attr('cy', function(d, i) {
                    // let coordsData = (d) => d['data']
                    return yScale(d['data'][1])
                })
                .attr('r', 1.5)
                .attr('fill', function(d, i) {
                    // console.log('fill::data', d)
                    if (d['endPeriod'] === 201807) {
                        return '#fb8072'
                    } else {
                        return '#bebada'
                    }
                })

            this.allTheDots = dots

            scatterMDS.append('text')
                .attr('class', 'similarity_view_heading')
                .attr('y', -margin.top + 16)
                .attr('x', 0)
                .attr('dx', -2)
                .attr('dy', 4)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'start')
                .attr('font-size', 16)
                .text(function (d) {
                    // console.log(d)
                    return 'Similarity View'
                })

            // var xAxis = d3.axisBottom()
            //     .scale(xScale)
            //     .ticks(7)

            // var yAxis = d3.axisLeft()
            //     .scale(yScale)
            //     .ticks(7)
            // scatterMDS.append('g')
            //     .attr('class', 'axis')
            //     .attr('transform', 'translate(' + 0 + ',' + (height - 2 * margin.top) + ')')
            //     .call(xAxis)

            // scatterMDS.append('g')
            //     .attr('class', 'axis')
            //     .attr('transform', 'translate(' + 0 + ',' + 0 + ')')
            //     .call(yAxis)
            // Lasso functions
            var lassoStart = function() {
                lasso.items()
                    .attr('r', 1.5) // reset size
                    .classed('not_possible', true)
                    .classed('selected', false)
            }
            var lassoDraw = function() {
                // Style the possible dots
                lasso.possibleItems()
                    .classed('not_possible', false)
                    .classed('possible', true)
                    // .attr('r', 2.5)
                    // .style('fill', function(d, i) {
                    //     if (d.endPeriod === 201807) {
                    //         return '#fb8072'
                    //     } else {
                    //         return '#bebada'
                    //     }
                    // })

                // Style the not possible dot
                lasso.notPossibleItems()
                    .classed('not_possible', true)
                    .classed('possible', false)
                    // .attr('r', 1.5)
            }
            var lassoEnd = function() {
                // let lassoedData = []
            // Reset the color of all dots
                lasso.items()
                    .classed('not_possible', false)
                    .classed('possible', false)

                // Style the selected dots
                lasso.selectedItems()
                    .classed('selected', true)
                    .attr('r', 3)
                    // .attr('fill', 'blue')
                    .style('opacity', 1.0)
                    // console.log(d3.classed('selected', true).node().value)

                // Reset the style of the not selected dots
                lasso.notSelectedItems()
                    .attr('r', 1.5)
                    .style('opacity', 0.4)
                // var selected = lasso.selectedItems().filter(function(d) { return d.selected === true })
                // console.log('bbb:', lasso.selectedItems()._groups[0][1])
                // console.log('bbb:', lasso.selectedItems().data())
                myThis.lassoedData = lasso.selectedItems().data()
                console.log('this.lassoedData:', myThis.lassoedData)
            }
            var lasso = d3Lasso.lasso()
                .closePathSelect(true)
                .closePathDistance(100)
                .items(dots)
                .targetArea(svg)
                .on('start', lassoStart)
                .on('draw', lassoDraw)
                .on('end', lassoEnd)

            svg.call(lasso)
        }
        // fetchLassoedData: function (){
        //     dataService.fetchLassoedDataPost(lassoedData, (returnedData) => {
        //         console.log('lassoedData(post): returneddata ', returnedData )
        //         this.data = returnedData
        //     })
        // }

    },
    mounted: function () {
        this.$nextTick(() => {
            dataService.drawMDSLasso((data) => {
                console.log('SimilarityView::returned data: ', data)
                this.message2 = data.data
            })
        })
        // this.drawBarChart = new DrawBarChart('#BarChart')
        // this.drawMDSLasso = new DrawMDSLasso('#MDSLasso')
    }
}

</script>

<style>
    #SimilarityView {
        width: 422.67px;
        height: 494px;
        margin: 2px;
        /* padding-right: 15px; */
    }

    #SimilarityView .card {
        margin-bottom: 5px;
        margin-top: 5px;
        height: 410px;
        width: 426.67px;
        border-radius: 0;
        
    }

    /* #Overview .card-header {
        font-size: 12px;
        width: 360px;
        padding: 6px 12px;
        height: 34px;
    } */

    #SimilarityView .card-block {
        padding: 0px;
        position: relative;
    }

    /* #peopleview text {
        font-weight: 300;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serf;
        font-size: 14px;
    } */

    #characterContainer {
        height: calc(100% - 34px);
        /* border-radius: 2px; */
        /* border: 1px solid #fe6271; */
    }

    /* #peopleview .card-box {
        box-shadow: 0 8px 42px 0 rgba(0, 0, 0, 0.08);
        border-radius: 5px;
        background-clip: padding-box;
    } */

    /* .container-left {
        float: left;
        width: 15%;
        height: 100%;
        margin: 0px;
        overflow: auto;
        border-right: 1px solid rgba(0,0,0,.125);
    }

    .container-right {
        float: right;
        width: 85%;
        height: 100%;
        margin: 0px;
        position: relative;
    } */

    /* #peopleview .personRow {
        width: 100%;
        
        margin: 0px;
        box-shadow: 0 8px 42px 0 rgba(0, 0, 0, 0.08);
        border-radius: 5px;
        background-clip: padding-box;
    } */

     /* #peopleview .row {
        width: 100%;
        margin: 0px;
        height: 140px;
        /* margin-bottom: -25px;
    } */

    /* #peopleview .divPhoto {
        margin: auto;
        margin-top: 5px;
        max-height: 50%;
        max-width: 50%;
    }

    #peopleview .personPhoto {
        max-height: 100%;
        max-width: 100%;
    }
    #peopleview .personPhotoDiv {
        padding-top: 5px;
        padding-bottom: 5px;
        max-width: 120px;
        
    } */
    /* #peopleview .personGraph {
        min-width: calc(100% - 120px);
        height: 100%;
        padding: 0px;
    }
    #peopleview .personName {
        margin-top: 2px;
        margin-bottom: 5px;
        font-size: 14px;
        font-weight: 700;
        line-height: 18px;
    }

    #peopleview div.tooltip {
		position: absolute;
		text-align: center;
		pointer-events: none;
		font-family: sans-serif;
		font-size: 12px;
		text-anchor: middle;
		background-color: lightsteelblue;;
		border-radius: 3px;
		padding: 6px 12px;
	} */

    /* #selectedPeopleView {
        width: 100%;
        height: 100%;
        position: relative;
    }

    #heatmapDiv {
        position: absolute;
        pointer-events: none;
    }

    .heatmap-canvas {
        pointer-events: none;
    } */

    .lasso path {
            stroke: rgb(80,80,80);
            stroke-width:2px;
        }

    .lasso .drawn {
        fill-opacity:.05 ;
    }

    .lasso .loop_close {
        fill:none;
        stroke-dasharray: 4,4;
    }

    .lasso .origin {
        fill:#3399FF;
        fill-opacity:.5;
    }

    .not_possible {
        fill: rgb(200,200,200);
    }

    /* .possible {
        fill: #EC888C;
    } */

    /* .selected {
        fill: steelblue;
    }  */
/* 
    #distributionView {
        position: absolute;
        top: 0px;
        left: 0px;
        width: 400px;
        height: 150px;
        background-color: #EEEEEE;
        opacity: 1.0;
        border: 1px solid #b3aeae;
        z-index: 10000;
    }

    path {
        fill: none;
        stroke: steelblue;
        stroke-width: 2;
    } */

    /* .axis path, .axis line {
        fill: none;
        shape-rendering: crispEdges;
        stroke: #BBB;
        stroke-width: 1;
    }

    .axis text {
        fill: #766;
        font-family: 'PT Sans Narrow', sans-serif;
        font-size: 12px;
    } */
</style>
