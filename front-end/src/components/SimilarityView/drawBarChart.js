/* global d3  */

let DrawBarChart = function (id) {
    // this.svgHeight = $(id).height()
    // this.svgWidth = $(id).width()
    // this.margin = { top: 50, right: 50, bottom: 30, left: 120 }
    // this.height = this.svgHeight - this.margin.top - this.margin.bottom
    // this.width = this.svgWidth - this.margin.left - this.margin.right
    // this.svg = d3.select(id).append('svg')
    //     .attr('height', this.svgHeight)
    //     .attr('width', this.svgWidth)

    // this.graphContainer = this.svg.append('g')
    //     .attr('class', 'g_main')
    //     .attr('transform', 'translate(' + this.margin.left + ', ' + this.margin.top + ')')
}

DrawBarChart.prototype.printInfo = function (data) {
    // console.log('data from drawBarChart.js : ', data.message)
    var margin = {
        top: 30,
        bottom: 50,
        right: 20,
        left: 40
    }
    var dataset = data.data
    // var data = [40,20,50,80,10,22]
    var svg = d3.select('svg')
    var width = svg.attr('width')
    var height = svg.attr('height')
    var g = svg.append('g')
               .attr('transform', 'translate(' + margin.top + ', ' + margin.left + ')')

    var xScale = d3.scaleBand()
                   .domain(d3.range(dataset.length))
                   .rangeRound([0, width - margin.left - margin.right])
    var xAxis = d3.axisBottom(xScale)
    var yScale = d3.scaleLinear()
                   .domain([0, d3.max(dataset)])
                   .range([height - margin.top - margin.bottom, 0])
    var yAxis = d3.axisLeft(yScale)

    g.append('g')
     .attr('transform', 'translate(' + 0 + ',' + (height - margin.top - margin.bottom) + ')')
     .call(xAxis)
    g.append('g')
     .attr('transform', 'translate(0,0)')
     .call(yAxis)

    var gs = g.selectAll('.rect')
              .data(dataset)
              .enter()
              .append('g')

    var rectPadding = 20

    gs.append('rect')
      .attr('x', function(d, i) {
          return xScale(i) + rectPadding / 2
      })
      .attr('y', function(d, i) {
          var min = yScale.domain()[0]
          return yScale(min)
      })
      .attr('width', function() {
          return xScale.step() - rectPadding
      })
      .attr('height', function(d, i) {
          return 0
      })
      .on('click', function(d, i) {
          d3.select(this)
            .transition()
            .duration(1000)
            .attr('fill', 'green')
          alert(dataset[i])
      })
      .on('mouseout', function() {
          d3.select(this)
            .transition()
            .duration(1000)
            .attr('fill', 'red')
      })
      .transition()
      .duration(1500)
      .delay(function (d, i) {
          return i * 400
      })
      .attr('y', function(d, i) {
          return yScale(d)
      })
      .attr('height', function(d, i) {
          return height - margin.top - margin.bottom - yScale(d)
      })
      .attr('fill', 'blue')
}
export default DrawBarChart
