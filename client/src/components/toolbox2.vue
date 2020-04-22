<template>
  <div class="toolbox-2">
    <button @click="addWire">add Wire</button>
    <button @click="removeWire">Remove Wire</button>
    <button @click="cloneSendSystem">send</button>
    <button @click="cloneResetSystem">reset system</button>
    <tracingButtons></tracingButtons>
    <input
      class="save-circuit"
      type="text"
      placeholder="Save Circuit by Name"
      v-model="savedCirciutName"
    />

    <button @click="saveCircuit(savedCirciutName)">Save Circuit</button>

    <label class="select-algorithm">Select an Algorithm</label>
    <select v-model="selectedAlgorithm">
      <option v-for="(item, index) in algorithms" :key="index" :value="item.circuit">{{ item.name }}</option>
    </select>

    
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
  props: ["setAlgorithm"],
  data() {
    return {
      selectedAlgorithm: null,
      savedCirciutName: ""
    };
  },
  watch: {
    selectedAlgorithm() {
      if (this.selectedAlgorithm != null) {
        //window.console.log(this.selectedAlgorithm)
        this.setAlgorithm(this.selectedAlgorithm);
        this.selectedAlgorithm = null;
      }
    }
  },
  computed: {
    ...mapState(["algorithms"]),
    ...mapState(["jsonObject"])
  },
  methods: {
    addWire: function() {
      this.$parent.jsonObject.wires++;
      this.$parent.$refs.tracingLine.updateTracingLine();
    },
    removeWire: function() {
      this.$parent.jsonObject.wires--;
      this.$parent.jsonObject.init.pop();
      this.$parent.$refs.tracingLine.updateTracingLine();
    },
    cloneSendSystem: function() {
      this.$parent.sendSystem();
    },
    cloneResetSystem: function() {
      this.selectedAlgorithm = null;
      this.$parent.resetSystem();
    },
    saveCircuit(name) {
      if (name != "") {
        if (this.$parent.maxWire) {
          this.algorithms.push({
            name: name,
            circuit: {
              wires: this.jsonObject.wires,
              init: [...this.jsonObject.init],
              rows: [...this.jsonObject.rows]
            }
          });
          //window.console.log(this.algorithms);
          this.savedCirciutName = "";
        } else {
          alert("empty circuit !!");
        }
      } else {
        alert("Please, enter name for the algorithm");
      }
    },
  }
};
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
  margin: 0em 0.5em 0em 5em;
}
.select-algorithm {
  margin: 0em 0.5em 0em 2em;
}

.toolbox2-buttons {
  margin: 1em;
}
</style>
