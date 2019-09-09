<template>
    <div id='risk_identification_view' class='border' style='margin: 2px 2px 2px 2px;'>
        <svg id='risk_identification_view_svg'></svg>
        <div id='risk_identification_view_tooltip'></div>
    </div>
</template>

<script>
/* global d3 */
import dataService from '../../service/dataService'

export default {
    name: 'RiskIdentificationView',
    components: {
    },
    props: {
        topKModels: Array,
        selectedItem: Object,
        productData: Array
    },
    data() {
        return {
            dataArray: [],
            topKModelData: []
        }
    },
    watch: {
        topKModels: function(newValue, oldValue) {
            console.log('RiskIdentificationView::topKModels change to: ', newValue)
        },

        selectedItem: function(newValue, oldValue) {
            console.log('RiskIdentificationView::selectedItem change to: ', newValue)

            d3.select('#risk_identification_view_svg').html('')
            d3.select('#risk_identification_view_svg')
                .attr('height', 200)

            // draw risk identification view head
            d3.select('#risk_identification_view_svg')
                .append('text')
                .attr('class', 'risk_identification_view_heading')
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
                    return 'Risk Identification View'
                })

            if (newValue !== null) {
                if (newValue.endPeriod === 201807) {
                    this.getRiskIdentificationViewData()
                }
            }
        },

        dataArray: function(newValue, oldValue) {
            // console.log('RiskIdentificationView::dataArray: ', newValue)
            this.drawRiskIdentificationView()
        },

        topKModelData: function(newValue, oldValue) {
            console.log('RiskIdentificationView::topKModelData: ', newValue)
        },

        productData: function(newValue, oldValue) {
            console.log('RiskIdentificationView::productData: ', newValue)
        }
    },
    methods: {
        getRiskIdentificationViewData: function() {
            let productData = this.productData
            let productDataBefore2017 = productData.filter(function(d, i) {
                return d.endPeriod !== 201807
            })

            productDataBefore2017 = productDataBefore2017.map(function(d) {
                return {
                    'item': d.item,
                    'endPeriod': d.endPeriod
                }
            })

            let selectedItem = this.selectedItem

            console.log('RiskIdentificationView::productDataBefore2017: ', productDataBefore2017)

            dataService.getRiskIdentificationViewData(selectedItem, productDataBefore2017, (returnedData) => {
                console.log('RiskIdentificationView::returnedData: ', returnedData)
                let topKModelData = returnedData.topKModelData
                for (let modelIndex = 0; modelIndex < topKModelData.length; modelIndex++) {
                    let currentModel = topKModelData[modelIndex]
                    let accuracyArray = currentModel.accuracy
                    let varianceArray = currentModel.variance
                    for (let cellIndex = 0; cellIndex < accuracyArray.length; cellIndex++) {
                        varianceArray[cellIndex].accuracy = accuracyArray[cellIndex].accuracy
                    }
                }
                this.topKModelData = topKModelData

                this.dataArray = returnedData.data
            })
        },

        drawRiskIdentificationView: function() {
            let myThis = this
            let dataArray = this.dataArray
            let topKModelData = this.topKModelData
            let timeSeriesLength = 43

            let totalWidth = 742.67
            let totalHeight = 431
            let margin = {top: 55, right: 10, bottom: 10, left: 10}
            // let width = totalWidth - margin.left - margin.right
            // let height = totalHeight - margin.top - margin.bottom
            let timeSeriesWidth = 244
            let timeSeriesHeight = 30
            let timeSeriesYGap = 55

            totalHeight = margin.top + dataArray.length * timeSeriesYGap

            var svg = d3.select('#risk_identification_view_svg')
                .attr('width', totalWidth)
                .attr('height', totalHeight)
                .append('g')
                .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

            var dataGroup = svg.selectAll('.data_group')
                .data(dataArray)
                .enter()
                .append('g')
                .attr('class', 'data_group')
                .attr('transform', function(d, i) {
                    let translateX = 0
                    let translateY = i * timeSeriesYGap

                    return 'translate(' + translateX + ', ' + translateY + ')'
                })

            // data group text
            dataGroup.append('g')
                .attr('class', 'item_name')
                .append('text')
                .attr('y', 0)
                .attr('x', 5)
                .attr('dy', -7)
                .attr('fill', '#212529')
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'start')
                .attr('font-size', 12)
                .text(function (d) {
                    // console.log(d)
                    return d.item + ': '
                })

            // data group delete icon
            var deleteItemIcon = dataGroup.append('g')
                .attr('class', 'delete_item_icon_group')
                .append('text')
                .attr('class', 'delete_item_icon')
                .attr('y', 0)
                .attr('x', 5)
                .attr('dy', -7)
                .attr('fill', function(d, i) {
                    return '#000000'
                })
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 12)
                .attr('cursor', 'pointer')
                .text('x')
                .style('opacity', 0.0)

            deleteItemIcon.on('mousemove', function(d) {
                deleteItemIcon.style('opacity', function(dd) {
                    if (dd === d) {
                        return 1.0
                    } else {
                        return 0.0
                    }
                })
            })
            .on('mouseout', function(d) {
                deleteItemIcon.style('opacity', 0.0)
            })

            deleteItemIcon.on('click', function(d) {
                myThis.deleteItem(d.item)
            })

            drawTrendAreaChart()
            drawHistoricalDemandLineChart()
            drawSeasonalLineChart()
            drawAcfBarChartWithConfidenceIntervals()
            drawAdfTestPValueRectangle()
            drawParallelCoordinatesPlot()

            function drawHistoricalDemandLineChart() {
                // set the ranges
                let x = d3.scaleLinear().range([0, timeSeriesWidth])
                let y = d3.scaleLinear().range([timeSeriesHeight, 0])

                // define the line
                let historicalDemandLine = d3.line()
                    .x(function(d) { return x(d.index) })
                    .y(function(d) { return y(d.historical_demand) })
                    .defined(function(d) {
                        return d.historical_demand
                    })
                    .curve(d3.curveMonotoneX)

                x.domain([0, timeSeriesLength])
                y.domain([0, 1])

                let historicalDemandGroup = dataGroup.append('g')
                    .attr('class', 'historical_demand_group')

                // draw the line
                historicalDemandGroup.selectAll('path')
                    .data(function(d) {
                        console.log('The data of path for historical demand: ', [d.new_historical_demand])
                        return [d.new_historical_demand]
                    })
                    .enter()
                    .append('path')
                    .attr('class', 'line')
                    .attr('d', historicalDemandLine)
            }

            function drawTrendAreaChart() {
                // set the ranges
                let x = d3.scaleLinear().range([0, timeSeriesWidth])
                let y = d3.scaleLinear().range([timeSeriesHeight, 0])

                // define the area
                // let historicalDemandLine = d3.line()
                //     .x(function(d) { return x(d.index) })
                //     .y(function(d) { return y(d.historical_demand) })
                //     .defined(function(d) {
                //         return d.historical_demand
                //     })
                //     .curve(d3.curveMonotoneX)
                var area = d3.area()
                    .x(function(d) { return x(d.index) })
                    .y0(timeSeriesHeight)
                    .y1(function(d) { return y(d.trend) })
                    .defined(function(d) {
                        return d.trend
                    })
                    .curve(d3.curveMonotoneX)

                x.domain([0, timeSeriesLength])
                y.domain([0, 1])

                let trendGroup = dataGroup.append('g')
                    .attr('class', 'trend_group')

                // add the area
                trendGroup.selectAll('path')
                    .data(function(d) {
                        console.log('The data of path for trend: ', [d.trend])
                        return [d.trend]
                    })
                    .enter()
                    .append('path')
                    .attr('class', 'area')
                    .attr('d', area)
            }

            function drawSeasonalLineChart() {
                let translateX = 254
                // compute min and max seasonal
                let minValue = 10000
                let maxValue = -10000
                let key = 'seasonal'
                for (let dataIndex = 0; dataIndex < dataArray.length; dataIndex++) {
                    let currentData = dataArray[dataIndex][key]
                    // console.log(currentData)
                    for (let i = 0; i < currentData.length; i++) {
                        let currentValue = currentData[i][key]
                        // console.log('currentSeasonal: ', currentValue)
                        if (currentValue !== null) {
                            if (minValue > currentValue) {
                                minValue = currentValue
                            }
                            if (maxValue < currentValue) {
                                maxValue = currentValue
                            }
                        }
                    }
                }
                console.log('minSeasonal: ', minValue)
                console.log('maxSeasonal: ', maxValue)

                // draw the line chart
                // set the ranges
                let x = d3.scaleLinear().range([0, timeSeriesWidth])
                let y = d3.scaleLinear().range([timeSeriesHeight, 0])

                // define the line
                let seasonalLine = d3.line()
                    .x(function(d) { return x(d.index) })
                    .y(function(d) { return y(d.seasonal) })
                    .defined(function(d) {
                        return d.seasonal
                    })
                    .curve(d3.curveMonotoneX)

                x.domain([0, timeSeriesLength])
                y.domain([minValue, maxValue]).nice()

                let seasonalGroup = dataGroup.append('g')
                    .attr('class', 'seasonal_group')
                    .attr('transform', function(d) {
                        return 'translate(' + translateX + ', 0)'
                    })

                // draw the line
                seasonalGroup.selectAll('path')
                    .data(function(d) {
                        console.log('The data of path for seasonal: ', [d.seasonal])
                        return [d.seasonal]
                    })
                    .enter()
                    .append('path')
                    .attr('class', 'seasonal_line')
                    .attr('d', seasonalLine)
                    // .attr('display', 'none')
            }

            function drawAcfBarChartWithConfidenceIntervals() {
                let translateX = 254
                let barWidth = 3
                // set the ranges
                let x = d3.scaleLinear().range([0, timeSeriesWidth])
                let y = d3.scaleLinear().range([timeSeriesHeight, 0])

                x.domain([0, timeSeriesLength])
                y.domain([-1, 1])

                let acfDataGroup = dataGroup.append('g')
                    .attr('class', 'acf_data_group')
                    .attr('transform', function(d) {
                        return 'translate(' + translateX + ', 0)'
                    })

                acfDataGroup.selectAll('.bar')
                    .data(function(d) {
                        console.log('The data of the bar chart for acf data: ', d.acf_data)
                        return d.acf_data
                    })
                    .enter()
                    .append('rect')
                    .attr('class', 'bar')
                    .attr('x', function(d, i) {
                        return x(i) - barWidth
                    })
                    .attr('y', function(d, i) {
                        let acfData = d.acf_data
                        if (acfData === null) {
                            return 0
                        }

                        if (acfData < 0) {
                            return timeSeriesHeight / 2
                        } else {
                            return y(acfData)
                        }
                    })
                    .attr('width', function(d, i) {
                        return barWidth
                    })
                    .attr('height', function(d, i) {
                        let acfData = d.acf_data
                        if (acfData === null) {
                            return 0
                        }

                        if (acfData < 0) {
                            return y(acfData) - timeSeriesHeight / 2
                        } else {
                            return timeSeriesHeight / 2 - y(acfData)
                        }
                    })

                // define the line
                let acfConfidenceIntervalsLowerLine = d3.line()
                    .x(function(d) { return x(d.index) })
                    .y(function(d) { return y(d.acf_confidence_intervals[0]) })
                    .defined(function(d) {
                        return d.acf_confidence_intervals
                    })
                    .curve(d3.curveMonotoneX)

                let acfConfidenceIntervalsUpperLine = d3.line()
                    .x(function(d) { return x(d.index) })
                    .y(function(d) { return y(d.acf_confidence_intervals[1]) })
                    .defined(function(d) {
                        return d.acf_confidence_intervals
                    })
                    .curve(d3.curveMonotoneX)

                let acfConfidenceIntervalsLowerLineGroup = dataGroup.append('g')
                    .attr('class', 'acf_confidence_intervals_lower_line_group')
                    .attr('transform', function(d) {
                        return 'translate(' + translateX + ', 0)'
                    })

                let acfConfidenceIntervalsUpperLineGroup = dataGroup.append('g')
                    .attr('class', 'acf_confidence_intervals_upper_line_group')
                    .attr('transform', function(d) {
                        return 'translate(' + translateX + ', 0)'
                    })

                // draw the line
                acfConfidenceIntervalsLowerLineGroup.selectAll('path')
                    .data(function(d) {
                        console.log('The data of path for acf confidence intervals: ', [d.acf_confidence_intervals])
                        return [d.acf_confidence_intervals]
                    })
                    .enter()
                    .append('path')
                    .attr('class', 'acf_confidence_intervals_line')
                    .attr('d', acfConfidenceIntervalsLowerLine)

                acfConfidenceIntervalsUpperLineGroup.selectAll('path')
                    .data(function(d) {
                        return [d.acf_confidence_intervals]
                    })
                    .enter()
                    .append('path')
                    .attr('class', 'acf_confidence_intervals_line')
                    .attr('d', acfConfidenceIntervalsUpperLine)
            }

            function drawAdfTestPValueRectangle() {
                let rectangleWidth = 15
                let rectangleHeight = 10
                let translateX = 254 * 2
                let adfTestPValueGroup = dataGroup.append('g')
                    .attr('class', 'adf_test_p_value_group')

                adfTestPValueGroup.append('rect')
                    .attr('class', 'adf_test_p_value_rect')
                    .attr('transform', function(d, i) {
                        console.log('adf_test_p_value_rect data: ', d.adf_test_p_value)
                        return 'translate(' + translateX + ', 0)'
                    })
                    .attr('x', function(d, i) {
                        return 0
                    })
                    .attr('y', function(d, i) {
                        return timeSeriesHeight / 2 - rectangleHeight / 2
                    })
                    .attr('width', function(d, i) {
                        return rectangleWidth
                    })
                    .attr('height', function(d, i) {
                        return rectangleHeight
                    })
                    .style('fill', function(d, i) {
                        let pValue = d.adf_test_p_value
                        if (pValue < 0.05) {
                            return '#add8e6'
                        } else {
                            return '#ffffff'
                        }
                    })
            }

            function drawParallelCoordinatesPlot() {
                let translateX = 254 * 2 + 15 + 10 + 20
                let parallelCoordinatesPlotWidth = 150

                // count the min and max of accuracy and variance
                let minAccuracy = 10000
                let maxAccuracy = -10000
                let minVariance = 10000
                let maxVariance = -10000

                for (let modelIndex = 0; modelIndex < topKModelData.length; modelIndex++) {
                    let currentModel = topKModelData[modelIndex]
                    let accuracyArray = currentModel.accuracy
                    let varianceArray = currentModel.variance

                    for (let i = 0; i < accuracyArray.length; i++) {
                        let currentValue = accuracyArray[i].accuracy

                        if (currentValue > -0.5) {
                            if (minAccuracy > currentValue) {
                                minAccuracy = currentValue
                            }
                            if (maxAccuracy < currentValue) {
                                maxAccuracy = currentValue
                            }
                        }
                    }
                    for (let i = 0; i < varianceArray.length; i++) {
                        let currentValue = varianceArray[i].variance

                        if (currentValue > -0.5) {
                            if (minVariance > currentValue) {
                                minVariance = currentValue
                            }
                            if (maxVariance < currentValue) {
                                maxVariance = currentValue
                            }
                        }
                    }
                }

                console.log('minAccuracy: ', minAccuracy)
                console.log('maxAccuracy: ', maxAccuracy)
                console.log('minVariance: ', minVariance)
                console.log('maxVariance: ', maxVariance)

                let translateY = timeSeriesYGap + timeSeriesHeight / 2
                let anormalX = -15

                let z = d3.scaleOrdinal()
                    .range([
                        '#fb8072', // red
                        '#80b1d3', // blue
                        '#8dd3c7', // green
                        '#bebada', // purple
                        '#fdb462' // orange
                    ])
                z.domain(['model 1', 'model 2', 'model 3', 'model 4', 'model 5'])

                let modelPerformanceAxisGroup = svg.append('g')
                    .attr('class', 'model_performance_axis_group')

                let modelItemPerformanceGroup = svg.append('g')
                    .selectAll('.model_item_performance_group')
                    .data(topKModelData)
                    .enter()
                    .append('g')
                    .attr('class', 'model_item_performance_group')
                    .attr('transform', function(d) {
                        return 'translate(' + translateX + ', ' + translateY + ')'
                    })

                let x = d3.scaleLinear().range([0, parallelCoordinatesPlotWidth])

                // define the line
                let modelPerformanceLine = d3.line()
                    .x(function(d) {
                        if (d.accuracy < -0.5) {
                            return anormalX
                        } else {
                            return x(d.accuracy)
                        }
                    })
                    .y(function(d) { return d.index * timeSeriesYGap })

                x.domain([minAccuracy, maxAccuracy]).nice()

                // draw path
                modelItemPerformanceGroup.selectAll('path')
                    .data(function(d) {
                        console.log('The data of path for top k model: ', [d.accuracy])
                        return [d.accuracy]
                    })
                    .enter()
                    .append('path')
                    .attr('class', 'seasonal_line')
                    .attr('d', modelPerformanceLine)
                    .style('stroke', function(d, i) {
                        return z(d[0].model_name)
                    })
                    .style('stroke-width', 2)

                let itemNumberForModelPerformance = topKModelData[0].accuracy.length
                console.log('itemNumberForModelPerformance: ', itemNumberForModelPerformance)

                // draw the axis
                modelPerformanceAxisGroup.selectAll('.model_performance_axis')
                    .data(topKModelData[0].accuracy)
                    .enter()
                    .append('g')
                    .attr('class', 'model_performance_axis')
                    .attr('transform', function(d, i) {
                        let currentTranslateY = i * timeSeriesYGap + translateY
                        return 'translate(' + translateX + ', ' + currentTranslateY + ')'
                    })
                    .call(d3.axisTop(x).tickFormat(d3.format('.1f')).ticks(5))

                // draw circles
                let whiteColor = d3.rgb('#FFFFFF')
                let yellowColor = d3.rgb('#f16913') // orange
                var computeYellowColor = d3.interpolate(whiteColor, yellowColor)
                var linearYellowColor = d3.scaleLinear()
                    .domain([0, 1])
                    .range([0, 1])

                modelItemPerformanceGroup.selectAll('circle')
                    .data(function(d) {
                        console.log('The data of circles for top k model: ', d.variance)
                        return d.variance
                    })
                    .enter()
                    .append('circle')
                    .attr('r', function(d, i) {
                        if (d.accuracy < -0.5) {
                            return 2
                        } else {
                            return 5
                        }
                    })
                    .attr('cx', function(d, i) {
                        if (d.accuracy < -0.5) {
                            return anormalX
                        } else {
                            return x(d.accuracy)
                        }
                    })
                    .attr('cy', function(d, i) {
                        return d.index * timeSeriesYGap
                    })
                    .style('fill', function(d, i) {
                        if (d.accuracy < -0.5) {
                            return z(d.model_name)
                        } else {
                            return computeYellowColor(linearYellowColor(d.variance / maxVariance))
                        }
                    })
                    .style('stroke-width', function(d, i) {
                        if (d.accuracy < -0.5) {
                            return 0
                        } else {
                            return 1
                        }
                    })
                    .style('stroke', function(d, i) {
                        return z(d.model_name)
                    })
            }
        },

        deleteItem: function(itemName) {
            console.log('this.deleteItem: delete ', itemName)
        }
    },
    mounted: function () {
        this.$nextTick(() => {
            // draw risk identification view head
            d3.select('#risk_identification_view_svg')
                .append('text')
                .attr('class', 'risk_identification_view_heading')
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
                    return 'Risk Identification View'
                })
        })
    }
}
</script>

<style>
    #risk_identification_view {
        /* width: 1596px; */
        width: 742.67px;
        height: 431px;
        overflow-y: auto;
        overflow-x: hidden;
    }

    #risk_identification_view #risk_identification_view_svg {
        width: 742.67px;
    }

    #risk_identification_view .tooltip {
        background-color: #fff;
        border: 2px solid #ccc;
        border-radius: 8px;
        padding: 10px;
    }

    #risk_identification_view .line {
        fill: none;
        stroke: steelblue;
        stroke-width: 2px;
    }

    #risk_identification_view .seasonal_line {
        fill: none;
        stroke: #636363;
        stroke-width: 2px;
        opacity: 0.5;
    }

    #risk_identification_view .acf_confidence_intervals_line {
        fill: none;
        stroke: lightblue;
        stroke-width: 1px;
        opacity: 0.8;
    }

    #risk_identification_view .area {
        fill: lightblue;
        opacity: 0.8;
    }

    #risk_identification_view .bar {
        fill: steelblue; 
    }

    #risk_identification_view .adf_test_p_value_rect {
        stroke: #d9d9d9;
        stroke-width: 1px;
    }

    #risk_identification_view .model_performance_axis line {
        stroke: #969696;
    }

    #risk_identification_view .model_performance_axis path {
        stroke: #969696;
    }

    #risk_identification_view .model_performance_axis text {
        fill: #969696;
        font-size: 10px;
    }

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

