<template>
  <div v-if="!this.$parent.$parent.qasmIncludeIfFlag" class="exe">
    <button class="exeBtn" @click="exeStart">start</button>
    <button class="exeBtn" @click="preExe">⟨exe|</button>
    <button class="exeBtn" @click="nextExe">|exe⟩</button>
    <button class="exeBtn" @click="exeEnd">end</button>
  </div>
</template>
<!-- ========================================================== -->
<script>
export default {
  name: "tracingButtons",
  display: "tracingButtons",
  methods: {
    //-----------------------------------------------------------------------
    nextExe: function() {
      if (this.$parent.$parent.exeCount < this.$parent.$parent.maxWire) {
        this.$parent.$parent.exeCount++;
        this.$parent.$parent.$refs.tracingLine.updateTracingLine();
        this.$parent.$parent.sendSystem();
      }
    },
    //-----------------------------------------------------------------------
    preExe: function() {
      if (this.$parent.$parent.exeCount > 0) {
        this.$parent.$parent.exeCount--;
        this.$parent.$parent.$refs.tracingLine.updateTracingLine();
        this.$parent.$parent.sendSystem();
      }
    },
    //-----------------------------------------------------------------------
    exeStart: function() {
      if (this.$parent.$parent.exeCount != 0) {
        this.$parent.$parent.exeCount = 0;
        this.$parent.$parent.$refs.tracingLine.updateTracingLine();
        this.$parent.$parent.sendSystem();
      }
    },
    //-----------------------------------------------------------------------
    exeEnd: function() {
      if (this.$parent.$parent.exeCount != this.$parent.$parent.maxWire) {
        this.$parent.$parent.exeCount = this.$parent.$parent.maxWire;
        this.$parent.$parent.$refs.tracingLine.updateTracingLine();
        this.$parent.$parent.sendSystem();
      }
    }
    //-----------------------------------------------------------------------
    //-----------------------------------------------------------------------
  }
};
</script>
<!-- ========================================================== -->
<style scoped>
.exeBtn {
  display: inline-block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
</style>
