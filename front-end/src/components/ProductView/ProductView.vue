
<template src='./ProductView.html'></template>

<script>
/* global d3 */
// import DrawPeople from './drawPeople.js'
import dataService from '../../service/dataService'
export default {
    name: 'ProductView',
    components: {
    },
    props: {
        lassoedDataFromSimilarityView: {}
    },
    data() {
        return {
            arcData: [],
            sortedArcData: [],
            lassoedData: []
        }
    },
    watch: {
        arcData(newValue, oldValue) {
            // this.sortedArcData = newData.sort(.....)
            this.fetchArcData(newValue)
        },
        lassoedDataFromSimilarityView(newValue, oldValue) {
            this.printLassoedData(newValue)
            dataService.fetchLassoedDataFromSimilarityViewPost(newValue, (returnedData) => {
                // 画glyph 将来把这个函数天蝎了
            })
        }
        // lassoedData: function(newValue, oldValue) {
        //     let lassoedData = this.lassoedDataFromOverview
        //     console.log('productview::lassoedData', lassoedData)
        //     return lassoedData
        // }

        // lassoedData(newValue, oldValue) {
        //     dataService.fetchLassoedDataPost(newValue, (returnedData) => {
        //         console.log('ProductView::fetchProductViewLassoedData: ', returnedData)
        //         let lassoedData = this.lassoedDataFromOverview
        //         console.log('productview::lassoedData', lassoedData)
        //     })
        // }
    },
    methods: {
        // fetchArcData2: function(data) {
        //     console.log('Overview::fetchArcData2: data: ', data)
        // },
        printLassoedData: function (data) {
            let testData = this.lassoedDataFromSimilarityView
            console.log('productView::testData::', testData.SimilarityViewData.data)
        },
        fetchArcData: function(data) {
            // console.log('fetch::productview', data)
            var numItem = 5
            var svg = d3.select('#arcData_svg')
            // let width = svg.attr('width')
            // let height = svg.attr('height')
            let innerRadius = 20
            let varianceOuterRadius = 30
            // accOuterRadious
            let arcDataset = data.slice(0, numItem)
            // console.log('arcData: ', arcDataset)
            let varancePart = svg.append('g')
                .attr('transform', 'translate(100,100)')
            // arc of varance
            let arcVarance = d3.arc()
                .innerRadius(innerRadius)
                .outerRadius(varianceOuterRadius)
                .startAngle(function(d, i) {
                    return Math.PI * 2 / 6 * i - (Math.PI * 2 / (numItem + 1))
                })
                .endAngle(function(d, i) {
                    return Math.PI * 2 / 6 * (i + 1) - (Math.PI * 2 / (numItem + 1))
                })
            //  descending order
            // dataset.sort(function(x, y) {
            //     return d3.descending(x.acc, y.acc)
            // })

            varancePart.selectAll('path')
                .data(arcDataset)
                .enter()
                .append('path')
                .attr('d', arcVarance)
                .attr('class', varancePart)
                .style('fill', function(d, i) {
                    // console.log(i)
                    // console.log('dataset::acc: ', d.acc)
                    if (i === 0) {
                        return '#fbb4ae' // red
                    } else if (i === 1) {
                        return '#b3cde3' // blue
                    } else if (i === 2) {
                        return '#ccebc5' // green
                    } else if (i === 3) {
                        return '#decbe4' // purple
                    } else {
                        return 'yellow'
                    }
                })
            // arc of acc
            var accPart = svg.append('g')
                .attr('transform', 'translate(100,100)')
                .attr('class', 'accPart')
            var accOuterRadious = d3.scaleLinear()
                .domain([0, 1.0])
                .range([30, 150])

            var arcAcc = d3.arc()
                .innerRadius(varianceOuterRadius)
                .outerRadius(function(d, i) {
                    // console.log('d:', accOuterRadious(d.acc))
                    return accOuterRadious(d.acc)
                })
                .startAngle(function(d, i) {
                    return Math.PI * 2 / 6 * i - (Math.PI * 2 / (numItem + 1))
                })
                .endAngle(function(d, i) {
                    return Math.PI * 2 / 6 * (i + 1) - (Math.PI * 2 / (numItem + 1))
                })
            accPart.selectAll('path')
                .data(arcDataset)
                .enter()
                .append('path')
                .attr('class', 'myArc')
                .style('stroke', '#fff')
                .style('stroke-width', 3)
                .attr('d', arcAcc)
                .style('fill', function(d, i) {
                    if (i === 1) {
                        return '#fbb4ae' // red
                    } else if (i === 0) {
                        return '#b3cde3' // blue
                    } else if (i === 3) {
                        return '#ccebc5' // green
                    } else if (i === 2) {
                        return 'red' // purple
                    } else {
                        return 'gray'
                    }
                })
            // draw the violin chart
            let violinDataset = data.slice(numItem, data.length)
            var histoChart = d3.histogram()
            var yScale = d3.scaleLinear()
                .domain([0, 0.55])
                .range([0, 50])
            // var yAxis = d3.axisRight().scale(yScale)

            svg.append('g')
                .attr('class', 'yAxis')

                // .attr('transform', 'translate(0,10)')

            histoChart.domain(yScale.domain())
                .thresholds(5)
                .value(d => d.acc)
            var xScale = d3.scaleLinear()
                .domain([0, 6])
                .range([0, 25])

            var area = d3.area()
                // .x0(d => -d.length)
                // .x1(d => d.length)
                .x0(function(d) {
                    return -xScale(d.length)
                })
                .x1(function(d) {
                    return xScale(d.length)
                })
                .y(d => yScale(d.x0))
                .curve(d3.curveCatmullRom)

            svg.selectAll('g.violin')
                .data([violinDataset]).enter()
                .append('g')
            // .attr('transform', (d, i) => `translate(${150 + i * 100}, 10)`).append('path')
                .attr('transform', (d, i) => 'translate(' + 30 + ',' + 100 + ')').append('path')
                .attr('transform', 'rotate(-90)')
                .style('stroke', 'black')
                .style('stroke-width', 2)
                .style('fill', 'blue')
                // .attr('d', d => area(histoChart(d)))
                .attr('d', function(d, i) {
                    // console.log('begin d: ', d)
                    return area(histoChart(d))
                })
        }
        // fetchLassoedData: function () {
        //     dataService.fetchLassoedDataPost((returnedData) => {
        //         console.log('lassoedData(post): returneddata ', returnedData)
        //         this.lassoedData = returnedData
        //     })
        // }
    },
    mounted: function () {
        dataService.fetchArcData((data) => {
            // console.log('productview::returned data: ', data)
            var arcData = data.data
            arcData.sort(function(x, y) {
                return y.acc - x.acc
            })
            // console.log('sorted arc data', arcData)

            this.arcData = arcData
        })
    }
}

</script>

<style>
    #ProductView {
        height: 100%;
        width: 840px;
        margin: 0 auto;
        /* padding-right: 15px; */
    }

    #ProductView .card {
        margin-bottom: 5px;
        margin-top: 5px;
        height: 410px;
        width: 830px;
        border-radius: 0;
    }

    /* #ProductExplorationView .card-header {
        font-size: 12px;
        width: 720px;
        padding: 6px 12px;
        height: 34px;
    } */

    /* #ProductView .card-block {
        padding: 0px;
        position: relative;
    } */

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
    }

    .lasso path {
            stroke: rgb(80,80,80);
            stroke-width:2px;
        }

    .lasso .drawn {
        fill-opacity:.05 ;
    } */

    /* .lasso .loop_close {
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

    .possible {
        fill: #EC888C;
    }

    .selected {
        fill: steelblue;
    } */
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
    #ProductView .myArc {
        border: 5px solid #000;

    }
</style>
