<template>
  <div class="add-custom-gate">
    <div id="myNav" class="overlay" style="width:0%">
      <a href="javascript:void(0)"  class="closebtn" @click="closeNav()">&#10006;</a>

      <div class="column">
        <h1>Add Matrix</h1>
        <h3>Name</h3>
        <input type="text" id="nameofgate" required />
        <h3>number of wires</h3>
        <CustomMx ref="matrixcu"></CustomMx>
        <br />
        <button
          @click="create_the_matrix()"
        >create</button>
      </div>

      <!--
       <div class="column">
        <h1 style="color: black;">from rotation</h1>
        <h3 style="color: black;">select the gate</h3>
       </div>
      -->
      <div class="column">
        <h1 >sub-circuit</h1>
        <h3 >name</h3>
        <input type="text" id="subCircuitName" />
        <h3>Rows</h3>
        <label class="from-to">From</label>
        <select id="fromRow" >
          <option v-for="i in this.$parent.$parent.jsonObject.wires" :key="i" :value="i">{{i}}</option>
        </select>
        <label class="from-to">To</label>
        <select id="toRow">
          <option v-for="i in this.$parent.$parent.jsonObject.wires" :key="i" :value="i">{{i}}</option>
        </select>
        <h3>Columns</h3>
        <label class="from-to">From</label>
        <select id="fromColumn">
          <option v-for="i in this.$parent.$parent.maxWire" :key="i" :value="i">{{i}}</option>
        </select>
        <label class="from-to">To</label>
        <select id="toColumn">
          <option v-for="i in this.$parent.$parent.maxWire" :key="i" :value="i">{{i}}</option>
        </select>
        <br />
        <button
          @click="subCircuitCustoGate()"
        >create</button>
      </div>

      <div class="column">
        <h1> n<sup>th</sup> root of gate</h1>
 
     
        <h3>select the gate</h3>
        <select id="rootGate" >
          <optgroup label="Gates">
            <option value="x">X</option>
            <option value="y">Y</option>
            <option value="z">Z</option>
            <option value="h">H</option>
            <option value="s">S</option>
            <option value="t">T</option>
            <option value="sdg">S†</option>
            <option value="tdg">T†</option>
          </optgroup>
          <optgroup v-if="nthRootCustomGates().length" label="Custom Gates">
            <option
              v-for="element in nthRootCustomGates()"
              :key="element.id"
              :value="element.id"
            >{{ element.id }}</option>
          </optgroup>
        </select>
        <h3 style="color: black;">root</h3>
        <input id="root" type="number" value="2"  />
        <br />
        <button
          @click="nthRoot()"
        >create</button>
      </div>

      <!-- <img class="capturedImage" :src="capturedImage" /> -->

      <!-- <div class="addGateError">
        <label id="errormsg"></label>
      </div>-->
    </div>

    <button class="addGate" @click="openNav()">Add Custom Gate</button>
  </div>
</template>
<!-- =============================================================  -->
<script>
//import draggable from "vuedraggable";
import axios from "axios";
import CustomMx from "./custom_mx.vue";
// import html2canvas from "html2canvas";
export default {
  name: "addcustomgate",
  display: "addcustomgate",
  components: {
    //draggable,
    CustomMx
  },
  data() {
    return {
      // capturedImage: ""
    };
  },
  methods: {
    openNav() {
      document.getElementById("myNav").style.width = "100%";
      document.getElementById("subCircuitName").value = null;
      document.getElementById("nameofgate").value = null;
    },
    // ----------------------------------------------------
    closeNav() {
      document.getElementById("myNav").style.width = "0%";
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
      var isUnitary;
      var json_object = {};
      json_object["matrix"] = matrix;

      if (matrix_validate) {
        axios.post("http://localhost:5000/isUnitary", json_object).then(res => {
          //window.console.log("the data success to returned be from the server");
          isUnitary = res.data.isUnitary;
          //isUnitary; //to hassan.. it's a boolean data which represent if the matrix is unitary or not
          // window.console.log("new unitary:" + isUnitary);
          if (isUnitary) {
            this.addGate(nameofgate);
            this.$parent.$parent.jsonObject.custom[nameofgate] = matrix;
            this.closeNav();
          } else {
            alert("please, enter unitary matrix");
          }
        });
      } else {
        alert(msg);
      }
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
    nthRoot: function() {
      var select = document.getElementById("rootGate");
      var backName = select.value;
      var name = select.options[select.selectedIndex].text;
      // window.console.log(name);
      var root = document.getElementById("root").value;
      if (
        name + "^(1/" + root + ")" in
        this.$parent.$parent.jsonObject.custom
      ) {
        alert("sorry, " + name + "^(1/" + root + ")" + " is already exist");
      } else {
        var json_object = {
          root: root,
          gate: backName,
          custom: this.$parent.$parent.jsonObject.custom
        };
        if (root >= 2) {
          axios.post("http://localhost:5000/nthRoot", json_object).then(res => {
            /*window.console.log(res.data);*/
            if (res.data.isUnitary) {
              this.addGate(name + "^(1/" + root + ")");
              this.$parent.$parent.jsonObject.custom[
                name + "^(1/" + root + ")"
              ] = res.data.matrix;
              this.closeNav();
            } else {
              alert("sorry, " + name + "^(1/" + root + ")" + " isn't unitary");
            }
          });
        } else {
          alert("please, choose number more than one !!");
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
            alert("please, enter a name for the gate");
          } else {
            for (let i in this.$parent.customGates) {
              for (let k in this.$parent.customGates[i]) {
                if (this.$parent.customGates[i][k] === name) {
                  flag = false;
                  alert("this name is already exist");
                }
              }
            }
            if (flag) {
              this.cloneSubCircuitCustoGate(
                fromRow,
                toRow,
                fromColumn,
                toColumn
              );
            }
          }
        } else {
          alert("please, check the selected numbers");
        }
      }
    },
    //-----------------------------------------------------------------------
    cloneSubCircuitCustoGate: function(fromRow, toRow, fromColumn, toColumn) {
      var gatesSystem = [];
      for (let i = fromRow - 1; i < toRow; i++) {
        gatesSystem.push(
          this.$parent.$parent.jsonObject.rows[i].slice(
            fromColumn - 1,
            toColumn
          )
        );
      }

      var json_object = {
        wires: toRow - fromRow + 1,
        rows: gatesSystem
      };
      axios
        .post("http://localhost:5000/subCircuitCustomGate", json_object)
        .then(res => {
          if (res.data.isUnitary) {
            var name = document.getElementById("subCircuitName").value;
            this.addGate(name);
            this.$parent.$parent.jsonObject.custom[name] = res.data.matrix;
            document.getElementById("subCircuitName").value = null;
            this.closeNav();
          } else {
            alert("sorry, this subcircuit isn't unitary");
          }
        });
    },
    // ----------------------------------------------------
    addGate(nameofgate) {
      this.$parent.customGates.push({
        name: "custom_" + nameofgate,
        id: nameofgate
      });
      if (this.$parent.customGates.length < 9) {
        this.$parent.w =
          "width:" +
          Math.ceil(this.$parent.customGates.length / 2) * 3.85 +
          "em";
      } else {
        this.$parent.w = "width:15.9em";
      }
    },
    // ----------------------------------------------------
    nthRootCustomGates: function() {
      var gates = [];
      for (let element of this.$parent.customGates) {
        if (!element.id.includes("^(1/")) {
          gates.push(element);
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
div{
  color:white
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
  justify-content:center;
  align-items:stretch;
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

.column{
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
/* .zddGateError {
  color: red;
  padding-top: 35px;
  padding-left: 20px;
  text-align: center;
  font-size: 40px;
  display: inline-block;
} */
button{
  background:white;
  border-radius: 10px;
  border:3px solid grey;
  margin:30px 0px 0px 100px;
}
.addGate {
  display: inline-block;
  margin: 0em 0em 0em 0.2em;
  background-color: white;
  color:black;
  border-radius: 0.5em;
}
.from-to {
  color: black;
  margin-left: 0.4em;
  margin-right: 0.2em;
}
input{
  border-radius: 10px;
}
input[type="number"]{
  padding:0px 0px 0px 5px;
  width:50px;
}
select{
  border-radius:10px;
  width:100px;
}
h3{
  margin: 20px 1px 10px 1px;
}
</style>
