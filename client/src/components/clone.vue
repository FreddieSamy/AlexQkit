<template>
  <div class="circuit">
    <div v-if="!qasmFlag" class="upper-circuit">
      <toolbox ref="toolbox"></toolbox>
      <ibm ref="ibm"></ibm>
    </div>
    <br />
    <div class="qasmAndWires">
      <pre class="qasmText" v-if="qasmTextFlag">{{ this.qasmText }}</pre>
      <div class="qasm" v-if="qasmFlag">
        <button class="qasmBtn" @click="qasm">Draggable Circuit</button>
        <textarea id="textarea">OPENQASM 2.0; include "qelib1.inc";</textarea>
        <button class="qasmBtn" @click="sendQasm">Run</button>
      </div>
      <h3 v-if="qasmFlag">{{ qasmError }}</h3>
      <circuitDrawing v-if="qasmFlag && qasmError == ''"></circuitDrawing>
      <img
        v-if="!qasmFlag"
        :style="'height:' + tracingLineHeight + 'em'"
        id="executionLine"
        src="../assets/executionLine.png"
      />
      <div v-if="!qasmFlag" class="wiresBlock">
        <div class="wires">
          <wire v-for="row in rows" :key="row" :id="row" :ref="'wire'"></wire>
        </div>
      </div>
    </div>
    <div class="toolbox-2">
      <trash v-if="!qasmFlag"></trash>
      <div v-if="!qasmFlag" class="wires-buttons">
        <button class="add-wire" @click="rows++, (tracingLineHeight += 5.6)">add Wire</button>
        <button class="remove-wire" @click="rows--, (tracingLineHeight -= 5.6)">Remove Wire</button>
        <button class="add-wire" @click="sendSystem">send</button>
        <button class="reset-system" @click="resetSystem">reset system</button>

        
        <div class="exe">
          <button class="exeBtn" @click="exeStart">start</button>
          <button class="exeBtn" @click="preExe">⟨exe|</button>
          <button class="exeBtn" @click="nextExe">|exe⟩</button>
          <button class="exeBtn" @click="exeEnd">end</button>
        </div>
      
         <button @click="getCols">get coulmns in console</button>
          <button @click="clearConsole">Clear Console</button>
      

        <!--
        <button class="add-wire" @click="teleAlgorithm">
          set teleportation algorithm as a test algorithm
        </button>
        -->
      </div>
    </div>
    <diracNotation></diracNotation>
    <div class="visual-row">
      <histoGram></histoGram>
      <blochSphere></blochSphere>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import toolbox from "./toolbox.vue";
import wire from "./wire.vue";
import ibm from "./ibm.vue";
import trash from "./trash.vue";
import axios from "axios";
import blochSphere from "./blochSphere.vue";
import histoGram from "./histoGram.vue";
import diracNotation from "./diracNotation.vue";
import circuitDrawing from "./circuitDrawing.vue";

export default {
  name: "clone",
  display: "clone",
  components: {
    toolbox,
    ibm,
    wire,
    trash,
    blochSphere,
    histoGram,
    diracNotation,
    circuitDrawing
  },
  data() {
    return {
      API_TOKEN:"",
      qasmError: "",
      tracingLineHeight: 15,
      qasmText: "There is no circuit",
      reversedWires: true,
      diracNotationData: "|000⟩",
      exeCount: 0,
      route: "http://localhost:5000/data",
      states: ["0", "1", "+", "-", "i", "-i"],
      rows: 3, // number of wires
      maxWire: 0, // maximum number of gates in a wire
      qasmFlag: false,
      qasmTextFlag: false,
      jsonObject: [
        {
          API_TOKEN:"",
          wire: 0,
          init: [],
          rows: [],
          reversedWires: true,
          exeCount: 0,
          custom:{}
        }
      ]
    };
  },
  methods: {
    //-----------------------------------------------------------------------
    showSystem: function() {
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        window.console.log(JSON.stringify(wireCaller.list));
      }
    },
    //-----------------------------------------------------------------------
    updateMaxWire: function() {
      let firstWire = this.$refs.wire[0];
      this.maxWire = firstWire.list.length;
      for (let i = 1; i < this.rows; i++) {
        let wireCaller = this.$refs.wire[i];
        if (wireCaller.list.length > this.maxWire) {
          this.maxWire = wireCaller.list.length;
        }
      }
      // window.console.log("max wire = "+this.maxWire);
    },
    //-----------------------------------------------------------------------
    resetSystem: function() {
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.resetWire();
      }
      this.maxWire = 0;
      this.exeCount = 0;
      this.updateTracingLine();
      this.qasmText = "There is no circuit";
    },
    //-----------------------------------------------------------------------
    addIdentityToColumn: function(wireId) {
      for (let i = 0; i < this.rows; i++) {
        if (i + 1 != wireId) {
          var wireCaller = this.$refs.wire[i];
          wireCaller.addIdentity();
        }
      }
    },
    //-----------------------------------------------------------------------
    removeIdentityColumn: function(columnIndex) {
      for (let row = 0; row < this.rows; row++) {
        var wireCaller = this.$refs.wire[row];
        wireCaller.removeGateByIndex(columnIndex);
      }
      this.maxWire--;
    },
    //-----------------------------------------------------------------------
    isAllColumnIdentity: function(columnIndex) {
      for (let i = 0; i < this.rows; i++) {
        var wireList = this.$refs.wire[i].list;
        var gateName = wireList[columnIndex]["name"];
        if (gateName.localeCompare("i") !== 0) {
          //window.console.log("found a gate on column "+columnIndex+" is not identiy gate:"+ gateName);
          return false;
        }
      }
      //window.console.log("all coulmn is "+columnIndex+" identity");
      return true;
    },
    //-----------------------------------------------------------------------
    removeIdentitySystem: function() {
      for (let colIdx = this.maxWire - 1; colIdx >= 0; colIdx--) {
        if (this.isAllColumnIdentity(colIdx)) {
          this.removeIdentityColumn(colIdx);
        }
      }
    },
    //-----------------------------------------------------------------------
    sendSystem: function() {
      var statesSystem = [];
      var gatesSystem = [];
      var toolboxconnect=this.$refs.toolbox;
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        statesSystem.push(wireCaller.getState());
        gatesSystem.push(wireCaller.getGates(i));
      }
      this.jsonObject[0] = {
        API_TOKEN:this.API_TOKEN ,
        reversedWires: this.reversedWires,
        exeCount: this.exeCount,
        wires: this.rows,
        init: statesSystem,
        rows: gatesSystem,
        custom:toolboxconnect.sendtoclone()
      };
      window.console.log(this.jsonObject);
      this.sendToServer(this.route, this.jsonObject);
    },
    //-----------------------------------------------------------------------
    sendToServer: function(route, jsonObject) {
      axios.post(route, jsonObject).then(res => {
        window.console.log("the data success to returned be from the server");
        window.console.log(res);
        this.draw();
        this.diracNotationData = res.data.diracNotation;
        this.qasmError = res.data.qasmError;
        this.qasmText = res.data.qasm;
        window.console.log(res.data.qasmError);
      });
    },
    //-----------------------------------------------------------------------
    teleAlgorithm: function() {
      let test_json_object = {
        wires: 3,
        init: ["0", "0", "0"],
        rows: [
          ["x", "i", "c", "h", "i", "h"],
          ["i", "h", "c", "x", "c", "i"],
          ["i", "i", "x", "i", "h", "c"]
        ]
      };
      window.console.log(test_json_object);
      this.rows = test_json_object["wires"];
      this.setAlgorithm(test_json_object);
    },
    //-----------------------------------------------------------------------
    setAlgorithm: function(systemObject) {
      for (let row = 0; row < this.rows; row++) {
        var wireCaller = this.$refs.wire[row];
        wireCaller.setState(systemObject["init"][row]);
        wireCaller.setGates(systemObject["rows"][row]);
      }
    },
    //-----------------------------------------------------------------------
    setRows: function(rows) {
      if (this.rows === rows) {
        return true;
      }
      return false;
    },
    //-----------------------------------------------------------------------
    clearConsole: function() {
      window.console.clear();
    },
    getCols:function(){
        
       // for(let i = 1 ; i <= this.maxWire ; i++ ){
          var col = document.querySelectorAll('.circuit-gate');
          
          window.console.log(col);
       // }
        
    },
    //-----------------------------------------------------------------------
    draw: function() {
      var imgOfHistoGram = document.getElementById("chart");
      imgOfHistoGram.src = "http://127.0.0.1:5000/chart.png?time" + new Date();

      var imgofblochSphere = document.getElementById("bloch");
      imgofblochSphere.src =
        "http://127.0.0.1:5000/blochsphere.png?time=" + new Date();

      if (this.qasmFlag) {
        var imgOfCircuit = document.getElementById("circuitDrawing");
        imgOfCircuit.src =
          "http://127.0.0.1:5000/circuit.png?time=" + new Date();
      }
    },
    //-----------------------------------------------------------------------
    sendQasm: function() {
      this.qasmError = "";
      this.jsonObject[0] = {
        qasm: document.getElementById("textarea").value
      };
      this.sendToServer(this.route, this.jsonObject);
    },
    //-----------------------------------------------------------------------
    qasmTextFun: function() {
      this.qasmTextFlag = !this.qasmTextFlag;
      this.sendSystem();
    },
    //-----------------------------------------------------------------------
    qasm: function() {
      this.qasmFlag = !this.qasmFlag;
      this.qasmTextFlag = false;
    },
    //-----------------------------------------------------------------------
    nextExe: function() {
      if (this.exeCount < this.maxWire) {
        this.exeCount++;
        this.updateTracingLine();
        this.sendSystem();
      }
    },
    //-----------------------------------------------------------------------
    preExe: function() {
      if (this.exeCount > 0) {
        this.exeCount--;
        this.updateTracingLine();
        this.sendSystem();
      }
    },
    //-----------------------------------------------------------------------
    exeStart: function() {
      if (this.exeCount != 0) {
        this.exeCount = 0;
        this.updateTracingLine();
        this.sendSystem();
      }
    },
    //-----------------------------------------------------------------------
    exeEnd: function() {
      if (this.exeCount != this.maxWire) {
        this.exeCount = this.maxWire;
        this.updateTracingLine();
        this.sendSystem();
      }
    },
    //-----------------------------------------------------------------------
    updateTracingLine: function() {
      document.getElementById("executionLine").style.marginLeft =
        3.8 * this.exeCount + "em";
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.circuit {
  white-space: nowrap;
}
.upper-circuit {
  /*border: 3px solid black;*/
  display: flex;
  margin: 0.2em 0.2em 0.2em 0.2em;
  padding: 0em 0em 0em 0em;
  width: 99%;
  white-space: normal;
}
.wires {
  /*border: 0.1em dashed blue;*/
  margin: 0em 0.1em 0em 0.1em;
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
.exeBtn {
  display: inline-block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
.reset-system {
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

  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
  right: 0;
  top: 0;
}
.wiresBlock {
  width: 99%;
  height: 99%;
  margin: 0em 0.2em 0em 0.2em;
}
.qasmAndWires {
  /*border: dashed firebrick;*/
  display: inline-flex;
  width: 99%;
  height: 50%;
  margin: 0.2em 0.2em 3em 0.2em;
}
.visual-row {
  display: flex;
}
textarea {
  width: 90%;
  height: 99%;
  bottom: 0;
  border-radius: 0.5em;
  margin: auto;
}
.qasmText {
  border: 1px solid black;
  border-radius: 0.5em;
  margin: 0.2em 0.2em 3em 0.2em;
  padding: 0.2em 0.2em 3em 0.2em;
  min-width: 20%;
}
#executionLine {
  width: 10em;
  z-index: -1;
  position: fixed;
  /*height: 15em;*/
  margin-top: 0.9em;
  margin-left: 0em;
}
</style>
