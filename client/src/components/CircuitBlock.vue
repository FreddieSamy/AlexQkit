<template>
  <div :id="fromColumn" class="circuit-block">
    <label class="label">{{label}}</label>
  </div>
</template>
<!-- ========================================================== -->
<script>
// import { getElementWidth } from "./tracingLine.vue";

export default {
  name: "circuitBlock",
  // data() {
  //   return {
  //     label: "algorithm",
  //     fromColumn: 5,
  //     toColumn: 10
  //   };
  // },
  props: ["label", "fromColumn", "toColumn"],
  methods: {
    // ...["getElementWidth"],
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
    draw: function() {
      var qasmMargin = this.getElementWidth("editor");
      var stateBtnMargin = this.getElementWidth("qubit-state");
      var gateMargin = this.getElementWidth("circuit-gate");
      var wireNameMargin = this.getElementWidth("qubit-name");
      var deleteBtnMaargin = this.getElementWidth("delete-wire");

      document.getElementById(this.fromColumn).style.height =
        document.getElementsByClassName("circuit-wires")[0].offsetHeight +
        2 +
        "px";

      document.getElementById(this.fromColumn).style.width =
        (this.toColumn - this.fromColumn) * gateMargin - 5 + "px";

      document.getElementById(this.fromColumn).style.marginLeft =
        this.fromColumn * gateMargin +
        qasmMargin +
        stateBtnMargin +
        wireNameMargin +
        deleteBtnMaargin +
        5 +
        "px";
    }
  },
  beforeCreate() {
    this.$nextTick(() => {
      this.$nextTick(() => {
        this.draw();
      });
    });
  }
};
</script>
<!-- ========================================================== -->
<style scoped>
.circuit-block {
  border: 2px solid #2980b9;
  border-radius: 0.5em;
  z-index: -2;
  position: absolute;
  text-align: center;
  margin-top: -3px;
}
.label {
  position: relative;
  top: -10px;
  background: white;
}
</style>
