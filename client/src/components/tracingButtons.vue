<!-- all this compnent should be terminated and set functions in vuex actions -->
<template>
  <div class="exe">
    <button class="exeBtn" @click="exeStart">start</button>
    <button class="exeBtn" @click="preExe">⟨exe|</button>
    <button class="exeBtn" @click="nextExe">|exe⟩</button>
    <button class="exeBtn" @click="exeEnd">end</button>
  </div>
</template>
<!-- ========================================================== -->
<script>
import { mapState, mapActions } from "vuex";
export default {
  name: "tracingButtons",
  display: "tracingButtons",
  computed: {
    ...mapState(["jsonObject"])
  },
  methods: {
    ...mapActions(["runCircuit"]),
    //-----------------------------------------------------------------------
    nextExe: function() {
      if (this.jsonObject.exeCount < this.jsonObject.colsCount) {
        this.jsonObject.exeCount++;
        this.$parent.$parent.$refs.tracingLine.updateTracingLine();
        this.runCircuit();
      }
    },
    //-----------------------------------------------------------------------
    preExe: function() {
      if (this.jsonObject.exeCount > 0) {
        this.jsonObject.exeCount--;
        this.$parent.$parent.$refs.tracingLine.updateTracingLine();
        this.runCircuit();
      }
    },
    //-----------------------------------------------------------------------
    exeStart: function() {
      if (this.jsonObject.exeCount != 0) {
        this.jsonObject.exeCount = 0;
        this.$parent.$parent.$refs.tracingLine.updateTracingLine();
        this.runCircuit();
      }
    },
    //-----------------------------------------------------------------------
    exeEnd: function() {
      if (this.jsonObject.exeCount != this.jsonObject.colsCount) {
        this.jsonObject.exeCount = this.jsonObject.colsCount;
        this.$parent.$parent.$refs.tracingLine.updateTracingLine();
        this.runCircuit();
      }
    }
    //-----------------------------------------------------------------------
  }
};
</script>
<!-- ========================================================== -->
<style scoped>
.exe {
  display: flex;
}
.exeBtn {
  margin: 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
  border: 2px solid grey;
}
</style>
