<template>
  <div class="toolbox">
    <div class="tools-container">
      <div class="box-labels">
        <div class="tool-box-label">
          <label>Toolbox</label>
        </div>
        <div class="custom-gate-label">
          <label>Custom Gates</label>
        </div>
      </div>
      <div class="toolbox-of-gates">
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
              <div class="gate-name">{{ element.name }}</div>
            </div>
          </transition-group>
        </draggable>
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
              <div class="gate-name">{{ element.name }}</div>
            </div>
          </transition-group>
        </draggable>
        <div class="Area2">
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
                <div class="gate-name">{{ element.name }}</div>
              </div>
            </transition-group>
          </draggable>
          <input class="angle" type="number" name="rx" placeholder="90" id />
          <input class="angle" type="number" name="ry" placeholder="PI/2" id />
          <input class="angle" type="number" name="rz" placeholder="PI/2" id />
        </div>

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
              <div class="gate-name">{{ element.name }}</div>
            </div>
          </transition-group>
        </draggable>
      </div>
      <draggable
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
            <div class="gate-name">{{ element.name }}</div>
          </div>
        </transition-group>
      </draggable>
    </div><br>
    <div class="user-tools">
      <button class="qasm" @click="qasm">|qasm⟩</button>
      <div id="myNav" class="overlay">
        <a href="javascript:void(0)" class="closebtn" @click="closeNav()"
          >&#10006;</a
        >
        <div class="column1">
          <h1 class="p" style="color: black ">from matrix</h1>
          <p style="color: black">nameof gate:</p>
          <input type="text" id="nameofgate" />
          <h3 style="color: black">enter gate</h3>
          <textarea rows="4" id="valueofgate"></textarea>
          <br />
          <button
            @click="create_the_matrix()"
            style="background: none;color: white; border: 1px solid white; font-size: 20px; margin-top: 10px;"
          >
            create
          </button>
        </div>
        <div class="column2">
          <h1 style="color: black">from rotation</h1>
        </div>
        <div class="column3">
          <h1 style="color: black">from circuit</h1>
        </div>
      </div>
      <button class="addGate" @click="openNav()">Add Custom Gate</button>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
export default {
  name: "toolbox",
  display: "toolbox",
  components: {
    draggable,
  },
  data() {
    return {
      gates1: [
        { name: "c", id: "c", index: "" },
        { name: "m", id: "m", index: "" },
        { name: "oc", id: "oc", index: "" },
        { name: "reset", id: "reset", index: "" },
      ],
      gates2: [
        { name: "x", id: "x", index: "" },
        { name: "y", id: "y", index: "" },
        { name: "z", id: "z", index: "" },
        { name: "h", id: "h", index: "" },
        { name: "swap", id: "swap", index: "" },
      ],
      gates3: [
        { name: "rx", id: "rx", index: "" },
        { name: "ry", id: "ry", index: "" },
        { name: "rz", id: "rz", index: "" },
      ],
      gates4: [
        { name: "s", id: "s", index: "" },
        { name: "t", id: "t", index: "" },
        { name: "sdg", id: "sdg", index: "" },
        { name: "tdg", id: "tdg", index: "" },
      ],
      customGates: [],
      w: "width:7.7em",
    };
  },
  methods: {
    log: function(/*evt*/) {},
    // ----------------------------------------------------
    cloneGate({ name }) {
      return {
        name: name,
      };
    },
     // ----------------------------------------------------
    addGate(nameofgate) {
      this.customGates.push({
        name: nameofgate,
        id: this.customGates.length + 1,
      });
      this.w = "width:" + Math.ceil(this.customGates.length / 2) * 3.85 + "em";
    },
     // ----------------------------------------------------
    openNav() {
      document.getElementById("myNav").style.width = "100%";
    },
     // ----------------------------------------------------
    closeNav() {
      document.getElementById("myNav").style.width = "0%";
    },
     // ----------------------------------------------------
    create_the_matrix() {
      this.closeNav();
      var nameofgate = document.getElementById("nameofgate").value;
      var valofgate = document.getElementById("valueofgate");
      var matrix = this.make_matrix(valofgate);
      window.console.log(matrix);
      var { matrix_validate, msg } = this.validate_of_matrix(matrix);
      window.console.log(matrix_validate);
      window.console.log(msg);
      if (matrix_validate) {
        this.addGate(nameofgate);
      }
      document.getElementById("nameofgate").value = null;
      document.getElementById("valueofgate").value = null;
    },
     // ----------------------------------------------------
    make_matrix(valofgate) {
      var row = valofgate.value.split("\n");
      var count;
      var matrix = [];
      for (count in row) {
        row[count] = row[count].replace(/\s/g, "");
        var sub = row[count].split(",");
        if (row[count] !== undefined && row[count] != "") {
          matrix.push(sub);
        }
      }
      return matrix;
    },
     // ----------------------------------------------------
    validate_of_matrix(matrix) {
      var matrix_validate = true;
      var msg = "please check the dimenons of the matrix";
      var count1, count2, count3, check;
      var regex = /^(-)?\d+$|^(-)?i$|^(-)?\d+(-|\+)(\d+)?i$|^(-)?\d+i$|^(-)?(\d+)?i(-|\+)\d$/;
      if (nameofgate==""){
        msg="you have to enter name for gate";
        matrix_validate=false;
        return{matrix_validate,msg};
      }
      if (Number.isInteger(Math.log2(matrix.length))) {
        matrix_validate = true;
      } else {
        matrix_validate = false;
        return { matrix_validate, msg };
      }
      for (count3 in matrix)
        if (matrix.length != matrix[count3].length) {
          matrix_validate = false;
          msg = "please check if the number of rows equal columns";
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
    qasm() {
      this.$parent.qasmFlag = !this.$parent.qasmFlag;
    },
     // ----------------------------------------------------
  },
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
  background-color:#979A9A;
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
  white-space: pre-wrap;
  height: 6.6em;
  width: 11.6em;
}
.custom-gates {
  border: 1px solid black;
  display: inline-block;
  height: 7.4em;
  overflow: auto;
  border-radius: 0.3em;
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
  margin: 0.3em 0.7em 0.3em 0.5em;
  width: 3em;
  height: 3em;
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
  width: 400px;
  min-height: 300px;
  background: rgb(47, 68, 85, 0.7);
  float: left;
  margin-top: 20px;
  margin-left: 20px;
  text-align: center;
  border-radius: 25px;
  display: inline-block;
  margin-right: 30px;
}

.column2 {
  width: 400px;
  min-height: 300px;
  background: rgb(47, 68, 85, 0.7);
  position: center;
  margin-top: 20px;
  text-align: center;
  border-radius: 25px;
  margin-right: 30px;
  display: inline-block;
}
.column3 {
  width: 400px;
  min-height: 300px;
  background: rgb(47, 68, 85, 0.7);
  margin-top: 20px;
  text-align: center;

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
</style>
