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

    updateTracingLine: function() {
      var qasmMargin = 0;
      var stateBtnMargin = 0;
      var gateMargin = 0;

      this.$nextTick(() => {
        if (this.$parent.$refs.qasm.qasmFlag) {
          qasmMargin = document.getElementsByClassName("editor")[0].offsetWidth;
        }
        if (document.getElementsByClassName("qubit")[0] != undefined) {
          var ele = document.getElementsByClassName("qubit")[0];
          var style = ele.currentStyle || window.getComputedStyle(ele);
          stateBtnMargin =
            document.getElementsByClassName("qubit")[0].offsetWidth +
            parseFloat(style.marginLeft) +
            parseFloat(style.marginRight);
        }
        if (document.getElementsByClassName("circuit-gate")[0] != undefined) {
          ele = document.getElementsByClassName("circuit-gate")[0];
          style = ele.currentStyle || window.getComputedStyle(ele);
          // window.console.log(style.marginLeft);
          gateMargin =
            document.getElementsByClassName("circuit-gate")[0].offsetWidth +
            parseFloat(style.marginLeft) +
            parseFloat(style.marginRight);
        }

        document.getElementById("tracingLine").style.marginLeft =
          gateMargin * this.jsonObject.exeCount +
          stateBtnMargin +
          qasmMargin +
          this.width +
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
  width: 10;
  margin-top: 0em;
  /* margin-left: 3.2em; */
  z-index: -1;
  background-color: #5b758b;
}
</style>
