<template>
  <div class="add-custom-gate">
    <div id="myNav" class="overlay">
      <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>

      <div class="column1">
        <h1 class="p" style="color: black ">from matrix</h1>
        <h3 style="color: black">name</h3>
        <input type="text" id="nameofgate" />
        <h3 style="color: black">number of wires</h3>
        <CustomMx ref="matrixcu"></CustomMx>
        <br />
        <button
          @click="create_the_matrix()"
          style="background: none;color: white; border: 1px solid white; font-size: 20px; margin-top: 10px;"
        >create</button>
      </div>

      <!-- <div class="column2">
        <h1 style="color: black;">from rotation</h1>
        <h3 style="color: black;">select the gate</h3>
      </div>-->

      <div class="column3">
        <h1 style="color: black;">from circuit</h1>
        <h3 style="color: black;">Name</h3>
        <input type="text" id="subCircuitName" />
        <h3 style="color: black;">Rows</h3>
        <label style="color: black;">From</label>
        <select id="fromRow" style="width:15%;">
          <option v-for="i in this.$parent.$parent.rows" :key="i" :value="i">{{i}}</option>
        </select>
        <label style="color: black;">To</label>
        <select id="toRow" style="width:15%;">
          <option v-for="i in this.$parent.$parent.rows" :key="i" :value="i">{{i}}</option>
        </select>
        <h3 style="color: black;">Columns</h3>
        <label style="color: black;">From</label>
        <select id="fromColumn" style="width:15%;">
          <option v-for="i in this.$parent.$parent.maxWire" :key="i" :value="i">{{i}}</option>
        </select>
        <label style="color: black;">To</label>
        <select id="toColumn" style="width:15%;">
          <option v-for="i in this.$parent.$parent.maxWire" :key="i" :value="i">{{i}}</option>
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
        <input style="width:40%;" id="root" type="number" value="2" />
        <button
          @click="nthRoot()"
          style="background: none;color: white; border: 1px solid white; font-size: 20px; margin-top: 2em;"
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
      // capturedImage: "",
      customsrever: {}
    };
  },
  methods: {
    openNav() {
      document.getElementById("myNav").style.width = "100%";
      document.getElementById("subCircuitName").value = null;
      document.getElementById("nameofgate").value = null;

      // html2canvas(document.querySelector("#circuit-wires")).then(canvas => {
      //   this.capturedImage = canvas.toDataURL();
      //   window.console.log("canvas.toDataURL() -->" + this.capturedImage);
      //   canvas.toBlob(function(blob) {
      //     var reader = new FileReader();
      //     reader.readAsDataURL(blob);
      //     reader.onloadend = function() {
      //       let base64data = reader.result;
      //       window.console.log("Base64--> " + base64data);
      //     };
      //   });
      // });
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
          // window.console.log("new unitary:" + isUnitary);
          if (isUnitary) {
            this.addGate(nameofgate);
            this.customsrever[nameofgate] = matrix;
            // window.console.log(this.customsrever);
            this.closeNav();
          } else {
            alert("please, enter unitary matrix");
          }
        });
      } else {
        alert(msg);
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
    sendtotoolbox() {
      return this.customsrever;
    },
    // ----------------------------------------------------
    nthRoot: function() {
      var select = document.getElementById("rootGate");
      var backName = select.value;
      var name = select.options[select.selectedIndex].text;
      // window.console.log(name);
      var root = document.getElementById("root").value;
      if (name + "^(1/" + root + ")" in this.customsrever) {
        alert("sorry, " + name + "^(1/" + root + ")" + " is already exist");
      } else {
        var jsonObject = {
          root: root,
          gate: backName,
          custom: this.customsrever
        };
        if (root >= 2) {
          axios.post("http://localhost:5000/nthRoot", jsonObject).then(res => {
            /*window.console.log(res.data);*/
            if (res.data.isUnitary) {
              this.addGate(name + "^(1/" + root + ")");
              this.customsrever[name + "^(1/" + root + ")"] = res.data.matrix;
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

      var jsonObject = {
        wires: toRow - fromRow + 1,
        rows: gatesSystem
      };
      axios
        .post("http://localhost:5000/subCircuitCustomGate", jsonObject)
        .then(res => {
          if (res.data.isUnitary) {
            var name = document.getElementById("subCircuitName").value;
            this.addGate(name);
            window.console.log(res.data.matrix);
            this.customsrever[name] = res.data.matrix;
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
/* .zddGateError {
  color: red;
  padding-top: 35px;
  padding-left: 20px;
  text-align: center;
  font-size: 40px;
  display: inline-block;
} */
.addGate {
  display: inline-block;
  margin: 0em 0em 0em 0.2em;
  background-color: white;
  border-radius: 0.5em;
}
</style>
