/* eslint-disable no-undef */
/* global d3  */
let DrawMDSLasso = function(id) {

}

DrawMDSLasso.prototype.drawMDSLasso = function(data) {
    var svg = d3.select('svg')
    // var width = svg.attr('width')
    var height = svg.attr('height')

    // var dataset = data.message
    var dataset = data.data
    console.log('successful')

        // .append('svg')

    var margin = { top: 20, bottom: 20, left: 20, right: 20 }

    var xScale = d3.scaleLinear()
        .domain([d3.min(dataset, (d) => d[0]), d3.max(dataset, (d) => d[0])])
        // .domain([-7, 7])
        .range([0, height - 2 * margin.left])
    var yScale = d3.scaleLinear()
        .domain([d3.max(dataset, (d) => d[1]), d3.min(dataset, (d) => d[1])])
        // .domain([-7, 7])
        .range([0, height - 2 * margin.left])
    var scatterMDS = svg.append('g')
        .attr('transform', 'translate(' + margin.top + ',' + margin.left + ')')

    // var circles = svg.selectAll('circle')
    //     .data(data)
    //     .enter()
    //     .append('circle')
    //     .attr('cx', d => d[0] * w)
    //     .attr('cy', d => d[1] * h)
    //     .attr('r', r)
    var dots = scatterMDS.selectAll('circle')
        .data(dataset)
        .enter()
        .append('circle')
        .attr('cx', function(d, i) {
            // console.log('aaa: ', d[0])
            return xScale(d[0])
        })
        .attr('cy', function(d, i) {
            return yScale(d[1])
        })
        .attr('r', 3)
        .attr('fill', 'red')

    var xAxis = d3.axisBottom()
        .scale(xScale)
        .ticks(7)

    var yAxis = d3.axisLeft()
        .scale(yScale)
        .ticks(7)
    scatterMDS.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + 0 + ',' + (height - 2 * margin.top) + ')')
        .call(xAxis)

    scatterMDS.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(' + 0 + ',' + 0 + ')')
        .call(yAxis)
    // Lasso functions
    var lassoStart = function() {
        lasso.items()
            .attr('r', 3.5) // reset size
            .classed('not_possible', true)
            .classed('selected', false)
    }
    var lassoDraw = function() {
        // Style the possible dots
        lasso.possibleItems()
            .classed('not_possible', false)
            .classed('possible', true)

        // Style the not possible dot
        lasso.notPossibleItems()
            .classed('not_possible', true)
            .classed('possible', false)
    }
    var lassoEnd = function() {
    // Reset the color of all dots
        lasso.items()
            .classed('not_possible', false)
            .classed('possible', false)

        // Style the selected dots
        lasso.selectedItems()
            .classed('selected', true)
            .attr('r', 7)
            .attr('fill', 'green')
            // console.log(d3.classed('selected', true).node().value)

        // Reset the style of the not selected dots
        lasso.notSelectedItems()
            .attr('r', 3.5)
        // var selected = lasso.selectedItems().filter(function(d) { return d.selected === true })
        // console.log('bbb:', lasso.selectedItems()._groups[0][1])
        console.log('bbb:', lasso.selectedItems().data())
    }
    var lasso = d3.lasso()
        .closePathSelect(true)
        .closePathDistance(100)
        .items(dots)
        .targetArea(svg)
        .on('start', lassoStart)
        .on('draw', lassoDraw)
        .on('end', lassoEnd)

    svg.call(lasso)
}
export default DrawMDSLasso
