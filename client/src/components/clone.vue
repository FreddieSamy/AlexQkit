<template>
  <div class="circuit">
    <div class="upper-circuit">
      <toolbox></toolbox>
      <!--ibm></ibm-->
    </div>
    <!-- <trash></trash> -->
    <br />
    <div class="qasmAndWires">
      <div class="qasm" v-if="qasmFlag">
        <textarea>OPENQASM 2.0; include "qelib1.inc";</textarea>
        <button class="qasmBtn">Run</button>
      </div>
      <div class="wiresBlock">
        <div class="wires">
          <wire v-for="row in rows" :key="row" :id="row" :ref="'wire'"></wire>
        </div>
      </div>
    </div>
    <div class="toolbox-2">
      <trash></trash>
      <div class="wires-buttons">
        <button class="add-wire" @click="rows++">Add Wire</button>
        <button class="remove-wire" @click="rows--">Remove Wire</button>
        <button class="add-wire" @click="showSystem">
          show system on console
        </button>
        <button class="add-wire" @click="systemStates">send</button><br />
        <button class="add-wire" @click="resetSystem">reset system</button>
        <button class="add-wire" @click="clearConsole">Clear Console</button>
      </div>
    </div>
    <diracNotation></diracNotation>
    <blochSphere></blochSphere>
    <histoGram></histoGram>
  </div>
</template>
<!-- =============================================================  -->
<script>
import toolbox from "./toolbox.vue";
import wire from "./wire.vue";
/*import ibm from "./ibm.vue";*/
import trash from "./trash.vue";
import axios from "axios";
import blochSphere from "./blochSphere.vue";
import histoGram from "./histoGram.vue";
import diracNotation from "./diracNotation.vue";

export default {
  name: "clone",
  display: "clone",
  components: {
    toolbox,
    /*ibm,*/
    wire,
    trash,
    blochSphere,
    histoGram,
    diracNotation
  },
  data() {
    return {
      route: "http://localhost:5000/data",
      states: ["0", "1", "+", "-", "i", "-i"],
      rows: 2,
      maxWire: 0, // number of wires
      system: {}, // maximum number of gates in a wire
      jsonObject: [
        {
          wire: 0,
          init: [],
          rows: []
        }
      ],
      qasmFlag: false
    };
  },
  methods: {
    showSystem: function() {
      for (let i = 1; i <= this.rows; i++) {
        window.console.log(JSON.stringify(this.system[i]));
      }
    },
    //---------------------------------------------
    updateSystem: function(wireId, wireData) {
      this.system[wireId] = wireData;
      if (this.maxWire < wireData[1].length) {
        this.maxWire = wireData[1].length;
      }
    },
    //---------------------------------------------
    resetSystem: function() {
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.resetWire();
      }
    },
    //---------------------------------------------
    addIdentityToRow: function(wireId) {
      for (let i = 0; i < this.rows; i++) {
        if (i + 1 != wireId) {
          var wireCaller = this.$refs.wire[i];
          wireCaller.addIdentity();
        }
      }
    },
    //---------------------------------------------
    pruneIdentityRow: function() {
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.popLast();
      }
      this.maxWire--;
    },
    //---------------------------------------------
    systemStates: function() {
      var statesSystem = [];
      var gatesSystem = [];
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        statesSystem.push(wireCaller.getState());
        gatesSystem.push(wireCaller.getGates());
      }
      this.jsonObject[0] = {
        wires: this.rows,
        init: statesSystem,
        rows: gatesSystem
      };
      this.sendToServer(this.route, this.jsonObject);
    },
    //---------------------------------------------
    sendToServer: function(route, jsonObject) {
      axios.post(route, jsonObject).then(res => {
        window.console.log("the data success to returned be from the server");
        window.console.log(res);
        
        this.draw();
      });
    },
    //---------------------------------------------
    clearConsole: function() {
      window.console.clear();
    },

    draw: function() {
      var imgOfHistoGram = document.getElementById("chart");
      imgOfHistoGram.src = "http://127.0.0.1:5000/chart.png?time" + new Date();
      var imgofblochSphere = document.getElementById("bloch");
      imgofblochSphere.src =
        "http://127.0.0.1:5000/blochsphere.png?time=" + new Date();
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.upper-circuit {
  /*border: 3px solid black;*/
  display: inline-block;
  margin: 0.2em 0.2em 0.2em 0.2em;
  padding: 0em 0em 0em 0em;
  width: 99%;
}
.wires {
  /*border: 0.1em dashed blue;*/
  margin: 0em 0.1em 0em 0.1em;
  /*display: table-cell;*/
}
.flip-list-move {
  transition: transform 10.9s;
}
.wires-buttons {
  display: inline-block;
  margin: 0.9em 0.2em 0.2em 0.2em;
  padding: 0em 0em 0em 0em;
}
.add-wire {
  display: inline-block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
.remove-wire {
  display: inline-block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
.trashArea {
  color: #ef9494;
  border: 0.1em dashed #ef9494;
  border-radius: 0.2em;
  display: block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  width: 97%;
  text-align: center;
}
.qasm {
  display: block;
  width: 30%;
  margin: 0em 0.2em 0em 0em;
  /*border: 1px solid black;*/
  border-radius: 0.5em;
}
.qasmBtn {
  display: block;
  height: 2em;
  width: 5em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
  right: 0;
  top: 0;
}
.wiresBlock {
  /*display: table-cell;*/
  width: 99%;
  height: 99%;
  margin: 0em 0.2em 0em 0.2em;
}
.qasmAndWires {
  /*border: dashed firebrick;*/
  display: inline-flex;
  width: 99%;
  height: 99%;
  margin: 0.2em 0.2em 3em 0.2em;
}
textarea {
  width: 90%;
  height: 99%;
  bottom: 0;
  /*border: 1px solid black;*/
  border-radius: 0.5em;
  margin: auto;
}
</style>
