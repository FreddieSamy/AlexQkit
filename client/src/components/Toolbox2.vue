<template>
  <div class="toolbox-2">
    <!-- Run and Rest Circuit Buttons -->
    <button class="run-circuit-btn" @click="runCircuit">Run</button>
    <button class="reset-circuit-btn" @click="cloneResetSystem">Reset</button>
    <!-- end  Run and Rest Circuit Buttons -->

    <!-- Tracing Buttons -->
    <button class="exe-btn" @click="exeStart">
      <img src="../assets/icons8-skip-to-start-48.png" alt />
    </button>
    <button class="exe-btn" @click="preExe">
      <img src="../assets/icons8-previous-26.png" alt />
    </button>
    <button class="exe-btn" @click="nextExe">
      <img src="../assets/icons8-next-26.png" alt />
    </button>
    <button class="exe-btn" @click="exeEnd">
      <img src="../assets/icons8-end-48.png" alt />
    </button>
    <!-- end Tracing buttons -->

    <!-- Elementary Gates Button -->
    <button class="elementary-gates" @click="this.$parent.elementaryGates">Elementary Gates</button>
    <!-- end Elementary Gates Button -->

    <!-- Boolean Function Button -->
    <booleanFunction ref="createBoolean" class="boolean-function" />
    <!-- end  Boolean Function Button -->

    <!-- Circuit loops Button -->
    <Circiutloops class="circuit-loops" :colsCount="this.jsonObject.colsCount" />
    <!-- end Circuit loops Button -->

    <!-- Save Circuit Block -->
    <input type="text" placeholder="Save Circuit by Name" v-model="savedCirciutName" />
    <button class="save-circuit-btn" @click="saveCircuit(savedCirciutName)">Save Circuit</button>
    <!-- Save Circuit Block -->

    <!-- Select Algorithm Block -->
    <label>Select an Algorithm</label>
    <select v-model="selectedAlgorithm">
      <option v-for="(item, index) in algorithms" :key="index" :value="item">{{ item.name }}</option>
    </select>
    <!-- end Select Algorithm Block -->
  </div>
</template>
<!-- =============================================================  -->
<script>
import { mapState, mapActions } from "vuex";
import booleanFunction from "./booleanFunction.vue";
import Circiutloops from "./CircuitLoops.vue";

export default {
  name: "Toolbox2",
  display: "Toolbox2",
  components: {
    booleanFunction,
    Circiutloops
  },
  props: ["setAlgorithm"],
  data() {
    return {
      selectedAlgorithm: null, 
      savedCirciutName: ""
    };
  },
  watch: {
    // this watcher watch if you select algorithm from the dropdown list of algorithms
    // and if you choose algorithm it apply it on circuit by-> setAlgotrithm
    selectedAlgorithm() {
      if (this.selectedAlgorithm != null) {
        this.setAlgorithm(this.selectedAlgorithm);
        this.selectedAlgorithm = null;
      }
    }
  },
  mounted() {
    // when mount the componenet check for saved algorithms in local storage
    // of the browser to get it 
    if (localStorage.hasOwnProperty("algorithms")) {
      this.getLocal("algorithms");
    } else {
      // in case of first time to run  on browser or (empty local Storage )
      this.storeLocal("algorithms");
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
      // just reset the system by the function in clone Component
      this.$parent.resetSystem();
    },
    nextExe: function() {
      // Step forward for the Tracing line and run circuit 
      if (this.jsonObject.exeCount < this.jsonObject.colsCount) {
        this.jsonObject.exeCount++;
        this.$parent.$refs.tracingLine.updateTracingLine();
        this.runCircuit();
      }
    },
    //-----------------------------------------------------------------------
    preExe: function() {
      // Step Backward for the Tracing line and run circuit 
      if (this.jsonObject.exeCount > 0) {
        this.jsonObject.exeCount--;
        this.$parent.$refs.tracingLine.updateTracingLine();
        this.runCircuit();
      }
    },
    //-----------------------------------------------------------------------
    // Skip to Start for the Tracing line and run circuit 
    exeStart: function() {
      if (this.jsonObject.exeCount != 0) {
        this.jsonObject.exeCount = 0;
        this.$parent.$refs.tracingLine.updateTracingLine();
        this.runCircuit();
      }
    },
    //-----------------------------------------------------------------------
    // Skip to end for the Tracing line and run circuit 
    exeEnd: function() {
      if (this.jsonObject.exeCount != this.jsonObject.colsCount) {
        this.jsonObject.exeCount = this.jsonObject.colsCount;
        this.$parent.$refs.tracingLine.updateTracingLine();
        this.runCircuit();
      }
    },
    // Save The Circuit applied after counting it's special gates
    // then store it in the local storage  
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
              swaps: this.countGate("Swap")
            }
          });
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
  justify-content: flex-start;
  align-items: center;
  flex-wrap: wrap;
  padding: 0px 50px;
}
button {
  background-color: white;
  border-radius: 0.5em;
  border: 2px solid grey;
  margin:0px 10px;
}
input {
  border-radius: 7px;
}
select {
  border-radius: 7px;
  background: white;
}
img {
  width: 12px;
  height: 10px;
}
.run-circuit-btn{
 margin:0px 0px 0px 10px;
}
.reset-circuit-btn{
  margin:0px 20px 0px 0px;
}
.exe-btn{
  margin:0;
}
.save-circuit-btn{
  margin: 0px 30px 0px 0px;
}
.circuit-loops{
  margin:0px 30px 0px 10px;
}
</style>
