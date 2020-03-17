<template>
  <div class="toolbox2">
    <button @click="addWire">add Wire</button>
    <button @click="removeWire">Remove Wire</button>
    <button @click="cloneSendSystem">send</button>
    <button @click="cloneResetSystem">reset system</button>
    <button @click="undo">undo (not working yet)</button>
    <button @click="redo">redo (not working yet)</button>
  </div>
</template>
<!-- =============================================================  -->
<script>
export default {
  name: "toolbox2",
  display: "toolbox2",
  props: ["eventQueue", "setAlgorithm"],
    computed:{
        eventIndex(){
            return this.eventQueue.length-1;
        }
    },
  methods: {
    addWire: function() {
      this.$parent.rows++;
      this.$parent.updateTracingLine();
    },
    removeWire: function() {
      this.$parent.rows--;
      this.$parent.updateTracingLine();
    },
    cloneSendSystem: function() {
      this.$parent.sendSystem();
    },
    cloneResetSystem: function() {
      this.$parent.resetSystem();
    },
    undo: function() {
        /*
      let event = this.eventQueue[this.eventIndex-1];
      if (event !== undefined) {
        this.setAlgorithm(event);
        window.console.log("event number"+this.eventIndex);
        this.eventIndex=(this.eventIndex-1)%1;
      }
      */
    },
    redo: function() {
        window.console.log(this.eventIndex);
    },
  },
};
0;
</script>
<!-- =============================================================  -->
<style scoped>
button {
  display: inline-block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
</style>
