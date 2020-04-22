<template>
  <div class="clone">
    <!-------------------------- upper circiut - tools -------------------- -->
    <div class="circuit-tools">
      <toolbox ref="toolbox"></toolbox>
      <ibm class="ibm" ref="ibm"></ibm>
    </div>
    <!-- ------------------------ Circiut --------------------->
    <div class="circuit">
      <qasm ref="qasm"></qasm>
      <tracingLine ref="tracingLine"></tracingLine>
      <circuitDrawing v-if="this.$nextTick(() => {this.$refs.qasm.qasmIncludeIfFlag })"></circuitDrawing>
      <!-- ------------ circiutloops & wires ------------->
      <div v-if="!this.$nextTick(() => {this.$refs.qasm.qasmIncludeIfFlag })" class="circuit-wires">
        <!-- ------------  wires ------------->
        <div class="wires">
          <wire v-for="row in jsonObject.wires" :key="row" :id="row" :ref="'wire'"></wire>
        </div>
      </div>
    </div>
    <div class="toolbox-2">
      <trash></trash>

      <div class="wires-buttons">
        <toolbox2
          v-if="!this.$nextTick(() => {this.$refs.qasm.qasmIncludeIfFlag })"
          class="toolbox2"
          :setAlgorithm="setAlgorithm"
        />
        <button
          v-if="!this.$nextTick(() => {this.$refs.qasm.qasmIncludeIfFlag })"
          class="exeBtn"
          @click="elementaryGates"
        >Elementary Gates</button>
      </div>
    </div>
    <div class="visual-row">
      <diracNotation ref="diracNotation"></diracNotation>
    </div>

    <div class="visual-row">
      <histoGram></histoGram>
      <blochSphere></blochSphere>
    </div>
    <matrixRepresentation ref="matrixRepresentation"></matrixRepresentation>
  </div>
</template>
<!-- =============================================================  -->
<script>
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
import qasm from "./qasm.vue";
import { mapState } from "vuex";

export default {
  name: "clone",
  display: "clone",
  components: {
    toolbox,
    ibm,
    circuitDrawing,
    wire,
    trash,
    toolbox2,
    blochSphere,
    histoGram,
    diracNotation,
    matrixRepresentation,
    qasm,
    tracingLine
  },
  mounted() {
    //window.console.log("clone has been mounted");
    //this.sendSystem();
  },
  data() {
    return {
      route: this.$store.state.routes.appRoute,
      maxWire: 0 // maximum number of gates in a wire
    };
  },
  computed: {
    ...mapState(["jsonObject"])
  },

  methods: {
    //-----------------------------------------------------------------------
    showSystem: function() {
      for (let i = 0; i < this.jsonObject.wires; i++) {
        var wireCaller = this.$refs.wire[i];
        window.console.log(JSON.stringify(wireCaller.list));
      }
    },
    //-----------------------------------------------------------------------
    updateMaxWire: function() {
      let firstWire = this.$refs.wire[0];
      this.maxWire = firstWire.list.length;
      for (let i = 0; i < this.jsonObject.wires; i++) {
        let wireCaller = this.$refs.wire[i];
        if (wireCaller.list.length > this.maxWire) {
          this.maxWire = wireCaller.list.length;
        }
      }
      this.jsonObject.exeCount = this.maxWire;
      this.$refs.tracingLine.updateTracingLine(); //update the trasing line
    },
    //-----------------------------------------------------------------------
    resetSystem: function() {
      for (let i = 0; i < this.jsonObject.wires; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.resetWire();
      }
      this.maxWire = 0;
      this.jsonObject.exeCount = 0;
      this.jsonObject.wires = 2;
      this.$refs.tracingLine.updateTracingLine();
      this.removeControlSystem();
      this.sendSystem();
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
      this.jsonObject.exeCount = this.maxWire;
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
      for (let colIdx = this.maxWire - 1; colIdx >= 0; colIdx--) {
        if (this.isAllColumnIdentity(colIdx)) {
          this.removeIdentityColumn(colIdx);
        }
      }
    },
    //-----------------------------------------------------------------------
    updateSystem: function() {   // should be terminated
      var statesSystem = [];
      var gatesSystem = [];
      for (let i = 0; i < this.jsonObject.wires; i++) {
        var wireCaller = this.$refs.wire[i];
        statesSystem.push(wireCaller.getState());
        gatesSystem.push(wireCaller.getGates(i));
      }
      this.jsonObject.init = statesSystem;
      this.jsonObject.rows = gatesSystem;
      // window.console.log("System Updated");
      // window.console.log(this.jsonObject);
    },
    //-----------------------------------------------------------------------
    sendToServer: function(route, jsonObject) {
      try {
        axios.post(route, jsonObject).then(
          res => {
            this.draw();
            this.$refs.diracNotation.value = res.data.diracNotation;
            this.$refs.matrixRepresentation.value =
              res.data.matrixRepresentation;
            this.$refs.ibm.link = res.data.link;
            this.$refs.qasm.qasmCode = res.data.qasm;
          },
          error => {
            window.console.log(error);
          }
        );
      } catch (error) {
        window.console.log("i think there is an error " + error);
      }

      //window.console.log(this.jsonObject);
    },
    sendSystem: function() {
      this.sendToServer(this.route, this.jsonObject);
    },
    //-----------------------------------------------------------------------
    setAlgorithm: function(systemObject) {
      this.jsonObject.wires = systemObject["wires"];
      this.$nextTick(() => {
        for (let row = 0; row < this.jsonObject.wires; row++) {
          var wireCaller = this.$refs.wire[row];
          wireCaller.setState(systemObject["init"][row]);
          wireCaller.setGates(systemObject["rows"][row]);
        }
        this.updateMaxWire();
      });
    },
    //-----------------------------------------------------------------------
    // setRows: function(rows) {
    //   if (this.rows === rows) {
    //     return true;
    //   }
    //   return false;
    // },
    //-----------------------------------------------------------------------
    draw: function() {
      var imgOfHistoGram = document.getElementById("chart");
      imgOfHistoGram.src = "http://127.0.0.1:5000/chart.png?time" + new Date();

      var imgofblochSphere = document.getElementById("bloch");
      imgofblochSphere.src =
        "http://127.0.0.1:5000/blochsphere.png?time=" + new Date();
      if (this.$refs.qasm.qasmIncludeIfFlag) {
        var imgOfCircuit = document.getElementById("circuitDrawing");
        imgOfCircuit.src =
          "http://127.0.0.1:5000/circuit.png?time=" + new Date();
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
      if (this.jsonObject.exeCount) {
        axios
          .post("http://localhost:5000/elementaryGates", this.jsonObject)
          .then(res => {
            this.jsonObject.custom = res.data.custom;
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

            this.setAlgorithm(this.jsonObject);
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
