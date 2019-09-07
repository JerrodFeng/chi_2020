/* global d3 */
import DrawPeople from './drawPeople.js'
import dataService from '../../service/dataService'

export default {
    name: 'SimilarityView',
    components: {
    },
    props: {
        videoName: String,
        peopleVideoData: Object
    },
    data() {
        return {
            peopleList: [],
            peopleInfo: {},
            allPeople: [],
            selectedPeople: []
        }
    },
    watch: {
        peopleVideoData: function (peopleVideoData) {
            this.peopleInfo = peopleVideoData['peopleData']['peopleInfo']
            this.peopleList = peopleVideoData['peopleData']['peopleList']
            this.allPeople = this.peopleList.map((d) => d['personName'])
            this.drawPeople.layout(peopleVideoData)
            dataService.lineChart('BabyFace1_S01E01', (data) => {
                console.log('lineChart: ', data)
                this.drawPeople.lineChart(data)
            })
        }
    },
    methods: {
        selectAllPeople: function () {
            this.selectedPeople = this.allPeople
            this.selectedPeople.forEach((personName) => {
                d3.select('#div-' + personName).classed('selected', true)
                d3.select('#div-' + personName).style('border', 'solid rgba(255, 0, 0, 1)')
            })
            console.log('selectAll, this.selectedPeople: ', this.selectedPeople)
        },
        removeAllPeople: function () {
            this.selectedPeople = []
            this.allPeople.forEach((personName) => {
                d3.select('#div-' + personName).classed('selected', false)
                d3.select('#div-' + personName).style('border', 'solid rgba(255, 0, 0, 0)')
            })
            console.log('removeAll, this.selectedPeople: ', this.selectedPeople)
        },
        selectPersonImage: function (event) {
            // console.log('selectPersonImage: ', event)
            // console.log('imageId: ', event.target.id)
            let personName = event.target.id.split('-')[1]
            console.log('personName: ', personName)
            if (!d3.select('#div-' + personName).classed('selected')) {
                d3.select('#div-' + personName).classed('selected', true)
                this.selectedPeople.push(personName)
                this.selectedPeople.sort()
                d3.select('#div-' + personName).style('border', 'solid rgba(255, 0, 0, 1)')
            } else {
                d3.select('#div-' + personName).classed('selected', false)
                d3.select('#div-' + personName).style('border', 'solid rgba(255, 0, 0, 0)')
                this.selectedPeople = this.selectedPeople.filter((x) => { return x !== personName })
            }
        },
        selectRemoveAll: function (event) {
            let personName = event.target.id.split('-')[1]
            if (!d3.select('#div-' + personName).classed('selected')) {
                this.selectAllPeople()
            } else {
                this.removeAllPeople()
            }
        }
    },
    mounted: function () {
        this.drawPeople = new DrawPeople('#selectedPeopleView')
    }
}
