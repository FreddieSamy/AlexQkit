<template>
  <div class="toolbox">
    <div class="tools-container">
      <div class="box-labels">
        <div class="tool-box-label">
          <label>Toolbox</label>
        </div>
        <div class="custom-gate-label">
          <label v-if="customGates.length">Custom Gates</label>
        </div>
      </div>
      <!--end box-labels-->

      <div class="toolbox-of-gates">
        <!-- ---------------------- gates 1 -------------------------- -->
        <draggable
          class="Area1"
          :list="gates1"
          :group="{ name: 'gates', pull: 'clone', put: false }"
          :clone="cloneGate"
          @change="log"
        >
          <transition-group type="transition" name="flip-list">
            <div
              class="toolbox-gates"
              v-for="element in gates1"
              :key="element.id"
              :id="element.name"
            >
              <div class="gate-name" id="hover-div">
                {{ element.name }}
                <span id="hover-element">{{ element.info }}</span>
              </div>
            </div>
          </transition-group>
        </draggable>

        <!-- ---------------------- gates 2 -------------------------- -->

        <draggable
          class="Area2"
          :list="gates2"
          :group="{ name: 'gates', pull: 'clone', put: false }"
          :clone="cloneGate"
          @change="log"
        >
          <transition-group type="transition" name="flip-list">
            <div
              class="toolbox-gates"
              v-for="element in gates2"
              :key="element.id"
              :id="element.name"
            >
              <div class="gate-name" id="hover-div">
                {{ element.name }}
                <span id="hover-element">{{ element.info }}</span>
              </div>
            </div>
          </transition-group>
        </draggable>
        <!-- ---------------------- gates 3 -------------------------- -->
        <div class="angle-gates">
          <draggable
            :list="gates3"
            :group="{ name: 'gates', pull: 'clone', put: false }"
            :clone="cloneGate"
            @change="log"
          >
            <transition-group type="transition" name="flip-list">
              <div
                class="toolbox-gates"
                v-for="element in gates3"
                :key="element.id"
                :id="element.name"
              >
                <div class="gate-name" id="hover-div">
                  {{ element.name }}
                  <span id="hover-element">{{ element.info }}</span>
                </div>
              </div>
            </transition-group>
          </draggable>
          <input class="angle" id="rxAngle" type="number" name="rx" value="90" />
          <input class="angle" id="ryAngle" type="number" name="ry" value="90" />
          <input class="angle" id="rzAngle" type="number" name="rz" value="90" />

          <input type="radio" id="degree" name="angleType" value="degree" checked />
          <label for="degree" style="font-size: 15px;">degree</label>
          <input type="radio" id="radian" name="angleType" value="radian" />
          <label for="radian" style="font-size: 15px;">radian</label>
        </div>
        <!-- ---------------------- gates 4 -------------------------- -->
        <draggable
          class="Area1"
          :list="gates4"
          :group="{ name: 'gates', pull: 'clone', put: false }"
          :clone="cloneGate"
          @change="log"
        >
          <transition-group type="transition" name="flip-list">
            <div
              class="toolbox-gates"
              v-for="element in gates4"
              :key="element.id"
              :id="element.name"
            >
              <div class="gate-name" id="hover-div">
                {{ element.name }}
                <span id="hover-element">{{ element.info }}</span>
              </div>
            </div>
          </transition-group>
        </draggable>
      </div>
      <draggable
        v-if="customGates.length"
        class="custom-gates"
        :list="customGates"
        :group="{ name: 'gates', pull: 'clone', put: false }"
        :clone="cloneGate"
        @change="log"
        :style="w"
      >
        <transition-group type="transition" name="flip-list">
          <div
            class="toolbox-gates"
            v-for="element in customGates"
            :key="element.id"
            :id="element.name"
          >
            <div class="gate-name">{{ element.id }}</div>
          </div>
        </transition-group>
      </draggable>
    </div>
    <!-- end tools-container -->
    <div>
      <label class="lbl1">Number Of Shots</label>
      <input class="ibmToken" type="number" placeholder="1024" id="numberofshots" />
    </div>
    <div class="user-tools">
      <button id="qasmToolboxBtn" class="qasm" @click="this.$parent.qasm">| qasm ⟩</button>
      <div id="myNav" class="overlay">
        <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>
        <div class="column1">
          <h1 class="p" style="color: black ">from matrix</h1>
          <h3 style="color: black">name</h3>
          <input type="text" id="nameofgate" />
          <h3 style="color: black">number of wires</h3>
          <matrixcu ref="matrixcu"></matrixcu>
          <br />
          <button
            @click="create_the_matrix()"
            style="background: none;color: white; border: 1px solid white; font-size: 20px; margin-top: 10px;"
          >create</button>
        </div>
        <div class="column2">
          <h1 style="color: black;">from rotation</h1>
          <h3 style="color: black;">select the gate</h3>
        </div>
        <div class="column3">
          <h1 style="color: black;">from circuit</h1>
          <h3 style="color: black;">Name</h3>
          <input type="text" id="subCircuitName" />
          <h3 style="color: black;">Rows</h3>
          <label style="color: black;">From</label>
          <select id="fromRow" style="width:15%;">
            <option v-for="i in this.$parent.rows" :key="i" :value="i">{{i}}</option>
          </select>
          <label style="color: black;">To</label>
          <select id="toRow" style="width:15%;">
            <option v-for="i in this.$parent.rows" :key="i" :value="i">{{i}}</option>
          </select>
          <h3 style="color: black;">Columns</h3>
          <label style="color: black;">From</label>
          <select id="fromColumn" style="width:15%;">
            <option v-for="i in this.$parent.maxWire" :key="i" :value="i">{{i}}</option>
          </select>
          <label style="color: black;">To</label>
          <select id="toColumn" style="width:15%;">
            <option v-for="i in this.$parent.maxWire" :key="i" :value="i">{{i}}</option>
          </select>
          <br />
          <button
            @click="subCircuitCustoGate()"
            style="background: none;color: white; border: 1px solid white; font-size: 20px; margin-top: 2em;"
          >create</button>
        </div>
        <div class="column4">
          <h1 style="color: black;">nth root</h1>
          <h3 style="color: black">select the gate</h3>
          <select id="rootGate" style="width:40%;">
            <optgroup label="Gates">
              <option
                v-for="index in gates2.length - 1"
                :key="index"
                :value="gates2[index - 1].name"
              >{{ gates2[index - 1].name }}</option>
              <option
                v-for="element in gates4"
                :key="element.id"
                :value="element.name"
              >{{ element.name }}</option>
            </optgroup>
            <optgroup v-if="customGates.length" label="Custom Gates">
              <option
                v-for="element in customGates"
                :key="element.id"
                :value="element.id"
              >{{ element.id }}</option>
            </optgroup>
          </select>
          <h3 style="color: black;">root</h3>
          <input style="width:40%;" id="root" type="number" value="2" />
          <button
            @click="nthRoot()"
            style="background: none;color: white; border: 1px solid white; font-size: 20px; margin-top: 2em;"
          >create</button>
        </div>

        <div class="addGateError">
          <label id="errormsg"></label>
        </div>
      </div>
      <button class="addGate" @click="openNav()">Add Custom Gate</button>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
import axios from "axios";
import matrixcu from "./matrixcu.vue";
export default {
  name: "toolbox",
  display: "toolbox",
  components: {
    draggable,
    matrixcu
  },
  data() {
    return {
      gates1: [
        { name: "c", id: "c", index: "", info: "closed control" },
        { name: "m", id: "m", index: "", info: "measurment gate" },
        { name: "oc", id: "oc", index: "", info: "open control" },
        { name: "reset", id: "reset", index: "", info: "reset gate" }
      ],
      gates2: [
        { name: "x", id: "x", index: "", info: "not gate" },
        { name: "y", id: "y", index: "", info: "" },
        { name: "z", id: "z", index: "", info: "" },
        { name: "h", id: "h", index: "", info: "simple super postition" },
        { name: "swap", id: "swap", index: "", info: "" }
      ],
      gates3: [
        { name: "rx", id: "rx", index: "", info: "" },
        { name: "ry", id: "ry", index: "", info: "" },
        { name: "rz", id: "rz", index: "", info: "" }
      ],
      gates4: [
        { name: "s", id: "s", index: "", info: "" },
        { name: "t", id: "t", index: "", info: "" },
        { name: "sdg", id: "sdg", index: "", info: "" },
        { name: "tdg", id: "tdg", index: "", info: "" }
      ],
      customGates: [],
      w: "width:7.7em",
      customsrever: {}
      // jsonobjectall: {
      //   [this.nameofgate]: this.matrix
      // }
    };
  },
  methods: {
    log: function() {
      this.$parent.qasmIncludeIfFlag = false;
      //this.$parent.maxWire = 0;
    },
    // ----------------------------------------------------
    cloneGate({ name }) {
      if (name == "rx") {
        name = name + "(" + document.getElementById("rxAngle").value + ")";
      } else if (name == "ry") {
        name = name + "(" + document.getElementById("ryAngle").value + ")";
      } else if (name == "rz") {
        name = name + "(" + document.getElementById("rzAngle").value + ")";
      }
      return {
        name: name
      };
    },
    // ----------------------------------------------------
    addGate(nameofgate) {
      this.customGates.push({
        name: "custom_" + nameofgate,
        id: nameofgate
      });
      if (this.customGates.length < 9) {
        this.w =
          "width:" + Math.ceil(this.customGates.length / 2) * 3.85 + "em";
      } else {
        this.w = "width:15.9em";
      }
    },
    // ----------------------------------------------------
    openNav() {
      document.getElementById("myNav").style.width = "100%";
      document.getElementById("subCircuitName").value = null;
      document.getElementById("nameofgate").value = null;
    },
    // ----------------------------------------------------
    closeNav() {
      document.getElementById("myNav").style.width = "0%";
      document.getElementById("errormsg").innerHTML = null;
      document.getElementById("wires").value = null;

      var conmatrixcu2 = this.$refs.matrixcu;
      conmatrixcu2.clear();
    },
    // ----------------------------------------------------
    create_the_matrix() {
      var nameofgate = document.getElementById("nameofgate").value;
      //var valofgate = document.getElementById("valueofgate");
      var conmatrixcu = this.$refs.matrixcu;
      var matrix = conmatrixcu.pulldata();
      var { matrix_validate, msg } = this.validate_of_matrix(
        matrix,
        nameofgate
      );
      window.console.log(matrix_validate);
      window.console.log(msg);
      var isUnitary;
      var jsonObject = {};
      jsonObject["matrix"] = matrix;
      window.console.log(matrix_validate);
      // window.console.log(msg);

      if (matrix_validate) {
        axios.post("http://localhost:5000/isUnitary", jsonObject).then(res => {
          window.console.log("the data success to returned be from the server");
          isUnitary = res.data.isUnitary;
          //isUnitary; //to hassan.. it's a boolean data which represent if the matrix is unitary or not
          window.console.log("new unitary:" + isUnitary);
          if (isUnitary) {
            this.addGate(nameofgate);
            this.customsrever[nameofgate] = matrix;
            // window.console.log(this.customsrever);
            document.getElementById("errormsg").innerHTML = null;
            this.closeNav();
          }
        });
      } else {
        document.getElementById("errormsg").innerHTML = "*" + msg + "*";
      }
      // document.getElementById("nameofgate").value = null;
      // conmatrixcu.clear();
      //document.getElementById("valueofgate").value = null;
      //window.console.log("unitary:" + this.$parent.isUnitary);
    },
    // ----------------------------------------------------
    //
    // ----------------------------------------------------
    validate_of_matrix(matrix, nameofgate) {
      var matrix_validate = true;
      var msg = "please check the dimenons of the matrix";
      var count1, count2, check;
      var regex = /^(-)?\d+$|^(-)?i$|^(-)?\d+(-|\+)(\d+)?i$|^(-)?\d+i$|^(-)?(\d+)?i(-|\+)\d$/;

      for (let i in this.customGates) {
        for (let k in this.customGates[i]) {
          if (this.customGates[i][k] === nameofgate) {
            matrix_validate = false;
            msg = "this name is already exist,please choose different name";
            return { matrix_validate, msg };
          }
        }
      }

      if (nameofgate == "" || nameofgate.length == 0) {
        matrix_validate = false;
        msg = "you have to write name for the gate";
        return { matrix_validate, msg };
      }
      if (nameofgate.includes(".")) {
        matrix_validate = false;
        msg = "name of gate can't include '.'";
        return { matrix_validate, msg };
      }

      for (count1 in matrix) {
        for (count2 in matrix[count1]) {
          check = regex.test(matrix[count1][count2]);
          if (!check) {
            matrix_validate = false;
            msg = "please check value of every element in matrix ";
            return { matrix_validate, msg };
          }
        }
      }
      msg = "";
      return { matrix_validate, msg };
    },

    // ----------------------------------------------------
    sendtoclone() {
      return this.customsrever;
    },
    // ----------------------------------------------------
    nthRoot: function() {
      var name = document.getElementById("rootGate").value;
      /*window.console.log(name);*/
      var root = document.getElementById("root").value;
      if (name + "^(1/" + root + ")" in this.customsrever) {
        document.getElementById("errormsg").innerHTML =
          "*sorry, " + name + "^(1/" + root + ")" + " is already exist*";
      } else {
        var jsonObject = {
          root: root,
          gate: name,
          custom: this.customsrever
        };
        if (root >= 2) {
          axios.post("http://localhost:5000/nthRoot", jsonObject).then(res => {
            /*window.console.log(res.data);*/
            if (res.data.isUnitary) {
              this.addGate(name + "^(1/" + root + ")");
              this.customsrever[name + "^(1/" + root + ")"] = res.data.matrix;
              document.getElementById("errormsg").innerHTML = null;
              this.closeNav();
            } else {
              document.getElementById("errormsg").innerHTML =
                "*sorry, " + name + "^(1/" + root + ")" + " isn't unitary*";
            }
          });
        } else {
          document.getElementById("errormsg").innerHTML =
            "*please, choose number more than one !!*";
        }
      }
    },
    // ----------------------------------------------------
    subCircuitCustoGate: function() {
      var name = document.getElementById("subCircuitName").value;
      var flag = true;
      var fromRow = document.getElementById("fromRow").value;
      var toRow = document.getElementById("toRow").value;
      var fromColumn = document.getElementById("fromColumn").value;
      var toColumn = document.getElementById("toColumn").value;
      if (fromRow && toRow && fromColumn && toColumn) {
        if (fromRow <= toRow && fromColumn <= toColumn) {
          if (name == "" || name.length == 0) {
            document.getElementById("errormsg").innerHTML =
              "*please, enter a name for the gate*";
          } else {
            for (let i in this.customGates) {
              for (let k in this.customGates[i]) {
                if (this.customGates[i][k] === name) {
                  flag = false;
                  document.getElementById("errormsg").innerHTML =
                    "*this name is already exist*";
                }
              }
            }
            if (flag) {
              this.$parent.cloneSubCircuitCustoGate(
                fromRow,
                toRow,
                fromColumn,
                toColumn
              );
            }
          }
        } else {
          document.getElementById("errormsg").innerHTML =
            "*please, check the selected numbers*";
        }
      }
    }
    // ----------------------------------------------------
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.toolbox {
  display: block;
}
.tools-container {
  display: inline-block;
}
.tool-box-label {
  display: inline-block;
  margin-right: 0.4em;
}
.custom-gate-label {
  display: inline-block;
  margin: 0em 0em 0em 37em;
}
.toolbox-gates {
  display: inline-block;
  margin: 0.3em 0.7em 0.3em 0.5em;
  width: 2.5em;
  height: 2.5em;
  border-radius: 0.3em;
  background-color: #979a9a;
}
.gate-name {
  text-align: center;
  margin: 0.7em 0.5em 0.5em 0.5em;
  color: black;
}
.toolbox-of-gates {
  display: inline-block;
  margin-right: 0.4em;
  height: 7.4em;
  overflow: auto;
}
.Area1 {
  border: 1px solid black;
  border-radius: 0.5em;
  margin: 0.1em 0.1em 0.1em 0.1em;
  display: inline-block;
  height: 6.6em;
  width: 7.7em;
}
.Area2 {
  border: 1px solid black;
  border-radius: 0.5em;
  margin: 0.1em 0.1em 0.1em 0.1em;
  display: inline-block;
  /* white-space: pre-wrap; */
  height: 6.6em;
  width: 11.6em;
}
.angle-gates {
  border: 1px solid black;
  border-radius: 0.5em;
  margin: 0.1em 0.1em 0.1em 0.1em;
  display: inline-block;
  /* white-space: pre-wrap; */
  height: 6.6em;
  width: 11.6em;
}
.custom-gates {
  border: 1px solid black;
  display: inline-block;
  height: 7.4em;
  overflow: auto;
  border-radius: 0.3em;
  min-width: 7.7em;
}

.flip-list-move {
  transition: transform 0.3s;
}
.user-tools {
  display: block;
}

.shots {
  display: inline-block;
  margin: 0em 1em 0em 1em;
}
.angle {
  margin: 0em 0.7em 0.1em 0.5em;
  width: 3em;
  height: 1em;
}
/*
#c {
  background-color: red;
}
*/
.addGate {
  margin: 0em 0em 0em 0.2em;
  background-color: white;
  border-radius: 0.5em;
}
.qasm {
  margin: 0em 0em 0em 0.2em;
  background-color: white;
  border-radius: 0.5em;
}
.overlay {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: rgba(11, 12, 16, 0.8);
  overflow-x: hidden;
  transition: 0.5s;
}

.overlay-content {
  position: relative;
  top: 25%;
  width: 100%;
  text-align: center;
  margin-top: 30px;
  font-family: "Lato", sans-serif;
}

.overlay a {
  padding: 8px;
  text-decoration: none;
  font-size: 36px;
  color: rgba(255, 255, 255, 0.7);
  display: block;
  transition: 0.3s;
}

.overlay a:hover,
.overlay a:focus {
  color: #f1f1f1;
}

.overlay .closebtn {
  position: absolute;
  top: 20px;
  right: 45px;
  font-size: 30px;
}
.overlay.button {
  background-color: Transparent;
  background-repeat: no-repeat;
  cursor: pointer;
  overflow: hidden;
  outline: none;
}
@media screen and (max-height: 450px) {
  .overlay a {
    font-size: 20px;
  }
  .overlay .closebtn {
    font-size: 40px;
    top: 15px;
    right: 35px;
  }
}

.column1 {
  float: left;
  min-width: 20em;
  min-height: 25em;
  background: rgb(47, 68, 85, 0.7);
  margin-top: 20px;
  margin-left: 20px;
  text-align: center;
  border-radius: 25px;
  display: inline-block;
  margin-right: 15px;
}

.column2 {
  float: left;
  min-width: 20em;
  min-height: 25em;
  background: rgb(47, 68, 85, 0.7);
  position: center;
  margin-top: 20px;
  text-align: center;
  border-radius: 25px;
  margin-right: 15px;
  margin-left: 15px;
  display: inline-block;
}
.column3 {
  float: left;
  min-width: 20em;
  min-height: 25em;
  background: rgb(47, 68, 85, 0.7);
  margin-top: 20px;
  text-align: center;
  margin-right: 15px;
  margin-left: 15px;
  border-radius: 25px;
  display: inline-block;
}
.column4 {
  float: left;
  min-width: 20em;
  min-height: 25em;
  background: rgb(47, 68, 85, 0.7);
  margin-top: 20px;
  text-align: center;
  margin-right: 15px;
  margin-left: 15px;
  border-radius: 25px;
  display: inline-block;
}
.create {
  padding: 10px 25px;
  margin: 4px 2px;
  background-color: #1c87c9;
  border: 3px solid #095484;
  border-radius: 5px;
  text-align: center;
  text-decoration: none;
  font-size: 20px;
  color: #fff;
  cursor: pointer;
}
.addGateError {
  color: red;
  padding-top: 35px;
  padding-left: 20px;
  text-align: center;
  font-size: 40px;
  display: inline-block;
}
#hover-element {
  display: none;
  position: absolute;
  background-color: lightgray;
  padding: 10px;
  border: solid;
  border-radius: 5px;
}

#hover-div:hover #hover-element {
  display: block;
}
</style>
