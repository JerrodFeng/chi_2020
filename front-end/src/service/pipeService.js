import Vue from 'vue'

var pipeService = new Vue({
    data: {
        FRAMESELECTEDVIDEO: 'frame_selected_video'
    },
    methods: {
        emitFrameSelectedFromVideo: function (msg) {
            this.$emit(this.FRAMESELECTEDVIDEO, msg)
        },
        onFrameSelectedFromVideo: function (callback) {
            this.$on(this.FRAMESELECTEDVIDEO, function (msg) {
                callback(msg)
            })
        }
    }
})

export default pipeService

