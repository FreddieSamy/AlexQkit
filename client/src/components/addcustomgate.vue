<template>
  <div class="add-custom-gate">
    <!--  begin  overlay for add custom gates   -->
    <div id="myNav" class="overlay" style="width:0%">
      <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>
      <!--  begin  enter custom gate as matrix (first column)   -->
      <div class="column">
        <h1>Add Matrix</h1>
        <h3>Name</h3>
        <input type="text" id="nameofgate" maxlength="4" required />
        <h3>number of wires</h3>
        <CustomMx ref="matrixcu"></CustomMx>
        <br />
        <button @click="create_the_matrix()">create</button>
      </div>
      <!--  end  enter custom gate as matrix (first column)   -->
      
      <div class="column">
        <h1>sub-circuit</h1>
        <h3>name</h3>
        <input type="text" id="subCircuitName" />
        <h3>Rows</h3>
        <label class="from-to">From</label>
        <select id="fromRow">
          <option v-for="i in this.jsonObject.wires" :key="i" :value="i">{{i}}</option>
        </select>
        <label class="from-to">To</label>
        <select id="toRow">
          <option v-for="i in this.jsonObject.wires" :key="i" :value="i">{{i}}</option>
        </select>
        <h3>Columns</h3>
        <label class="from-to">From</label>
        <select id="fromColumn">
          <option v-for="i in this.jsonObject.colsCount" :key="i" :value="i">{{i}}</option>
        </select>
        <label class="from-to">To</label>
        <select id="toColumn">
          <option v-for="i in this.jsonObject.colsCount" :key="i" :value="i">{{i}}</option>
        </select>
        <br />
        <button @click="subCircuitCustomGate()">create</button>
      </div>

      <div class="column">
        <h1>
          n
          <sup>th</sup> root of gate
        </h1>

        <h3>select the gate</h3>
        <select id="rootGate">
          <optgroup label="Gates">
            <option value="X">X</option>
            <option value="Y">Y</option>
            <option value="Z">Z</option>
            <option value="H">H</option>
            <option value="S">S</option>
            <option value="T">T</option>
            <option value="Sdg">S†</option>
            <option value="Tdg">T†</option>
          </optgroup>
          <optgroup v-if="nthRootCustomGates().length" label="Custom Gates">
            <option
              v-for="element in nthRootCustomGates()"
              :key="element.id"
              :value="element.name"
            >{{ element.id }}</option>
          </optgroup>
        </select>
        <h3 style="color: black;">root</h3>
        <input id="root" type="number" value="2" />
        <br />
        <div>
          <input type="checkbox" id="adjointCheckbox" />
          <label for="adjointCheckbox">Adjoint</label>
        </div>
        <button @click="nthRoot()">create</button>
      </div>
    </div>
    <!--  end  overlay for add custom gates   -->

    <button class="addGate" @click="openNav()">Add Custom Gate</button>
  </div>

</template>
<!-- =============================================================  -->
<script>
import axios from "axios";
import CustomMx from "./custom_mx.vue";
import { mapState, mapActions, mapGetters } from "vuex";
import {
  addCustomGates,
  subCirciutRoute,
  nthRootRoute
} from "./../data/routes";
export default {
  name: "addcustomgate",
  display: "addcustomgate",
  components: {
    CustomMx
  },
  data() {
    return {
      // capturedImage: ""
    };
  },
  computed: {
    ...mapState(["jsonObject"]),
    ...mapGetters(["gates"])
  },
  methods: {
    ...mapActions(["addCustomGate"]),
    // ----------------------------------------------------
    /* 
      - addGate function : add it to customgate dictionary in "gates_and_states.js"
    */
    addGate(gateName, gateWires) {
      this.addCustomGate({
        name: "c" + gateWires + "_" + gateName+"."+(gateWires-1),
        id: gateName,
        wires: gateWires
      });
    },
    // ----------------------------------------------------
    /* 
      - openNav function: to open overlay of add custom gate button
        when you press on it  
    */
    openNav() {
      document.getElementById("myNav").style.width = "100%";
      document.getElementById("subCircuitName").value = null;
      document.getElementById("nameofgate").value = null;
    },
    // ----------------------------------------------------
    /* 
      - closeNav function: to close overlay of add custom gate button
        when you press on (X) in top right the overlay 
    */
    closeNav() {
      document.getElementById("myNav").style.width = "0%";
      document.getElementById("wires").value = null;
      var conmatrixcu2 = this.$refs.matrixcu;
      conmatrixcu2.clear();
    },
    // ----------------------------------------------------
    /* 
      - create_the_matrix function: it's responsible to 
        custom gate as matrix "first column " to call
        custom_mx and pull the data and the check the
        validation of the matrix 
    */
    create_the_matrix() {
      var nameofgate = document.getElementById("nameofgate").value;
      //var valofgate = document.getElementById("valueofgate");
      var conmatrixcu = this.$refs.matrixcu;
      var { matrix, numwires } = conmatrixcu.pulldata(matrix, numwires);
      var { matrix_validate, msg } = this.validate_of_matrix(
        matrix,
        nameofgate
      );
      var isUnitary;
      var json_object = { matrix: matrix, gateName: nameofgate };

      if (matrix_validate) {
        axios.post(addCustomGates, json_object).then(res => {
          isUnitary = res.data.isUnitary;
          if (isUnitary) {
            this.addGate(nameofgate, numwires);

            this.closeNav();
          } else {
            alert(
              "please, enter unitary matrix.\nenter data with \nabsolute tolerance : 1e-5 \nrelative tolerance : 1e-8  "
            );
          }
        });
      } else {
        alert(msg);
      }
    },
    // ----------------------------------------------------
    // check if the name is already exist
    isExist(nameofgate) {
      for (let i in this.gates) {
        if (this.gates[i]["id"] === nameofgate) {
          return true;
        }
      }
      return false;
    },
    // ----------------------------------------------------
    /* 
      - validate_of_matrix: used to check the matrix that user enter it .
    */
    validate_of_matrix(matrix, nameofgate) {
      var matrix_validate = true;
      var msg = "please check the dimenons of the matrix";
      var count1, count2, check;
      var regex = /^(-)?([0-9][.])?[0-9]+$|^(-)?(([0-9][.])?[0-9]+)?i$|^(-)?([0-9][.])?[0-9]+(-|\+)(([0-9][.])?[0-9]+)?i$/;

      // check if the name is already exist
      if (this.isExist(nameofgate)) {
        matrix_validate = false;
        msg = "this name is already exist,please choose different name";
        return { matrix_validate, msg };
      }

      // check if the name is empty
      if (nameofgate == "" || nameofgate.length == 0) {
        matrix_validate = false;
        msg = "you have to write name for the gate";
        return { matrix_validate, msg };
      }

      // if it contains "." for backend reason
      if (nameofgate.includes(".")) {
        matrix_validate = false;
        msg = "name of gate can't include '.'";
        return { matrix_validate, msg };
      }

      // check the value of every input is correct or not
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
    subCircuitCustomGate: function() {
      //validates the inputs and call createSubCircuit() function for valid inputs
      var name = document.getElementById("subCircuitName").value;
      var fromRow = document.getElementById("fromRow").value;
      var toRow = document.getElementById("toRow").value;
      var fromColumn = document.getElementById("fromColumn").value;
      var toColumn = document.getElementById("toColumn").value;
      if (fromRow && toRow && fromColumn && toColumn) {
        if (fromRow <= toRow && fromColumn <= toColumn) {
          if (name == "" || name.length == 0) {
            alert("you have to write name for the gate");
          } else {
            if (this.isExist(name)) {
              alert("this name is already exist,please choose different name");
            } else {
              this.createSubCircuit(fromRow, toRow, fromColumn, toColumn, name);
            }
          }
        } else {
          alert("please, check the selected numbers");
        }
      }
    },
    //-----------------------------------------------------------------------
    createSubCircuit: function(fromRow, toRow, fromColumn, toColumn, name) {
      /*
      constructs jsonObject for the subCircuit and sends it to the backend
      custom gates created and stored at the backend 
      stores the gate in "gates_and_states.js" using addGate() function 
      */
      var gatesSystem = []; //get the selected rows and columns from the jsonObject "jsonObject.js"
      for (let i = fromRow - 1; i < toRow; i++) {
        gatesSystem.push(
          this.jsonObject.rows[i].slice(fromColumn - 1, toColumn)
        );
      }
      var wires = toRow - fromRow + 1; //num_qubits of the gate
      var json_object = {
        gateName: name,
        wires: wires,
        rows: gatesSystem,
        radian: this.jsonObject.radian
      };

      axios.post(subCirciutRoute, json_object).then(res => {
        //check if the gate is unitary in the backend
        if (res.data.isUnitary) {
          var name = document.getElementById("subCircuitName").value;
          this.addGate(name, wires); //store the gate in "gates_and_states.js"
          document.getElementById("subCircuitName").value = null;
          this.closeNav();
        } else {
          alert("sorry, this subcircuit isn't unitary");
        }
      });
    },
    // ----------------------------------------------------
    nthRoot: function() {
      /*
      validates the inputs of the nthRoot custom gates
      constructs the json_object to send it to the backend
      stores the gate name in "gates_and_states.js" using addGate() function
      */
      var select = document.getElementById("rootGate");
      var name = select.options[select.selectedIndex].value;
      window.console.log(name);
      var num_qubits = 1;
      if (name[0] == "c") {
        // for custom gates   "c<num_qubits>_<name>"
        var underscorePos = name.indexOf("_");
        num_qubits = name.slice(1, underscorePos);
        name = name.slice(underscorePos + 1);
      }
      var root = document.getElementById("root").value;
      var adjointFlag = document.getElementById("adjointCheckbox").checked;
      var newGateName = "√(" + name + ")";
      if (root != 2) {
        newGateName = root + newGateName;
      }
      if (adjointFlag) {
        newGateName += "†";
      }
      if (this.isExist(newGateName)) {
        alert("sorry, " + newGateName + " is already exist");
      } else {
        var json_object = {
          root: root,
          gateName: name,
          newGateName: newGateName,
          adjoint: adjointFlag
        };
        if (root >= 2) {
          axios.post(nthRootRoute, json_object).then(res => {
            if (res.data.isUnitary) {
              this.addGate(newGateName, num_qubits);
              this.closeNav();
            } else {
              alert("sorry, " + newGateName + " isn't unitary");
            }
          });
        } else {
          alert("please, choose number more than one !!");
        }
      }
      document.getElementById("adjointCheckbox").checked = false;
    },
    // ----------------------------------------------------

    nthRootCustomGates: function() {
      // to select custom gates from the stored gates and display them in the nth root list
      var gates = [];
      for (let i = 17; i < this.gates.length; i++) {
        //start at i=17 to avoid the normal gates "x,y,... "
        if (!this.gates[i].id.includes("√")) {
          gates.push(this.gates[i]);
        }
      }
      return gates;
    }
    // ----------------------------------------------------
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
div {
  color: white;
}
.overlay {
  height: 100%;
  top: 0;
  left: 0;
  position: fixed;
  z-index: 1;
  background-color: rgba(103, 106, 97, 0.55);
  overflow-x: hidden;
  transition: 0.5s;
  display: flex;
  justify-content: center;
  align-items: stretch;
  flex-wrap: wrap;
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

.column {
  background: rgb(47, 68, 85, 0.7);
  margin: 3em;
  padding: 1em;
  border-radius: 1em;
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
button {
  background: white;
  border-radius: 0.5em;
  border: 2px solid grey;
  margin: 30px 0px 0px 100px;
}
.addGate {
  display: inline-block;
  margin: 0em 0em 0em 0.2em;
  background-color: white;
  color: black;
  border-radius: 0.5em;
}
.from-to {
  color: black;
  margin-left: 0.4em;
  margin-right: 0.2em;
}
input {
  border-radius: 10px;
}
input[type="number"] {
  padding: 0px 0px 0px 5px;
  width: 50px;
}
select {
  border-radius: 10px;
  width: 100px;
}
h3 {
  margin: 20px 1px 10px 1px;
}
</style>
