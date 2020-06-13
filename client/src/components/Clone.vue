<template>
  <div class="clone">
    <!-- <label class="app-title">Alexandria Quantum Computer Kit</label>
    <hr />-->
    <div class="circuit-tools">
      <Toolbox ref="toolbox" />
      <IBM class="ibm" ref="ibm" />
    </div>

    <div class="circuit">
      <Qasm ref="qasm" />
      <tracingLine ref="tracingLine"></tracingLine>
      <CircuitDrawing v-if="this.circuitDrawingFlag" />
      <div v-if="!this.circuitDrawingFlag" class="circuit-wires">
        <!--  Wires box -->
        <div class="wires">
          <CircuitBlock
            v-for="block in liveResults.circuitBlocks"
            :key="block.fromColumn"
            :label="block.label"
            :fromColumn="block.fromColumn"
            :toColumn="block.toColumn"
          ></CircuitBlock>
          <!-- Wires -->
          <wire v-for="row in jsonObject.wires" :key="row" :id="row" :ref="'wire'"></wire>
          <!-- end Wires-->
        </div>
        <!-- End Wires Box -->
      </div>
    </div>
    <div class="circuit-tools-2">
      <Trash></Trash>

      <div class="wires-buttons">
        <Toolbox2 class="Toolbox-2" v-if="!this.circuitDrawingFlag" :setAlgorithm="setAlgorithm" />
      </div>
    </div>

 
      <!-- Dirac Notation -->
      <div class="DiracNotation">
        <p class="dirac-label">Dirac Notation :</p>
        <p class="dirac-value">{{this.liveResults.diracNotation}}</p>
      </div>
      <!-- End Dirac Notation -->


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
import MatrixRepresentation from "./MatrixRepresentation.vue";
import MessageBox from "./MessageBox.vue";
import Histogram from "./Histogram.vue";
import { mapGetters, mapState, mapActions } from "vuex";
import { elementaryGates } from "./../data/routes.js";
import CircuitBlock from "./CircuitBlock.vue";

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
    MessageBox,
    Histogram,
    MatrixRepresentation,
    Qasm,
    tracingLine,
    CircuitBlock
  },
  mounted() {
    //this.runCircuit();
  },
  data() {
    return { circuitDrawingFlag: false };
  },

  computed: {
    ...mapState(["jsonObject"]),
    ...mapGetters(["liveResults"]),
    ...mapGetters(["specialGatesCounter"])
  },

  methods: {
    ...mapActions(["resetCircuit"]),
    ...mapActions(["setColsCount"]),
    ...mapActions(["setExeCount"]),
    ...mapActions(["runCircuit"]),
    ...mapActions(["checkSwapSystem"]),
    ...mapActions(["removeMessages"]),
    ...mapActions(["checkWiresCustomGates"]),
    ...mapActions(["setCountControls"]),
    ...mapActions(["setCountSwaps"]),
    ...mapActions(["setCountCustoms"]),
    ...mapActions(["setCountSpecialGates"]),
    ...mapActions(["addWire"]),
    ...mapActions(["removeWire"]),
    //-----------------------------------------------------------------------
    updateMaxWire: function() {
      //window.console.log("updateMaxWire");
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

      // validate circuit

      // apply the control circuit if the circiut contains contorls
      if (this.specialGatesCounter.controls) {
        this.controlSystem();
      } // O(n^3)

      this.$nextTick(() => {
        // really need to optimize the validation
        this.removeMessages(); // O(1)
        if (this.specialGatesCounter.swaps) {
          this.checkSwapSystem();
        }
        
        if (this.specialGatesCounter.customs) {
          this.checkWiresCustomGates();
        }
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
    createWire() {
      this.addWire();
      this.$refs.tracingLine.updateTracingLine();
    },
    deleteWire(index) {
     this.removeWire(index)
      this.$nextTick(()=>{
        this.setAlgorithm({ circuit: this.jsonObject }, false, false);
        this.removeIdentitySystem();
      });
    },
    //-----------------------------------------------------------------------
    addGateColumn: function(wireId, columnId, gateName) {
      //window.console.log("add Identity to Column "+columnId);
      for (let i = 0; i < this.jsonObject.wires; i++) {
        if (i + 1 != wireId) {
          var wireCaller = this.$refs.wire[i];
          wireCaller.addGateByIndex(columnId, gateName);
        }
      }
    },
    //-----------------------------------------------------------------------
    removeIdentityColumn: function(columnIndex) {
      //window.console.log("remove Identity");
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
      // window.console.log("is all column identity");
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
      append = true,
      circuitBlock = true
    ) {
      if (circuitBlock) {
        var fromColumn = this.jsonObject.colsCount; // for circuitBlock
        if (!append) {
          fromColumn = 0;
        }
      }
      
      //this.jsonObject.colsCount +=  algorithmObject.circuit.rows[0];
      this.jsonObject.wires = Math.max(algorithmObject.circuit.wires,this.jsonObject.wires);
      this.jsonObject.init = [
        ...algorithmObject.circuit.init,
        ...this.jsonObject.init.slice(algorithmObject.circuit.init.length)
      ];

      this.$nextTick(() => {
        var row;
        for (row = 0; row < algorithmObject.circuit.wires; row++) {
          let wireCaller = this.$refs.wire[row];
          wireCaller.setState(algorithmObject["circuit"]["init"][row]);
          wireCaller.setGates(algorithmObject["circuit"]["rows"][row], append);
        }
        // in case wires on circuit are more than wires of the algorithm
        for (; row < this.jsonObject.wires; row++) {
          let wireCaller = this.$refs.wire[row];
          wireCaller.addIdentityRow(algorithmObject.circuit.rows[0].length);
        }

        this.updateMaxWire();

        // for circuitBlock
        if (circuitBlock) {
          var toColumn = this.jsonObject.colsCount;
          this.liveResults.circuitBlocks.push({
            label: algorithmObject.name,
            fromColumn: fromColumn,
            toColumn: toColumn
          });
        }
      });
    },
    //-----------------------------------------------------------------------
    controlSystem: function() {
      // O(n^3)
      //window.console.log("controlSystem O(n^3)");
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
      // O(n) can be enhanced
      let flag1 = true;
      let flag2 = true;
      var el1 = null;
      var el2 = null;
      var size = colElements.length;
      for (let i = 0; i < size; i++) {
        if (flag1 || flag2) {
          if (flag1) {
            if (colElements[i].id != "i") {
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
    applyControl: function(el1, el2) {
      // sould be in vuex
      const wires = document.querySelector(".wires");
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
        wires.appendChild(hr);
      }
    },
    //-----------------------------------------------------------------------
    removeControlSystem: function() {
      var clines = document.querySelectorAll(".cline");
      clines.forEach(cline => cline.parentNode.removeChild(cline));
    },
    //-----------------------------------------------------------------------
    elementaryGates: function() {
      if (this.jsonObject.exeCount) {
        axios.post(elementaryGates, this.jsonObject).then(res => {
          // this.jsonObject.custom = res.data.custom;
          var newGates = res.data.custom;
          var custom = this.$refs.toolbox.customGates;
          var flag = true;
          for (let i in newGates) {
            if (custom.length == 0) {
              this.$refs.toolbox.$refs.addcustomgate.addGate(
                newGates[i],
                newGates[i]
              );
            } else {
              for (let j in custom) {
                if (i == this.$refs.toolbox.customGates[j].id) {
                  flag = false;
                  break;
                }
              }
              if (flag) {
                this.$refs.toolbox.$refs.addcustomgate.addGate(
                  newGates[i],
                  newGates[i]
                );
              }
              flag = true;
            }
          }
          if (res.data.rows.length) {
            this.jsonObject.wires = res.data.rows.length;
            this.jsonObject.rows = res.data.rows;
          }
          this.setAlgorithm(
            { name: "Elementary Gates", circuit: this.jsonObject },
            false
          );
        });
      }
    },
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
  position: relative;
  padding: 20px 0px;
  flex-basis: 100%;
  flex-grow: 100%;

  overflow-y: hidden;
  overflow-x: auto;
  white-space: nowrap;
}
.results {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  /* border:1px solid black; */
}
.histogram {
  flex-basis: 100%;
  align-self: center;
  justify-self: center;
  justify-content: center;
}
.flip-list-move {
  transition: transform 10.9s;
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
.DiracNotation {
  border: 2px solid #aaaaaa;
  border-radius: 10px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
  overflow-x:auto;
}
.dirac-label {
  flex-basis: 7%;
  font-weight: bolder;
}
.dirac-value {
  flex-basis: 30%;
  background: lightgray;
  padding: 2px 10px 2px 10px;
}
.DiracNotation p {
  border-radius: 5px;
  margin: 5px;
}
</style>
