<template>
  <div class="toolbox-2">
    <div class="run-reset-buttons">
      <button @click="runCircuit">Run</button>
      <button @click="cloneResetSystem">Reset</button>
    </div>

    <tracingButtons class="tracing-buttons"></tracingButtons>

    <div class="elementary-gates">
      <button class="exeBtn" @click="this.$parent.elementaryGates">Elementary Gates</button>
    </div>

    <booleanFunction ref="createBoolean" class="boolean-function" />

    <div class="save-circuit">
      <input type="text" placeholder="Save Circuit by Name" v-model="savedCirciutName" />
      <button @click="saveCircuit(savedCirciutName)">Save Circuit</button>
    </div>
    <div class="select-algorithm">
      <label>Select an Algorithm</label>
      <select v-model="selectedAlgorithm">
        <option
          v-for="(item, index) in algorithms"
          :key="index"
          :value="item.circuit"
        >{{ item.name }}</option>
      </select>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import { mapState, mapActions } from "vuex";
import tracingButtons from "./tracingButtons.vue";
import booleanFunction from "./booleanFunction.vue";

export default {
  name: "Toolbox2",
  display: "Toolbox2",
  components: { tracingButtons, booleanFunction },
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
  mounted() {
    if(localStorage.hasOwnProperty('algorithms')){
        this.getLocal('algorithms')
    }else{ // in case of first run time only 
       this.storeLocal('algorithms');
    }
  },
  computed: {
    ...mapState(["jsonObject"]),
    ...mapState(["algorithms"])
  },
  methods: {
    ...mapActions(["runCircuit"]),
    ...mapActions(["setAlgorithms"]),
    ...mapActions(["isStored"]),
    ...mapActions(["countGate"]),
    ...mapActions(["storeLocal"]),
    ...mapActions(["getLocal"]),
    cloneResetSystem: function() {
      this.selectedAlgorithm = null;
      this.$parent.resetSystem();
    },
    saveCircuit(name) {
      if (name != "") {
        if (this.jsonObject.colsCount) {
          this.algorithms.push({
            name: name,
            circuit: {
              wires: this.jsonObject.wires,
              init: [...this.jsonObject.init],
              rows: [...this.jsonObject.rows],
              controls: this.countGate("●") + this.countGate("○"),
              swaps: this.countGate("swap")
            }
          });
          window.console.log("store")
          window.console.log(this.algorithms);
          this.storeLocal("algorithms");

          this.savedCirciutName = "";
        } else {
          alert("empty circuit !!");
        }
      } else {
        alert("Please, enter name for the algorithm");
      }
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.toolbox-2 {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  flex-wrap: wrap;
  padding: 0px 50px 0px 5px;
  margin: 0px;
}
button {
  display: inline-block;
  margin: 0em 0em 0em 0em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
  border: 2px solid grey;
}
input {
  border-radius: 7px;
}
select {
  border-radius: 7px;
  background: white;
}
.run-reset-buttons {
  flex-basis: 5%;
}
.tracing-buttons {
  flex-basis: 5%;
  margin: 0px 10px 0px 10px;
}
.boolean-function {
  flex-basis: 5%;
  margin: 0px 15px 0px 0px;
}
.elementary-gates {
  flex-basis: 5%;
}
.save-circuit {
  flex-basis: 5%;
  margin: 0px 10px 0px 10px;
}
.select-algorithm {
  flex-basis: 5%;
  margin: 0px 10px 0px 10px;
}
</style>
