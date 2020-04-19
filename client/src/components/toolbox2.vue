<template>
  <div class="toolbox-2">
    <button @click="addWire">add Wire</button>
    <button @click="removeWire">Remove Wire</button>
    <button @click="cloneSendSystem">send</button>
    <button @click="cloneResetSystem">reset system</button>

    <input
      class="save-circuit"
      type="text"
      placeholder="Save Circuit by Name"
      v-model="savedCirciutName"
    />

    <button @click="saveCircuit(savedCirciutName,eventQueue[eventQueue.length-1])">Save Circuit</button>

    <label class="select-algorithm">Select an Algorithm</label>
    <select v-model="selectedAlgorithm">
      <option v-for="(item, index) in algorithms" :key="index" :value="item.circuit">{{ item.name }}</option>
    </select>

    <tracingButtons></tracingButtons>
  </div>
</template>
<!-- =============================================================  -->
<script>
import { mapState } from "vuex";
import tracingButtons from "./tracingButtons.vue";
export default {
  name: "toolbox2",
  display: "toolbox2",
  components: { tracingButtons },
  props: ["eventQueue", "setAlgorithm"],
  data() {
    return {
      eventIndex: 0,
      selectedAlgorithm: null,
      savedCirciutName: ""
    };
  },
  watch: {
    selectedAlgorithm() {
      if (this.selectedAlgorithm != null) {
        this.setAlgorithm(this.selectedAlgorithm);
        this.selectedAlgorithm = null;
      }
    }
  },
  computed: {
    ...mapState(["algorithms"])
  },
  methods: {
    addWire: function() {
      this.$parent.rows++;
      this.$parent.$refs.tracingLine.updateTracingLine();
    },
    removeWire: function() {
      this.$parent.rows--;
      this.$parent.$refs.tracingLine.updateTracingLine();
    },
    cloneSendSystem: function() {
      this.$parent.sendSystem();
    },
    cloneResetSystem: function() {
      this.selectedAlgorithm = null;
      this.$parent.resetSystem();
    },
    saveCircuit(name, circuit) {
      if (name != "") {
        window.console.log(name);
        this.algorithms.push({ name: name, circuit: circuit });
        this.savedCirciutName = "";
      } else {
        alert("Please, enter name for the algorithm");
      }
    },
    clearConsole: function() {
      window.console.clear();
    }
  }
};
0;
</script>
<!-- =============================================================  -->
<style scoped>
toolbox-2 {
  display: flex;
}
button {
  display: inline-block;
  margin: 0em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
input {
  border-radius: 7px;
}
select {
  border-radius: 7px;
  background: white;
}

.save-circuit {
  margin: 0em 0.5em 0em 13em;
}
.select-algorithm {
  margin: 0em 0.5em 0em 2em;
}

.toolbox2-buttons {
  margin: 1em;
}
</style>
