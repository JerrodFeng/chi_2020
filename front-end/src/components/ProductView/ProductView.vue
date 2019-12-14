<template>
    <div id="ProductView" class='border'>
        <div id="change_glyph_type_checkbox">
            <input type="checkbox" v-model="isBarChartBased">
        </div>
        <div id="change_glyph_type_text">
            bar:
        </div>
        <!-- <div id='product_view_svg_div'> -->
        <svg id = 'product_view_svg'></svg>
        <!-- </div> -->
    </div>
</template>

<script>
/* global d3 */
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'
import dataService from '../../service/dataService'

export default {
    name: 'ProductView',
    components: {
    },
    props: {
        lassoedDataFromSimilarityView: Object,
        topKModels: Array,
        itemCategoryDictionary: Object
    },
    data() {
        return {
            productData: [],
            modelInformation: [],
            selectedItem: null,
            product201807Border: null,
            productBefore201807Border: null,
            maxModelVariance: 1.0,
            glyphType: 0, // circular design: 0, bar chart based design: 1
            isBarChartBased: false
        }
    },
    watch: {
        lassoedDataFromSimilarityView(newValue, oldValue) {
            // this.printLassoedData(newValue)
            dataService.fetchLassoedDataFromSimilarityViewPost(newValue, (returnedData) => {
                // 画glyph 将来把这个函数天蝎了
                console.log('ProductView::returnedData: ', returnedData)
                this.maxModelVariance = returnedData.maxModelVariance
                this.productData = returnedData.lassoedDataInformation
                this.modelInformation = returnedData.modelInformation
            })
        },

        maxModelVariance: function(newValue, oldValue) {
            this.$emit('changeMaxModelVariance', newValue)
        },

        productData: function(newValue, oldValue) {
            console.log('ProductView::productData: ', newValue)
            this.$emit('changeProductData', newValue)
        },

        modelInformation: function(newValue, oldValue) {
            this.$emit('changeModelInformation', {'modelInformation': newValue, 'maxModelVariance': this.maxModelVariance})
        },

        topKModels: function(newValue, oldValue) {
            console.log('ProductView::topKModels change to: ', newValue)
            this.selectedItem = null

            this.drawProductView()
        },

        selectedItem: function(newValue, oldValue) {
            console.log('ProductView::selectedItem change to: ', newValue)
            if (newValue !== null) {
                this.product201807Border.style('opacity', function(dd) {
                    if (dd.item === newValue.item && dd.endPeriod === newValue.endPeriod) {
                        return 1.0
                    }
                    return 0.0
                })
                this.productBefore201807Border.style('opacity', function(dd) {
                    if (dd.item === newValue.item && dd.endPeriod === newValue.endPeriod) {
                        return 1.0
                    }
                    return 0.0
                })
            }

            this.$emit('changeSelectedItem', newValue)
        },

        glyphType: function(newValue, oldValue) {
            this.selectedItem = null
            this.drawProductView()
        },

        isBarChartBased: function(newValue, oldValue) {
            console.log('ProductView::isBarChartBased change to: ', newValue)
            if (newValue === true) {
                this.glyphType = 1
            } else {
                this.glyphType = 0
            }
        }
    },
    methods: {
        drawProductView: function() {
            let myThis = this
            let productData201807 = this.productData.filter(function(d, i) {
                return d.endPeriod === 201807
            })
            console.log('ProductView::productData201807: ', productData201807)
            let productDataBefore201807 = this.productData.filter(function(d, i) {
                return d.endPeriod !== 201807
            })
            console.log('ProductView::productDataBefore201807: ', productDataBefore201807)
            let topKModels = this.topKModels

            // colors for top k models
            let z = d3.scaleOrdinal()
                    .range([
                        '#fbb4ae', // red
                        '#b3cde3', // blue
                        '#ccebc5', // green
                        '#decbe4', // purple
                        '#fed9a6' // orange
                    ])
            z.domain(topKModels)

            let rowCapacity = 7

            let productData201807RowNumber = 0
            if (productData201807.length !== 0) {
                productData201807RowNumber = Math.ceil(productData201807.length / rowCapacity)
            }
            let productDataBefore201807RowNumber = 0
            if (productDataBefore201807.length !== 0) {
                productDataBefore201807RowNumber = Math.ceil(productDataBefore201807.length / rowCapacity)
            }

            let productGlyphSize = 90
            let productGlyphGap = 120

            let barChartHeight = 60
            let barChartHeightGap = 90

            let margin = {top: 50 + 10, right: 80, bottom: 10, left: 10}
            let totalWidth = 849.33
            let totalHeight = margin.top + margin.bottom + productData201807RowNumber * barChartHeightGap + productDataBefore201807RowNumber * productGlyphGap
            totalHeight = Math.max(487, totalHeight)

            d3.select('#product_view_svg').html('')

            // draw product view head
            d3.select('#product_view_svg')
                .append('text')
                .attr('class', 'product_view_heading')
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
                    return 'Product View'
                })

            let svg = d3.select('#product_view_svg')
                .attr('width', totalWidth)
                .attr('height', totalHeight)
                .append('g')
                .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')')

            let product201807Group = svg.append('g')
                .selectAll('.product_201807_group')
                .data(productData201807)
                .enter()
                .append('g')
                .attr('class', 'product_201807_group')
                .attr('transform', function(d, i) {
                    let translateX = i % rowCapacity * productGlyphGap
                    let translateY = Math.floor(i / rowCapacity) * barChartHeightGap

                    return 'translate(' + translateX + ', ' + translateY + ')'
                })

            this.product201807Border = product201807Group.append('rect')
                .attr('class', 'product_201807_border_rect')
                .attr('x', -2)
                .attr('y', -2)
                .attr('width', productGlyphSize + 4)
                .attr('height', barChartHeight + 4)
                .style('fill', '#ffffff')
                .style('stroke', '#fbb4ae')
                .style('stroke-width', 1)
                .style('opacity', 0.0)

            let x = d3.scaleBand()
                .range([0, productGlyphSize])
                .padding(0.1)
            let y = d3.scaleLinear()
                .range([barChartHeight, 0])

            x.domain(topKModels)
            y.domain([0, 1])

            let product201807Bar = product201807Group.selectAll('.product_201807_bar')
                .data(function(d) {
                    console.log('d: ', d)
                    let newD = []
                    for (let i = 0; i < topKModels.length; i++) {
                        let currentModel = topKModels[i]
                        let modelData = d.model
                        let forecastedValue = -1
                        for (let j = 0; j < modelData.length; j++) {
                            let currentModelData = modelData[j]
                            if (currentModelData.model === currentModel) {
                                forecastedValue = currentModelData.predictValue
                            }
                        }

                        newD.push({
                            'item': d.item,
                            'endPeriod': d.endPeriod,
                            'model': currentModel,
                            'predictValue': forecastedValue
                        })
                    }
                    console.log('newD: ', newD)

                    return newD
                })
                .enter()
                .append('rect')
                .attr('class', 'product_201807_bar')
                .attr('x', function(d, i) {
                    return x(d.model)
                })
                .attr('width', function(d, i) {
                    return x.bandwidth()
                })
                .attr('y', function(d, i) {
                    if (d.predictValue < -0.5) {
                        return 0
                    } else {
                        if (d.predictValue > 1) {
                            return y(1)
                        } else {
                            return y(d.predictValue)
                        }
                    }
                })
                .attr('height', function(d, i) {
                    if (d.predictValue < -0.5) {
                        return barChartHeight
                    } else {
                        if (d.predictValue > 1) {
                            return barChartHeight - y(1)
                        } else {
                            return barChartHeight - y(d.predictValue)
                        }
                    }
                })
                .attr('fill', function(d, i) {
                    if (d.predictValue < -0.5) {
                        return '#ffffff'
                    } else {
                        return z(d.model)
                    }
                })
                .attr('stroke', function(d, i) {
                    if (d.predictValue < -0.5) {
                        return z(d.model)
                    } else {
                        return '#969696'
                    }
                })
                .attr('stroke-width', function(d, i) {
                    if (d.predictValue < -0.5) {
                        return 1
                    } else {
                        if (d.predictValue > 1) {
                            return 1
                        } else {
                            return 0
                        }
                    }
                })

            product201807Bar.on('click', function(d) {
                myThis.selectedItem = {
                    'item': d.item,
                    'endPeriod': d.endPeriod
                }
            })

            let productBefore201807Group = svg.append('g')
                .selectAll('.product_before_201807_group')
                .data(productDataBefore201807)
                .enter()
                .append('g')
                .attr('class', 'product_before_201807_group')
                .attr('transform', function(d, i) {
                    let translateX = i % rowCapacity * productGlyphGap
                    let translateY = Math.floor(i / rowCapacity) * productGlyphGap + productData201807RowNumber * barChartHeightGap

                    translateX = translateX + productGlyphSize / 2
                    translateY = translateY + productGlyphSize / 2

                    return 'translate(' + translateX + ', ' + translateY + ')'
                })

            this.productBefore201807Border = productBefore201807Group.append('rect')
                .attr('class', 'product_before_201807_border_rect')
                .attr('x', -2 - productGlyphSize / 2)
                .attr('y', -2 - productGlyphSize / 2)
                .attr('width', productGlyphSize + 4)
                .attr('height', productGlyphSize + 4)
                .style('fill', '#ffffff')
                .style('stroke', '#fbb4ae')
                .style('stroke-width', 1)
                .style('opacity', 0.0)

            let varianceInnerRadius = 10
            let varianceOuterRadius = 16
            let accuracyMaxOuterRadius = 45

            let theK = topKModels.length

            // compute the max value of variance
            let maxVariance = -10000
            for (let i = 0; i < productDataBefore201807.length; i++) {
                let currentModels = productDataBefore201807[i].model

                for (let j = 0; j < currentModels.length; j++) {
                    let currentModel = currentModels[j]
                    let modelItemVar = currentModel.modelItemVar

                    if (maxVariance < modelItemVar) {
                        maxVariance = modelItemVar
                    }
                }
            }
            console.log('ProductView::maxVariance: ', maxVariance)
            this.drawLegend(maxVariance)

            let whiteColor = d3.rgb('#FFFFFF')
            let yellowColor = d3.rgb('#f16913') // orange
            let computeYellowColor = d3.interpolate(whiteColor, yellowColor)
            let linearYellowColor = d3.scaleLinear()
                .domain([0, 1])
                .range([0, 1])

            if (this.glyphType === 0) {
                let varianceArc = d3.arc()
                    .innerRadius(varianceInnerRadius)
                    .outerRadius(varianceOuterRadius)
                    .startAngle(function(d, i) {
                        return (Math.PI * 2 / (theK + 1)) * (i - 1)
                    })
                    .endAngle(function(d, i) {
                        return (Math.PI * 2 / (theK + 1)) * i
                    })

                // draw variance arc
                productBefore201807Group.append('g')
                    .attr('class', 'product_glyph_variance_group')
                    .selectAll('path')
                    .data(function(d, i) {
                        let result = d.model.filter(function(d, i) {
                            return i < theK
                        })

                        // console.log('result: ', result)
                        return result
                    })
                    .enter()
                    .append('path')
                    .attr('d', varianceArc)
                    .style('fill', function(d, i) {
                        return computeYellowColor(linearYellowColor(d.modelItemVar / maxVariance))
                    })
                    .style('stroke', '#d9d9d9')
                    .style('stroke-width', 1)

                // draw accuracy arc
                let accuracyY = d3.scaleLinear()
                    .domain([0, 1])
                    .range([varianceOuterRadius, accuracyMaxOuterRadius])

                let accuracyArc = d3.arc()
                    .innerRadius(varianceOuterRadius)
                    .outerRadius(function(d, i) {
                        return accuracyY(d.accuracy)
                    })
                    .startAngle(function(d, i) {
                        return (Math.PI * 2 / (theK + 1)) * (i - 1)
                    })
                    .endAngle(function(d, i) {
                        return (Math.PI * 2 / (theK + 1)) * i
                    })

                let productBefore201807Arc = productBefore201807Group.append('g')
                    .attr('class', 'product_glyph_accuracy_group')
                    .selectAll('path')
                    .data(function(d, i) {
                        let result = d.model.filter(function(d, i) {
                            return i < theK
                        })

                        // console.log('result: ', result)
                        return result
                    })
                    .enter()
                    .append('path')
                    .attr('d', accuracyArc)
                    .style('fill', function(d, i) {
                        if (topKModels.includes(d.model)) {
                            return z(d.model)
                        } else {
                            return '#ffffff'
                        }
                    })
                    .style('stroke', '#d9d9d9')
                    .style('stroke-width', 1)

                productBefore201807Arc.on('click', function(d) {
                    myThis.selectedItem = {
                        'item': d.item,
                        'endPeriod': d.endPeriod
                    }
                })

                // draw the violin chart
                var histoChart = d3.histogram()
                var yScale = d3.scaleLinear()
                    .domain([0, 1])
                    .range([-varianceOuterRadius, -accuracyMaxOuterRadius])

                histoChart.domain(yScale.domain())
                    .thresholds(yScale.ticks(12))
                    .value(d => d.accuracy)
                var xScale = d3.scaleLinear()
                    .domain([0, 20])
                    .range([0, 15])

                var area = d3.area()
                    .x0(function(d) {
                        return -xScale(d.length)
                    })
                    .x1(function(d) {
                        return xScale(d.length)
                    })
                    .y(d => yScale(d.x0))
                    .curve(d3.curveCatmullRom)

                productBefore201807Group.append('g')
                    .attr('class', 'product_glyph_violin_group')
                    .selectAll('g')
                    .data(function(d, i) {
                        let result = d.model.filter(function(d, i) {
                            return i >= theK
                        })
                        return [result]
                    })
                    .enter()
                    .append('g')
                    .append('path')
                    .attr('transform', 'rotate(-90)')
                    .style('fill', '#d9d9d9')
                    .attr('d', function(d, i) {
                        return area(histoChart(d))
                    })
            } else { // draw bar chart based design
                let barGlyphX = d3.scaleBand()
                    .range([0, productGlyphSize - 15])
                    .padding(0.15)
                let barGlyphY = d3.scaleLinear()
                    .range([productGlyphSize - 17, 0])

                let xDomain = []
                for (let i = 0; i < theK; i++) {
                    xDomain.push(i)
                }
                barGlyphX.domain(xDomain)
                barGlyphY.domain([0, 1])

                // the part of bar chart: for accuracy
                let barGlyphBarGroup = productBefore201807Group.append('g')
                    .attr('class', 'bar_glyph_bar_group')
                    .attr('transform', function(d) {
                        let translateX = -productGlyphSize / 2
                        let translateY = -productGlyphSize / 2
                        return 'translate(' + translateX + ', ' + translateY + ')'
                    })

                // draw accuracy bar chart
                let barGlyphBar = barGlyphBarGroup.selectAll('.bar_glyph_bar')
                    .data(function(d) {
                        console.log('productView::barGlyphBarGroupData::d:', d)
                        let newD = []
                        let modelData = d.model
                        for (let i = 0; i < topKModels.length; i++) {
                            newD.push({
                                'item': d.item,
                                'endPeriod': d.endPeriod,
                                'model': modelData[i].model,
                                'accuracy': modelData[i].accuracy,
                                'variance': modelData[i].modelItemVar
                            })
                        }
                        console.log('productView::barGlyphBarGroupData::newD:', newD)

                        return newD
                    })
                    .enter()
                    .append('rect')
                    .attr('class', 'bar_glyph_bar')
                    .attr('x', function(d, i) {
                        // console.log('productView::barGlyph::i:', i)
                        return barGlyphX(i)
                    })
                    .attr('width', function(d, i) {
                        return barGlyphX.bandwidth()
                    })
                    .attr('y', function(d, i) {
                        return barGlyphY(d.accuracy)
                    })
                    .attr('height', function(d, i) {
                        return productGlyphSize - 17 - barGlyphY(d.accuracy)
                    })
                    .style('fill', function(d, i) {
                        if (topKModels.includes(d.model)) {
                            return z(d.model)
                        } else {
                            return '#ffffff'
                        }
                    })
                    .style('stroke', function(d) {
                        // if (topKModels.includes(d.model)) {
                        //     return z(d.model)
                        // } else {
                        //     return '#d9d9d9'
                        // }
                        return '#d9d9d9'
                    })
                    .style('stroke-width', 1)

                barGlyphBar.on('click', function(d) {
                    myThis.selectedItem = {
                        'item': d.item,
                        'endPeriod': d.endPeriod
                    }
                })

                // draw variance rectangle
                barGlyphBarGroup.selectAll('.bar_glyph_bar_var')
                    .data(function(d) {
                        // console.log('productView::barGlyphBarGroupData::d:', d)
                        let newD = []
                        let modelData = d.model
                        for (let i = 0; i < topKModels.length; i++) {
                            newD.push({
                                'item': d.item,
                                'endPeriod': d.endPeriod,
                                'model': modelData[i].model,
                                'accuracy': modelData[i].accuracy,
                                'variance': modelData[i].modelItemVar
                            })
                        }
                        // console.log('productView::barGlyphBarGroupData::newD:', newD)

                        return newD
                    })
                    .enter()
                    .append('rect')
                    .attr('class', 'bar_glyph_bar_var')
                    // .attr('transform', function(d) {
                    //     let translateX = 0
                    //     let translateY = 2
                    //     return 'translate(' + translateX + ', ' + translateY + ')'
                    // })
                    .attr('x', function(d, i) {
                        // console.log('productView::barGlyph::i:', i)
                        return barGlyphX(i)
                    })
                    .attr('width', function(d, i) {
                        return barGlyphX.bandwidth()
                    })
                    .attr('y', function(d, i) {
                        return productGlyphSize - 15
                    })
                    .attr('height', function(d, i) {
                        return 15
                    })
                    .style('fill', function(d, i) {
                        return computeYellowColor(linearYellowColor(d.variance / maxVariance))
                    })
                    .style('stroke', '#d9d9d9')
                    .style('stroke-width', 1)

                // draw the margin density plot
                let histoChart = d3.histogram()
                let yScale = d3.scaleLinear()
                    .domain([0, 1])
                    .range([productGlyphSize - 15, 0])

                histoChart.domain(yScale.domain())
                    .thresholds(yScale.ticks(12))
                    .value(d => d.accuracy)
                let xScale = d3.scaleLinear()
                    .domain([0, 20])
                    .range([0, 15])

                let area = d3.area()
                    .x0(function(d) {
                        // return -xScale(d.length)
                        return 0
                    })
                    .x1(function(d) {
                        return xScale(d.length)
                    })
                    .y(d => yScale(d.x0))
                    .curve(d3.curveCatmullRom)

                productBefore201807Group.append('g')
                    .attr('class', 'product_glyph_violin_group')
                    .attr('transform', function(d, i) {
                        let translateX = -productGlyphSize / 2 + productGlyphSize - 15
                        let translateY = -productGlyphSize / 2
                        return 'translate(' + translateX + ', ' + translateY + ')'
                    })
                    .selectAll('g')
                    .data(function(d, i) {
                        let result = d.model.filter(function(d, i) {
                            return i >= theK
                        })
                        return [result]
                    })
                    .enter()
                    .append('g')
                    .append('path')
                    // .attr('transform', 'rotate(-90)')
                    .style('fill', '#d9d9d9')
                    .attr('d', function(d, i) {
                        return area(histoChart(d))
                    })
            }

            // bar chart text
            product201807Group.append('text')
                    .attr('y', 0)
                    .attr('x', -5)
                    .attr('dy', -6)
                    .attr('fill', '#212529')
                    .attr('font-family', 'sans-serif')
                    .attr('text-anchor', 'start')
                    .attr('font-size', 14)
                    .text(function (d) {
                        // console.log(d)
                        let item = d.item
                        let category = 'other'
                        if (item in myThis.itemCategoryDictionary) {
                            category = myThis.itemCategoryDictionary[item]
                        }
                        return d.item + ' (' + category + '):'
                    })

            // product glyph text
            productBefore201807Group.append('text')
                    .attr('y', -productGlyphSize / 2)
                    .attr('x', -productGlyphSize / 2 - 5)
                    .attr('dy', -6)
                    .attr('fill', '#212529')
                    .attr('font-family', 'sans-serif')
                    .attr('text-anchor', 'start')
                    .attr('font-size', 14)
                    .text(function (d) {
                        // console.log(d)
                        let item = d.item
                        let category = 'other'
                        if (item in myThis.itemCategoryDictionary) {
                            category = myThis.itemCategoryDictionary[item]
                        }
                        return d.item + ' (' + category + '):'
                    })
        },

        drawProductView2: function(data) {
            // console.log('fetch::productview', data)
            var numItem = 5
            var svg = d3.select('#product_view_svg')
                .append('g')
                .attr('transform', 'translate(100, 100)')
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
        },

        drawLegend: function(maxVariance) {
            // variance legend
            let legendWidth = 80 - 15
            let legendHeight = 10
            let totalWidth = 849.33

            let whiteColor = d3.rgb('#FFFFFF')
            let yellowColor = d3.rgb('#f16913')

            var gradientLegendGroup = d3.select('#product_view_svg')
                .append('g')
                .attr('class', 'gradient_legend_group')

            var gradientLegend = gradientLegendGroup.append('defs')
                .append('linearGradient')
                .attr('id', 'gradient_legend')
                .attr('x1', '0%') // bottom
                .attr('y1', '0%')
                .attr('x2', '100%') // to top
                .attr('y2', '0%')
                .attr('spreadMethod', 'pad')

            gradientLegend.append('stop')
                .attr('offset', '0%')
                .attr('stop-color', whiteColor)
                .attr('stop-opacity', 1)

            // gradientLegend.append('stop')
            //     .attr('offset', '50%')
            //     .attr('stop-color', grayColor)
            //     .attr('stop-opacity', 1)

            gradientLegend.append('stop')
                .attr('offset', '100%')
                .attr('stop-color', yellowColor)
                .attr('stop-opacity', 1)

            gradientLegendGroup.append('rect')
                .attr('width', legendWidth)
                .attr('height', legendHeight)
                .style('fill', 'url(#gradient_legend)')
                .attr('transform', function(d) {
                    let tempX = totalWidth - 140 - 35
                    let tempY = 10

                    return 'translate(' + tempX + ', ' + tempY + ')'
                })

            gradientLegendGroup.append('text')
                .attr('y', 10)
                .attr('x', totalWidth - 140 + 85 - 35 - 15)
                .attr('dy', 8 + 2)
                .attr('fill', function(d, i) {
                    // let tempColor = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4']
                    // return tempColor[i]
                    return '#000000'
                })
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'start')
                .attr('font-size', 14)
                .text(maxVariance.toFixed(4))

            gradientLegendGroup.append('text')
                .attr('y', 10)
                .attr('x', totalWidth - 140 - 5 - 35)
                .attr('dy', 8 + 2)
                .attr('fill', function(d, i) {
                    // let tempColor = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4']
                    // return tempColor[i]
                    return '#000000'
                })
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 14)
                .text('0')

            gradientLegendGroup.append('text')
                .attr('y', 10)
                .attr('x', totalWidth - 140 - 5 - 15 - 33)
                .attr('dy', 8 + 2)
                .attr('fill', function(d, i) {
                    // let tempColor = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4']
                    // return tempColor[i]
                    return '#000000'
                })
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'end')
                .attr('font-size', 14)
                .text('var: ')

            // model legend
            let topKModels = this.topKModels

            // colors for top k models
            let z = d3.scaleOrdinal()
                .range([
                    '#fbb4ae', // red
                    '#b3cde3', // blue
                    '#ccebc5', // green
                    '#decbe4', // purple
                    '#fed9a6' // orange
                ])
            z.domain(topKModels)

            let modelLegend = d3.select('#product_view_svg').append('g')
                .attr('class', 'model_legend_group')
                .selectAll('.model_legend')
                .data(topKModels)
                .enter()
                .append('g')
                .attr('class', 'model_legend')
                .attr('transform', function(d, i) {
                    let translateX = totalWidth - 720 + i * 100
                    let translateY = 10
                    return 'translate(' + translateX + ', ' + translateY + ')'
                })

            modelLegend.append('rect')
                .attr('x', 0)
                .attr('width', 15)
                .attr('y', (10 - 15) / 2)
                .attr('height', 15)
                .style('fill', function(d) {
                    return z(d)
                })

            modelLegend.append('text')
                .attr('y', 0)
                .attr('x', 15 + 5)
                .attr('dy', 8 + 2)
                .attr('fill', function(d, i) {
                    // let tempColor = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4']
                    // return tempColor[i]
                    return '#000000'
                })
                .attr('font-family', 'sans-serif')
                .attr('text-anchor', 'start')
                .attr('font-size', 14)
                .text(function(d) {
                    return d
                    // return 'lstm_classic'
                })

            d3.select('#change_glyph_type_checkbox').style('display', 'block')
            d3.select('#change_glyph_type_text').style('display', 'block')

            // gradientLegendGroup.append('text')
            //     .attr('y', 10)
            //     .attr('x', totalWidth - 30)
            //     .attr('dy', 8 + 2)
            //     .attr('fill', function(d, i) {
            //         // let tempColor = ['#fbb4ae', '#b3cde3', '#ccebc5', '#decbe4']
            //         // return tempColor[i]
            //         return '#000000'
            //     })
            //     .attr('font-family', 'sans-serif')
            //     .attr('text-anchor', 'end')
            //     .attr('font-size', 14)
            //     .text('bar: ')
        }
    },
    mounted: function () {
        this.$nextTick(() => {
            d3.select('#product_view_svg')
            .attr('width', 849.33)
            .attr('height', 487)

            // draw product view head
            d3.select('#product_view_svg')
                .append('text')
                .attr('class', 'product_view_heading')
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
                    return 'Product View'
                })
        })
    }
}

</script>

<style>
    #ProductView {
        width: 849.33px;
        height: 494px;
        margin: 2px;
        /* padding-right: 15px; */
        overflow-y: auto;
        overflow-x: hidden;
    }

    #ProductView #product_view_svg {
        width: 849.33px;
        /* height: 494px; */
        /* margin: 0; */
        /* padding-right: 15px; */
        
    }

    #ProductView .card {
        margin-bottom: 5px;
        margin-top: 5px;
        height: 410px;
        width: 830px;
        border-radius: 0;
    }

    #ProductView #change_glyph_type_checkbox {
        position: absolute;
        top: 7px; 
        left: 828px;
        /* left: 798px; */
        display: none;
        font-family: sans-serif;
        font-size: 14px;
        fill: #000000;
    }

    #ProductView #change_glyph_type_text {
        position: absolute;
        top: 6px; 
        /* left: 828px; */
        left: 798px;
        display: none;
        font-family: sans-serif;
        font-size: 14px;
        fill: #000000;
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
