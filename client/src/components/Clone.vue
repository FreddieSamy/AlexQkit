<template>
  <div class="clone">
    <label class="app-title">Alexandria Quantum Computer Kit</label>
    <hr />
    <div class="circuit-tools">
      <Toolbox ref="toolbox" />
      <IBM class="ibm" ref="ibm" />
    </div>

    <div class="circuit">
      <Qasm ref="qasm" />
      <tracingLine ref="tracingLine"></tracingLine>
      <CircuitDrawing v-if="this.circuitDrawingFlag" />
      <div v-if="!this.circuitDrawingFlag" class="circuit-wires">
        <div class="wires">
          <wire v-for="row in jsonObject.wires" :key="row" :id="row" :ref="'wire'"></wire>
        </div>
      </div>
    </div>
    <div>
      <Trash></Trash>

      <div class="wires-buttons">
        <Toolbox2 v-if="!this.circuitDrawingFlag" :setAlgorithm="setAlgorithm" />
      </div>
    </div>

    <div class="visual-row">
      <DiracNotation ref="diracNotation" />
    </div>

    <div class="results">
      <MatrixRepresentation class="matrix" ref="matrixRepresentation" />
      <MessageBox class="message-box" />
      <Histogram class="histogram" />
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import axios from "axios";
import Toolbox from "./Toolbox.vue";
import IBM from "./IBM.vue";
import Qasm from "./Qasm.vue";
import CircuitDrawing from "./CircuitDrawing.vue";
import tracingLine from "./tracingLine.vue";
import Wire from "./Wire.vue";
import Trash from "./Trash.vue";
import Toolbox2 from "./Toolbox2.vue";
import DiracNotation from "./DiracNotation.vue";
import MatrixRepresentation from "./MatrixRepresentation.vue";
import MessageBox from "./MessageBox.vue";
import Histogram from "./Histogram.vue";
import { mapGetters, mapState, mapActions } from "vuex";
import { elementaryGates } from "./../data/routes.js";

export default {
  name: "clone",
  display: "clone",
  components: {
    Toolbox,
    IBM,
    CircuitDrawing,
    Wire,
    Trash,
    Toolbox2,
    DiracNotation,
    MessageBox,
    Histogram,
    MatrixRepresentation,
    Qasm,
    tracingLine
  },
  mounted() {
    //this.runCircuit();
  },
  data() {
    return { circuitDrawingFlag: false };
  },
  computed: {
    ...mapState(["jsonObject"]),
    ...mapGetters(["liveResults"])
  },

  methods: {
    ...mapActions(["resetCircuit"]),
    ...mapActions(["setColsCount"]),
    ...mapActions(["setExeCount"]),
    ...mapActions(["runCircuit"]),
    ...mapActions(["checkSwapSystem"]),
    ...mapActions(["removeMessages"]),

    //-----------------------------------------------------------------------
    updateMaxWire: function() {
      window.console.log("updateMaxWire");
      let firstWire = this.$refs.wire[0];
      this.jsonObject.colsCount = firstWire.list.length;

      for (let i = 0; i < this.jsonObject.wires; i++) {
        let wireCaller = this.$refs.wire[i];
        if (wireCaller.list.length > this.jsonObject.colsCount) {
          this.jsonObject.colsCount = wireCaller.list.length;
          this.setColsCount(wireCaller.list.length);
        }
      }
      this.setColsCount(this.jsonObject.colsCount);
      this.setExeCount(this.jsonObject.colsCount);

      this.$refs.tracingLine.updateTracingLine(); //update the tracing line
      //this.removeMessages();
      this.controlSystem();
      this.$nextTick(() => {
        this.removeMessages();
        this.checkSwapSystem();
      });
      //window.console.log("max wire = ", this.jsonObject.colsCount);
      //window.console.log("------------------- ");
    },
    //-----------------------------------------------------------------------
    resetSystem: function() {
      for (let i = 0; i < this.jsonObject.wires; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.resetWire();
      }
      this.resetCircuit();
      this.jsonObject.colsCount = 0;
      this.$refs.tracingLine.updateTracingLine();
      this.removeControlSystem();
      this.runCircuit();
    },
    //-----------------------------------------------------------------------
    addIdentityToColumn: function(wireId) {
      for (let i = 0; i < this.jsonObject.wires; i++) {
        if (i + 1 != wireId) {
          var wireCaller = this.$refs.wire[i];
          wireCaller.addIdentity();
        }
      }
    },
    //-----------------------------------------------------------------------
    removeIdentityColumn: function(columnIndex) {
      for (let row = 0; row < this.jsonObject.wires; row++) {
        var wireCaller = this.$refs.wire[row];
        wireCaller.removeGateByIndex(columnIndex);
      }
      this.updateMaxWire();
      this.jsonObject.exeCount = this.jsonObject.colsCount;
      this.$refs.tracingLine.updateTracingLine();
    },
    //-----------------------------------------------------------------------
    isAllColumnIdentity: function(columnIndex) {
      for (let i = 0; i < this.jsonObject.wires; i++) {
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
      for (let colIdx = this.jsonObject.colsCount - 1; colIdx >= 0; colIdx--) {
        if (this.isAllColumnIdentity(colIdx)) {
          this.removeIdentityColumn(colIdx);
        }
      }
    },
    //-----------------------------------------------------------------------
    setAlgorithm: function(
      algorithmObject,
      append = true
      // qubitNames = undefined
    ) {
      this.jsonObject.wires = Math.max(
        algorithmObject.wires,
        this.jsonObject.wires
      );
      this.jsonObject.init = [
        ...algorithmObject.init,
        ...this.jsonObject.init.slice(algorithmObject.init.length)
      ];
      var row = 0;
      this.$nextTick(() => {
        for (; row < algorithmObject.wires; row++) {
          let wireCaller = this.$refs.wire[row];
          wireCaller.setState(algorithmObject["init"][row]);
          wireCaller.setGates(algorithmObject["rows"][row], append);
          this.$nextTick(() => {
            this.updateMaxWire();
          });
        }
      });
      this.$nextTick(() => {
        this.$nextTick(() => {
          for (; row < this.jsonObject.wires; row++) {
            let wireCaller = this.$refs.wire[row];
            wireCaller.addIdentity();
          }
          this.updateMaxWire();
        });
      });
      // if (qubitNames) {
      //   this.$nextTick(() => {
      //     var variables = qubitNames.names;

      //     var indices = qubitNames.positions;
      //     if (indices == "") {
      //       indices = [...Array(variables.length + 1).keys()];
      //     }
      //     // window.console.log(indices);
      //     window.console.log(
      //       "max length: ",
      //       Math.max(3, ...variables.map(el => el.length))
      //     );
      //     for (let i = 0; i < variables.length; i++) {
      //       this.$refs.wire[parseInt(indices[i])].name = variables[i];
      //       this.$refs.wire[parseInt(indices[indices.length - 1])].name = "out";
      //     }
      //   });
      // }
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
    controlSystem: function() {
      this.removeControlSystem();
      this.$nextTick(() => {
        // wait to render the wire
        for (let i = 0; i < this.jsonObject.colsCount; i++) {
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
        if (colElements[j].id == "●" || colElements[j].id == "○") {
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
    elementaryGates: function() {
      if (this.jsonObject.exeCount) {
        axios.post(elementaryGates, this.jsonObject).then(res => {
          // this.jsonObject.custom = res.data.custom;
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
          if (res.data.rows.length) {
            this.jsonObject.wires = res.data.rows.length;
            this.jsonObject.rows = res.data.rows;
          }

          this.setAlgorithm(this.jsonObject, false);
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
.app-title {
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  font-family: "Times New Roman", Times, serif;
  font-weight: bolder;
  margin: 0px 0px -5px 0px;
}
.circuit-tools {
  display: flex;
  margin: 0.2em;
}
.toolbox {
  flex-basis: 65%;
}
.ibm {
  flex-basis: 30%;
}
.circuit {
  display: inline-flex;
  width: 99%;
  height: 50%;
  margin: 0.2em 0.2em 0.2em 0.2em;
}
.circuit-wires {
  margin: 0em 0.2em 0em 0.2em;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.wires {
  margin: 0em 0.1em 0em 0.1em;
  flex-basis: 100%;
}
.results {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-end;
  align-items: center;
  /* border:1px solid black; */
}
.histogram {
  flex-basis: 100%;
  align-self: center;
  justify-self: center;
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

.matrix {
  flex-basis: 40%;
}
button {
  border: 2px solid grey;
}
</style>
