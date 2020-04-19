<template>
  <div class="clone">
    <!-------------------------- upper circiut - tools -------------------- -->
    <div class="circuit-tools">
      <toolbox ref="toolbox"></toolbox>
      <ibm class="ibm" ref="ibm"></ibm>
    </div>
    <!-- ------------------------ Circiut --------------------->
    <div class="circuit">
      <!-- ------------------- qasm ----------------------->
      <div class="editor" v-if="qasmFlag">
        <div class="qasm">
          <prism-editor :lineNumbers="true" :code="qasmCode" v-model="qasmCode" language="js"></prism-editor>
        </div>
        <button class="qasmBtn" @click="sendQasm">Run</button>
      </div>
      <tracingLine ref="tracingLine"></tracingLine>
      <circuitDrawing v-if="qasmIncludeIfFlag "></circuitDrawing>
      <!-- ------------ circiutloops & wires ------------->
      <div v-if="!qasmIncludeIfFlag" class="circuit-wires">
        <!-- ------------  wires ------------->
        <div class="wires">
          <wire v-for="row in rows" :key="row" :id="row" :ref="'wire'"></wire>
        </div>
      </div>
    </div>
    <div class="toolbox-2">
      <trash></trash>

      <div class="wires-buttons">
        <toolbox2
          v-if="!qasmIncludeIfFlag"
          class="toolbox2"
          :eventQueue="eventQueue"
          :setAlgorithm="setAlgorithm"
        />
        <!-- <div v-if="!qasmIncludeIfFlag" class="exe">
          <button class="exeBtn" @click="exeStart">start</button>
          <button class="exeBtn" @click="preExe">⟨exe|</button>
          <button class="exeBtn" @click="nextExe">|exe⟩</button>
          <button class="exeBtn" @click="exeEnd">end</button>
        </div>-->
        <button v-if="!qasmIncludeIfFlag" class="exeBtn" @click="elementaryGates">Elementary Gates</button>
      </div>
    </div>
    <div class="visual-row">
      <diracNotation></diracNotation>
    </div>
    <matrixRepresentation></matrixRepresentation>
    <div class="visual-row">
      <histoGram></histoGram>
      <blochSphere></blochSphere>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import "prismjs";
import "prismjs/themes/prism.css";
import "vue-prism-editor/dist/VuePrismEditor.css";
import PrismEditor from "vue-prism-editor";
import toolbox from "./toolbox.vue";
import toolbox2 from "./toolbox2.vue";
import wire from "./wire.vue";
import ibm from "./ibm.vue";
import trash from "./trash.vue";
import axios from "axios";
import blochSphere from "./blochSphere.vue";
import histoGram from "./histoGram.vue";
import diracNotation from "./diracNotation.vue";
import circuitDrawing from "./circuitDrawing.vue";
import matrixRepresentation from "./matrixRepresentation.vue";
import tracingLine from "./tracingLine.vue";
// import { mapState } from 'vuex';

export default {
  name: "clone",
  display: "clone",
  components: {
    toolbox,
    ibm,
    PrismEditor,
    circuitDrawing,
    wire,
    trash,
    toolbox2,
    blochSphere,
    histoGram,
    diracNotation,
    matrixRepresentation,
    tracingLine
  },
  mounted() {
    //window.console.log("clone has been mounted");
    this.sendSystem();
    window.console.log();
  },
  updated() {
    //window.console.log("clone has been updated");
    this.controlSystem();
  },
  data() {
    return {
      qasmCode: "",
      API_TOKEN: "",
      diracNotationData: "|00⟩",
      exeCount: 0,
      route: this.$store.state.routes.appRoute,
      rows: 2, // number of wires
      maxWire: 0, // maximum number of gates in a wire
      qasmFlag: false,
      qasmIncludeIfFlag: false,
      matrixRepresentation: [],
      jsonObject: {
        API_TOKEN: "",
        wires: 0,
        init: [],
        rows: [],
        exeCount: 0,
        custom: {},
        shots: 1024,
        device: "",
        repeated: {}
      },
      eventQueue: []
    };
  },
  watch: {
    jsonObject: {
      immediate: true,
      handler() {
        this.eventQueue.push(this.jsonObject);
      }
    }
  },
  computed: {
    // ...mapState['jsonObject']
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
      for (let i = 0; i < this.rows; i++) {
        let wireCaller = this.$refs.wire[i];
        if (wireCaller.list.length > this.maxWire) {
          this.maxWire = wireCaller.list.length;
        }
      }

      this.exeCount = this.maxWire;
      this.$refs.tracingLine.updateTracingLine(); //update the trasing line
    },
    //-----------------------------------------------------------------------
    resetSystem: function() {
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.resetWire();
      }
      this.maxWire = 0;
      this.exeCount = 0;
      this.rows = 2;
      this.$refs.tracingLine.updateTracingLine();
      this.removeControlSystem();
      this.sendSystem();
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
      this.updateMaxWire();
      this.exeCount = this.maxWire;
      this.$refs.tracingLine.updateTracingLine();
    },
    //-----------------------------------------------------------------------
    isAllColumnIdentity: function(columnIndex) {
      for (let i = 0; i < this.rows; i++) {
        var wireList = this.$refs.wire[i].list;
        var gateName = wireList[columnIndex]["name"];
        if (gateName.localeCompare("i") !== 0) {
          return false;
        }
      }
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
    updateSystem: function() {
      var statesSystem = [];
      var gatesSystem = [];
      var toolboxconnect = this.$refs.toolbox;
      var ibmcon = this.$refs.ibm;
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        statesSystem.push(wireCaller.getState());
        gatesSystem.push(wireCaller.getGates(i));
      }
      this.jsonObject = {
        exeCount: this.exeCount,
        wires: this.rows,
        init: statesSystem,
        rows: gatesSystem,
        custom: toolboxconnect.sendtoclone(),
        shots: parseInt(ibmcon.returnshots())
      };
      if (document.getElementById("checkbox").checked) {
        this.jsonObject["API_TOKEN"] = this.API_TOKEN;
        this.jsonObject["device"] = this.device;
      }
      if (document.getElementById("degree").checked) {
        this.jsonObject["radian"] = false;
      }
      document.getElementById("checkbox").checked = false;
    },
    //-----------------------------------------------------------------------
    sendToServer: function(route, jsonObject) {
      axios.post(route, jsonObject).then(res => {
        this.draw();
        this.diracNotationData = res.data.diracNotation;
        this.matrixRepresentation = res.data.matrixRepresentation;
        this.$refs.ibm.link = res.data.link;
        this.qasmCode = res.data.qasm;
      });
    },
    sendSystem: function() {
      this.updateSystem();
      this.sendToServer(this.route, this.jsonObject);
    },
    //-----------------------------------------------------------------------

    //-----------------------------------------------------------------------
    setAlgorithm: function(systemObject) {
      this.rows = systemObject["wires"];
      this.$nextTick(() => {
        for (let row = 0; row < this.rows; row++) {
          var wireCaller = this.$refs.wire[row];
          wireCaller.setState(systemObject["init"][row]);
          wireCaller.setGates(systemObject["rows"][row]);
        }
        this.updateMaxWire();
      });
    },
    //-----------------------------------------------------------------------
    setRows: function(rows) {
      if (this.rows === rows) {
        return true;
      }
      return false;
    },
    //-----------------------------------------------------------------------
    draw: function() {
      var imgOfHistoGram = document.getElementById("chart");
      imgOfHistoGram.src = "http://127.0.0.1:5000/chart.png?time" + new Date();

      var imgofblochSphere = document.getElementById("bloch");
      imgofblochSphere.src =
        "http://127.0.0.1:5000/blochsphere.png?time=" + new Date();
      if (this.qasmIncludeIfFlag) {
        var imgOfCircuit = document.getElementById("circuitDrawing");
        imgOfCircuit.src =
          "http://127.0.0.1:5000/circuit.png?time=" + new Date();
      }
    },
    //-----------------------------------------------------------------------
    sendQasm: function() {
      // window.console.log(this.qasmCode);
      let jsonObject = {
        qasm: this.qasmCode
      };
      axios.post(this.route, jsonObject).then(res => {
        if (res.data.qasmError == "") {
          this.draw();
          this.diracNotationData = res.data.diracNotation;
          this.matrixRepresentation = res.data.matrixRepresentation;
          this.$refs.ibm.link = res.data.link;
          if (this.qasmFlag) {
            this.qasmCode = res.data.qasm;
            this.qasmIncludeIfFlag = this.qasmCode.includes("if");
          }

          if (res.data.qasmRows && !this.qasmIncludeIfFlag) {
            // undefined qasmRows leads to an error
            let circuit = {
              wires: res.data.qasmRows.length,
              init: Array(res.data.qasmRows.length).fill("0"),
              rows: res.data.qasmRows
            };
            this.setAlgorithm(circuit);
          }
        } else {
          alert("qasm code error :\n" + res.data.qasmError);
        }
      });
    },

    //-----------------------------------------------------------------------
    qasm: function() {
      this.qasmFlag = !this.qasmFlag;
      this.$refs.tracingLine.updateTracingLine();
      // this.sendSystem();
      if (this.qasmFlag) {
        document.getElementById("qasmToolboxBtn").innerHTML = "⟨ qasm |";
      } else {
        document.getElementById("qasmToolboxBtn").innerHTML = "| qasm ⟩";
      }
    },
    //-----------------------------------------------------------------------
    applyControl: function(el1, el2) {
      if (el1 != null && el2 != null) {
        let x = el1.offsetLeft + el1.offsetWidth / 2;
        let y1 = el1.offsetTop + el1.offsetHeight / 2;
        let y2 = el2.offsetTop + el1.offsetHeight / 2;
        let size = Math.abs(y2 - y1);
        var hr = document.createElement("hr");
        hr.setAttribute("class", "cline");
        hr.setAttribute("width", "2");
        hr.setAttribute("size", size);
        hr.style.left = 0;
        hr.style.top = 0;
        hr.style.margin = "" + y1 + "px 0px 0px " + (x - 2) + "px";
        var parent = this.$el;
        parent.appendChild(hr);
      }
    },
    //-----------------------------------------------------------------------
    removeControl: function() {
      var cline = document.querySelector(".cline");
      if (cline != null) {
        var parent = this.$el;
        parent.removeChild(cline);
        return true;
      }
      return false; // already cline = null (there is no control)
    },
    //-----------------------------------------------------------------------
    removeControlSystem: function() {
      var flag = true;
      while (flag) {
        flag = this.removeControl();
      }
    },
    //-----------------------------------------------------------------------
    controlSystem: function() {
      this.removeControlSystem();
      this.$nextTick(() => {
        // wait to render the wire
        for (let i = 0; i < this.maxWire; i++) {
          this.$nextTick(() => {
            // wait to render the added gate
            this.$nextTick(() => {
              // wait to render the identity
              let colElements = document.querySelectorAll(
                "[col=_" + (i + 1) + "]"
              );
              if (this.isControl(colElements)) {
                this.controlColumn(colElements);
              }
            }); // all identity has been rendered
          }); // added gate has been rendered
        } // end for loop
      }); // wire has been rendered
    },
    //-----------------------------------------------------------------------
    isControl: function(colElements) {
      for (let j = 0; j < colElements.length; j++) {
        if (colElements[j].id == "c" || colElements[j].id == "oc") {
          return true;
        }
      }
      return false;
    },
    //-----------------------------------------------------------------------
    controlColumn: function(colElements) {
      let flag1 = true;
      let flag2 = true;
      var el1 = null;
      var el2 = null;
      var size = colElements.length;
      for (let i = 0; i < size; i++) {
        if (flag1 || flag2) {
          if (flag1) {
            if (colElements[i].id != "i") {
              // found first element (upper)
              el1 = colElements[i];
              flag1 = false; // no need to search from top again
            }
          }
          if (flag2) {
            if (colElements[size - i - 1].id != "i") {
              // found second element (lower)
              el2 = colElements[size - i - 1];
              flag2 = false; // no need to search from bottom again
            }
          }
        }
      }
      if (el1 !== el2) {
        // if there is not only one c gate in the column
        this.applyControl(el1, el2);
      }
    },
    //-----------------------------------------------------------------------
    elementaryGates: function() {
      var statesSystem = [];
      var gatesSystem = [];
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        statesSystem.push(wireCaller.getState());
        gatesSystem.push(wireCaller.getGates(i));
      }
      var jsonObject = {
        rows: gatesSystem,
        custom: this.$refs.toolbox.customsrever
      };
      if (this.exeCount) {
        axios
          .post("http://localhost:5000/elementaryGates", jsonObject)
          .then(res => {
            this.$refs.toolbox.customsrever = res.data.custom;
            var dic = res.data.custom;
            var custom = this.$refs.toolbox.customGates;
            var flag = true;
            for (let i in dic) {
              if (custom.length == 0) {
                this.$refs.toolbox.$refs.addcustomgate.addGate(i, i);
              } else {
                for (let j in custom) {
                  if (i == this.$refs.toolbox.customGates[j].id) {
                    flag = false;
                    break;
                  }
                }
                if (flag) {
                  this.$refs.toolbox.$refs.addcustomgate.addGate(i, i);
                }
                flag = true;
              }
            }
            let json_object = {
              wires: res.data.rows.length,
              init: statesSystem,
              rows: res.data.rows
            };
            this.setAlgorithm(json_object);
          });
      }
    }
    //-----------------------------------------------------------------------
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.clone {
  white-space: nowrap;
}
.circuit-tools {
  display: flex;
  margin: 0.2em;
}
.toolbox {
  flex-basis: 65%;
}
.ibm {
  flex-basis: 35%;
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
.exeBtn {
  display: inline-block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
.qasm {
  overflow-y: auto;
  width: 18em;
  max-height: 20em;
  margin: 0em 0.2em 0em 0em;
  border-radius: 0.5em;
}
.editor {
  display: block;
  height: 100%;
  width: 18em;
}
.qasmBtn {
  margin: 0.2em 0.2em 0.2em 0em;
  display: block;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
  right: 0;
  top: 0;
}
.circuit-wires {
  width: 99%;
  height: 99%;
  margin: 0em 0.2em 0em 0.2em;
}
.circuit {
  /*border: dashed firebrick;*/
  display: inline-flex;
  width: 99%;
  height: 50%;
  margin: 0.2em 0.2em 0.2em 0.2em;
}
.visual-row {
  display: flex;
}
</style>
