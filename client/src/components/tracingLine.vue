<template>
  <hr
    v-if="!this.$parent.circuitDrawingFlag"
    id="tracingLine"
    :width="width"
    :size="updateTracingLine()"
  />
</template>
<!-- ========================================================== -->
<script>
import { mapState } from "vuex";

export default {
  name: "tracingLine",
  display: "tracingLine",
  data() {
    return {
      width: 2
    };
  },
  computed: {
    ...mapState(["jsonObject"])
  },
  methods: {
    //-----------------------------------------------------------------------
    getElementWidth: function(className) {
      if (document.getElementsByClassName(className)[0] != undefined) {
        var ele = document.getElementsByClassName(className)[0];
        var style = ele.currentStyle || window.getComputedStyle(ele);
        return (
          document.getElementsByClassName(className)[0].offsetWidth +
          parseFloat(style.marginLeft) +
          parseFloat(style.marginRight)
        );
      }
      return 0;
    },
    updateTracingLine: function() {
      this.$nextTick(() => {
        var qasmMargin = this.getElementWidth("editor");
        var stateBtnMargin = this.getElementWidth("qubit-state");
        var gateMargin = this.getElementWidth("circuit-gate");
        var wireNameMargin = this.getElementWidth("qubit-name");
        var deleteBtnMaargin = this.getElementWidth("delete");

        document.getElementById("tracingLine").style.marginLeft =
          gateMargin * this.jsonObject.exeCount +
          stateBtnMargin +
          qasmMargin +
          wireNameMargin +
          deleteBtnMaargin +
          this.width +
          1 +
          "px";
        document.getElementById(
          "tracingLine"
        ).size = document.getElementsByClassName(
          "circuit-wires"
        )[0].offsetHeight;
      });
    }
    //-----------------------------------------------------------------------
  }
};
</script>
<!-- ========================================================== -->
<style scoped>
#tracingLine {
  position: absolute;
  margin-top: 0em;
  z-index: -1;
  background-color: #5b758b;
}
</style>
