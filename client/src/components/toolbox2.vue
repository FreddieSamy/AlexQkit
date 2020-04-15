<template>
  <div class="toolbox2">
    <button @click="addWire">add Wire</button>
    <button @click="removeWire">Remove Wire</button>
    <button @click="cloneSendSystem">send</button>
    <button @click="cloneResetSystem">reset system</button>

    <label>Save System by Name</label>
    <input type="text" v-model="savedCirciutName" />

    <button @click="saveCircuit(savedCirciutName,eventQueue[eventQueue.length-1])">Save system</button>

    <label> Select Algorithm </label>
    <select v-model="selectedAlgorithm">
      <option
        v-for="(item, index) in algorithms"
        :key="index"
        :value="item.circuit"
      >
        {{ item.name }}
      </option>
    </select>
    <!-- just devolopment block  (will be deleted)-->
    <br>
    <button @click="clearConsole">Clear Console</button>
    <!-- end development block -->
  </div>
</template>
<!-- =============================================================  -->
<script>
import { mapState } from 'vuex'
export default {
  name: "toolbox2",
  display: "toolbox2",
  props: ["eventQueue", "setAlgorithm"],
  data() {
    return {
      eventIndex: 0,
      selectedAlgorithm: null,
      savedCirciutName: "",
    };
  },
  watch: {
    selectedAlgorithm() {
      if (this.selectedAlgorithm != null) {
        this.setAlgorithm(this.selectedAlgorithm);
        this.selectedAlgorithm=null;
      }
    },
  },
  computed: {
    ...mapState(['algorithms'])
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
      this.selectedAlgorithm = null;
      this.$parent.resetSystem();
    },
    saveCircuit(name,circuit) {
      window.console.log(name);
      this.algorithms.push({'name':name,'circuit':circuit});
      this.savedCirciutName="";
    },
    clearConsole: function() {
      window.console.clear();
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
