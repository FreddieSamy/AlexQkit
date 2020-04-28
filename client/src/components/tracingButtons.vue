<template>
  <div v-if="!this.$parent.$parent.$refs.qasm.qasmIncludeIfFlag" class="exe">
    <button class="exeBtn" @click="exeStart">start</button>
    <button class="exeBtn" @click="preExe">⟨exe|</button>
    <button class="exeBtn" @click="nextExe">|exe⟩</button>
    <button class="exeBtn" @click="exeEnd">end</button>
  </div>
</template>
<!-- ========================================================== -->
<script>
import { mapState ,mapActions } from "vuex"
export default {
  name: "tracingButtons",
  display: "tracingButtons",
  computed: {
    ...mapState(['jsonObject'])
  },
  methods: {
    ...mapActions(["runCircuit"]),
    //-----------------------------------------------------------------------
    nextExe: function() {
      if (
        this.jsonObject.exeCount < this.jsonObject.colsCount
      ) {
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
      if (
        this.jsonObject.exeCount != this.jsonObject.colsCount
      ) {
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
.exe{
  display: inline-block;
  margin: 0em 0em 0em 3em;
}
.exeBtn {
  display: inline-block;
  margin: 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;

  border:2px solid grey;

}

</style>
