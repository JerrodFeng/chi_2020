<template>
    <div id='detail_view' class='border'>
        <svg id='detail_view_svg'></svg>
        <div id='detail_view_tooltip'></div>
    </div>
</template>

<script>
/* global d3 */
import dataService from '../../service/dataService'

export default {
    name: 'DetailView',
    components: {
    },
    props: {
        topKModels: Array,
        selectedItem: Object
    },
    data() {
        return {
            modelPerformanceData: [],
            demandData: []
        }
    },
    watch: {
        selectedItem: function (newValue, oldValue) {
            console.log('DetailView::this.selectedItem change to: ', newValue)

            d3.select('#detail_view_svg').html('')
            // draw detail view head
            d3.select('#detail_view_svg')
                .append('text')
                .attr('class', 'detail_view_heading')
                .attr('y', 16)
                .attr('x', 0)
                .attr('dx', 8)
                .attr('dy', 4)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'start')
                .attr('font-size', 16)
                .text(function (d) {
                    // console.log(d)
                    return 'Detail View'
                })

            if (newValue !== null) {
                this.getDetailViewData()
            }
        },

        topKModels: function (newValue, oldValue) {
            console.log('DetailView::this.topKModels change to: ', newValue)
        },

        modelPerformanceData: function(newValue, oldValue) {
            this.drawModelPerformanceView()
        },

        demandData: function(newValue, oldValue) {
            // console.log('DetailView::demandData changes to: ', newValue)
            this.drawDemandDataView()
        }
    },
    methods: {
        getDetailViewData: function() {
            dataService.getDetailViewData(this.selectedItem, this.topKModels, (returnedData) => {
                console.log('DetailView::returnedData: ', returnedData)
                this.modelPerformanceData = returnedData.modelPerformanceData
                this.demandData = returnedData.demandData
            })
        },

        drawModelPerformanceView: function() {
            let modelPerformanceData = this.modelPerformanceData
            let topKModels = this.topKModels

            let totalWidth = 529.33
            let totalHeight = 431
            let margin = {top: 30, right: 10, bottom: 10, left: 90}

            let barChartGap = 45
            let barChartHeight = 30
            let barWidth = 25
            let barGap = 35

            var svg = d3.select('#detail_view_svg')
                .attr('width', totalWidth)
                .attr('height', totalHeight)
                .append('g')
                .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

            var modelPerformanceGroup = svg.append('g')
                .selectAll('.model_performance_group')
                .data(modelPerformanceData)
                .enter()
                .append('g')
                .attr('class', 'model_performance_group')
                .attr('transform', function(d, i) {
                    let translateX = 0
                    let translateY = i * barChartGap

                    return 'translate(' + translateX + ', ' + translateY + ')'
                })

            let y = d3.scaleLinear()
                .range([barChartHeight, 0])
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

            // text
            modelPerformanceGroup.append('g')
                .attr('class', 'model_name')
                .append('text')
                .attr('y', 6)
                .attr('x', -10)
                .attr('dy', barChartHeight / 2)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 12)
                .text(function (d) {
                    // console.log(d)
                    return d.model + ': '
                })

            modelPerformanceGroup.selectAll('.model_performance_rectangle')
                .data(function(d) {
                    return d.accuracy
                })
                .enter()
                .append('rect')
                .attr('class', 'model_performance_rectangle')
                .attr('x', function(d, i) {
                    return barGap * d.index
                })
                .attr('width', function(d, i) {
                    return barWidth
                })
                .attr('y', function(d, i) {
                    if (d.accuracy < -0.5) {
                        return 0
                    } else {
                        return y(d.accuracy)
                    }
                })
                .attr('height', function(d, i) {
                    if (d.accuracy < -0.5) {
                        return barChartHeight
                    } else {
                        return barChartHeight - y(d.accuracy)
                    }
                })
                .style('fill', function(d, i) {
                    if (d.accuracy < -0.5) {
                        return '#ffffff'
                    } else {
                        return z(d.model)
                    }
                })
                .style('stroke', function(d, i) {
                    return z(d.model)
                })
                .style('stroke-width', function(d, i) {
                    if (d.accuracy < -0.5) {
                        return 1
                    } else {
                        return 0
                    }
                })
        },

        drawDemandDataView: function() {
            let demandData = this.demandData

            let totalWidth = 529.33
            let totalHeight = 431
            let margin = {top: 30 + 225 + 15, right: 10 + 20, bottom: 10 + 30, left: 90 - 40}

            let lineChartWidth = totalWidth - margin.left - margin.right
            let lineChartHeight = totalHeight - margin.top - margin.bottom

            let demandLength = demandData[0].demand.length

            let maxDemand = -10000
            // find the max demand
            for (let i = 0; i < demandData.length; i++) {
                let currentDemandArray = demandData[i].demand
                for (let j = 0; j < currentDemandArray.length; j++) {
                    let currentDemand = currentDemandArray[j].demand
                    if (currentDemand !== null) {
                        if (maxDemand < currentDemand) {
                            maxDemand = currentDemand
                        }
                    }
                }
            }

            console.log('maxDemand: ', maxDemand)

            var svg = d3.select('#detail_view_svg')
                .attr('width', totalWidth)
                .attr('height', totalHeight)
                .append('g')
                .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

            let typeArray = demandData.map(function(d) {
                return d.type
            })

            let z = d3.scaleOrdinal()
                    .range([
                        '#969696', // gray
                        '#fbb4ae', // red
                        '#b3cde3', // blue
                        '#ccebc5', // green
                        '#decbe4', // purple
                        '#fed9a6' // orange
                    ])
            z.domain(typeArray)

            var demandDataGroup = svg.append('g')
                .selectAll('.demand_data_group')
                .data(demandData)
                .enter()
                .append('g')
                .attr('class', 'demand_data_group')
                .style('stroke', function(d, i) {
                    return z(d.type)
                })

            let x = d3.scaleLinear().range([0, lineChartWidth])
            let y = d3.scaleLinear().range([lineChartHeight, 0])

            // define the line
            let demandLine = d3.line()
                .x(function(d) { return x(d.index) })
                .y(function(d) { return y(d.demand) })
                .defined(function(d) {
                    return d.demand !== null && d.demand > -0.5
                })
                // .curve(d3.curveMonotoneX)

            x.domain([0, demandLength])
            y.domain([0, maxDemand]).nice()

            // draw the line
            demandDataGroup.selectAll('path')
                .data(function(d) {
                    console.log('The data of path for demand: ', [d.demand])
                    return [d.demand]
                })
                .enter()
                .append('path')
                .attr('class', 'demand_line')
                .attr('d', demandLine)

            // Add the X Axis
            svg.append('g')
                .attr('class', 'axis')
                .attr('transform', 'translate(0,' + lineChartHeight + ')')
                .call(d3.axisBottom(x))

            // Add the Y Axis
            svg.append('g')
                .attr('class', 'axis')
                .call(d3.axisLeft(y))

            // x axis caption
            svg.append('text')
                .attr('y', lineChartHeight)
                .attr('x', lineChartWidth)
                .attr('dy', 28)
                .attr('fill', '#969696')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 10)
                .text('month')

            // y axis caption
            svg.append('text')
                .attr('y', 0)
                .attr('x', 0)
                .attr('dy', -10)
                .attr('fill', '#969696')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 10)
                .text('demand')
        }
    },
    mounted: function () {
        this.$nextTick(() => {
            // draw detail view head
            d3.select('#detail_view_svg')
                .append('text')
                .attr('class', 'detail_view_heading')
                .attr('y', 16)
                .attr('x', 0)
                .attr('dx', 8)
                .attr('dy', 4)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'start')
                .attr('font-size', 16)
                .text(function (d) {
                    // console.log(d)
                    return 'Detail View'
                })
        })
    }
}
</script>

<style>
    #detail_view {
        width: 529.33px;
        height: 431px;
        margin: 2px;
    }

    #detail_view #detail_view_svg {
        width: 529.33px;
        height: 431px;
    }

    #detail_view .tooltip {
        background-color: #fff;
        border: 2px solid #ccc;
        border-radius: 8px;
        padding: 10px;
    }

    #detail_view .model_performance_group {
        fill: #80b1d3;
    }

    #detail_view .demand_line {
        fill: none;
        /* stroke: #636363; */
        stroke-width: 2px;
        /* opacity: 0.5; */
    }

    #detail_view .axis line {
        stroke: #969696;
    }

    #detail_view .axis path {
        stroke: #969696;
    }

    #detail_view .axis text {
        fill: #969696;
        font-size: 10px;
    }
</style>

