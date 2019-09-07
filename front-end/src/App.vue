<template>
    <div id="app">
        <div class="container-fluid">
            <div class='row'>
                <div class='col-2'>
                    <div class='row'>
                        <ControlPanel 
                          @listenToChildEvent='showMsgFromChild'
                          @changeTopKModels='changeTopKModels'
                          :modelInformation='modelInformation'
                        ></ControlPanel>
                        <!-- <View001></View001> -->
                    </div>                   
                </div>
                <div class='col-8'>
                    <div class='row'>
                        <div class='col-4'>
                            <div class='row'>
                                <SimilarityView 
                                :message='message' 
                                @listenToChildEvent='showMsgFromChild'
                                @changeLassoedDataFromSimilarityView ='changeLassoedDataFromSimilarityView'
                                ></SimilarityView>
                            </div>                            
                        </div>
                        <div class='col-8'>
                            <div class='row'>
                                <ProductView
                                :lassoedDataFromSimilarityView = 'lassoedDataFromSimilarityView'
                                :topKModels = 'topKModels'
                                @changeLassoedDataFromSimilarityView ='changeLassoedDataFromSimilarityView'
                                @changeModelInformation='changeModelInformation'
                                ></ProductView>
                            </div>                           
                        </div>                        
                    </div>
                    <div class='row'>
                        <div class='col-5'>
                            <div class="row">
                                <DetailView></DetailView>
                            </div>
                        </div>
                        <div class='col-7'>
                            <div class="row">
                                <RiskIdentificationView></RiskIdentificationView>
                            </div>        
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import 'bootstrap/dist/css/bootstrap.min.css'
    import 'bootstrap/dist/js/bootstrap.min.js'
    import 'video.js/dist/video-js.min.css'

    // import dataService from './service/dataService'

    import ControlPanel from './components/ControlPanel/ControlPanel.vue'
    import SimilarityView from './components/SimilarityView/SimilarityView.vue'
    import ProductView from './components/ProductView/ProductView.vue'
    import DetailView from './components/DetailView/DetailView.vue'
    import RiskIdentificationView from './components/RiskIdentificationView/RiskIdentificationView.vue'

    export default {
        name: 'app',
        components: {
            ControlPanel,
            SimilarityView,
            ProductView,
            DetailView,
            RiskIdentificationView
        },
        data() {
            return {
                message: 'hello child',
                lassoedDataFromSimilarityView: { },
                modelInformation: [],
                topKModels: []
            }
        },
        methods: {
            showMsgFromChild: function(data) {
                // console.log('App::' + data)
                this.message = data
                console.log(this.message)
            },
            changeLassoedDataFromSimilarityView: function(newLassoedDataFromSimilarityView) {
                this.lassoedDataFromSimilarityView = newLassoedDataFromSimilarityView
            },
    
            changeModelInformation: function(newModelInformation) {
                this.modelInformation = newModelInformation
            },

            changeTopKModels: function(newTopKModels) {
                this.topKModels = newTopKModels
            }
        },
        mounted: function () {
            // this.$nextTick(() => {
            //     dataService.initialization(this.videoName, (data) => {
            //         this.peopleVideoData = data
            //     })
            // })
        }
    }

</script>

<style>
    #app {
        width: 1920px;
        margin: 0 auto;
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        color: #2c3e50;
        background-color: white;
    }

    .container {
        width: 100%;
        /* padding: 5px 10px 5px 10px; */
    }

    .content {
        padding: 2px 2px 2px 2px;
    }

    footer {
        margin-left: 20px;
    }

    .nav-tabs-navigation {
        height: 25px;
    }
    .nav-tabs-wrapper {
        height: 25px;
    }

    .nav .nav-tabs {
        height: 25px;
    }

    .tab {
        height: 25px;
    }

    .tabs__link {
        height: 25px;
        padding: 0px;
    }

    .vue-tabs .nav > li > a {
        padding: 2px 10px 2px 10px;
    }

    .vue-tabs .nav > li span.title {
        font-size: 14px;
    }
</style>
