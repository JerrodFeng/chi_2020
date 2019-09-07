/* global d3 $ */

let DrawPeople = function (id) {
    this.svgHeight = $(id).height()
    this.svgWidth = $(id).width()
    this.margin = { top: 50, right: 50, bottom: 30, left: 120 }
    this.height = this.svgHeight - this.margin.top - this.margin.bottom
    this.width = this.svgWidth - this.margin.left - this.margin.right

    this.svg = d3.select(id).append('svg')
        .attr('height', this.svgHeight)
        .attr('width', this.svgWidth)

    this.graphContainer = this.svg.append('g')
        .attr('class', 'g_main')
        .attr('transform', 'translate(' + this.margin.left + ', ' + this.margin.top + ')')

    this.emotionList = ['angry', 'surprise', 'happy', 'neutral', 'sad', 'disgust', 'fear']
    this.colorRange = ['#fbca35', '#3ec845', '#fe6271', '#bdbdbd', '#4667cc', '#aa81f3', '#45b0e2']
    this.emotionColorRange = {
        'angry': '#fbca35',
        'disgust': '#aa81f3',
        'fear': '#45b0e2',
        'happy': '#fe6271',
        'neutral': '#bdbdbd',
        'sad': '#4667cc',
        'surprise': '#3ec845'
    }
}

DrawPeople.prototype.layout = function (data) {
    console.log('drawPeople: ', data)
}

DrawPeople.prototype.lineChart = function (data) {
    let xScale = d3.scaleLinear().range([0, this.width])
    let yScale = d3.scaleLinear().range([this.height, 0])

    let xAxis = d3.axisBottom()
        .scale(xScale)
        .ticks(5)

    let yAxis = d3.axisLeft()
        .scale(yScale)
        .ticks(5)

    let valueline = d3.line()
        .x(function (d) {
            return xScale(d.xVal)
        })
        .y(function (d) {
            return yScale(d.yVal)
        })

    // Scale the range of the data
    xScale.domain(d3.extent(data,
        function (d) {
            return d.xVal
        }))
    yScale.domain([
        0, d3.max(data,
            function (d) {
                return d.yVal
            })
    ])

    this.graphContainer.append('path')
        .attr('d', valueline(data))

    this.graphContainer.append('g') // Add the X Axis
    .attr('class', 'x axis')
    .attr('transform', 'translate(0,' + this.height + ')')
    .call(xAxis)

    this.graphContainer.append('g') // Add the Y Axis
        .attr('class', 'y axis')
        .call(yAxis)
}

export default DrawPeople
