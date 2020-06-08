<template>
  <div class="toolbox">
    <!--  Tooolbox Draggable Area for gates -->
    <draggable
      :list="gates"
      :group="{ name: 'gates', pull: 'clone', put: false }"
      :clone="cloneGate"
    >
      <transition-group type="transition" name="flip-list" class="toolbox-gates-area">
        <!--------------------- Gates ----------------should be a component------------->
        <div class="toolbox-gates" v-for="gate in this.gates" :key="gate.id" :id="gate.name">
          <div class="gate-name" id="hover-div" v-if="gate.name[0]!='c'">
            {{ gate.name }}
            <!-- <span id="hover-element">{{ gate.info }}</span> -->

            <input
              v-if="gate.name == 'Rx' || gate.name == 'Ry' || gate.name == 'Rz' "
              class="angle-input"
              :id="gate.name+ 'Angle'"
              type="number"
              :name="gate.name"
              value="90"
            />
          </div>
          <div v-else>{{ gate.id }}</div>
          <!-- in case of custom gates -->
        </div>
        <!---------------------end of Gates --------------------------------------->
      </transition-group>
    </draggable>
    <!-- End Tooolbox Draggable Area for gates -->

    <!-- toolbox user-tools Qasm,Matrix representation,add custom gate,angle gate degree,number of shots --> 
    <div class="user-tools">
      <div class="qasm-box">
        <button id="qasmToolboxBtn" class="qasm" @click="$parent.$refs.qasm.qasm()">| qasm ⟩</button>

        <button
          class="matrix-btn"
          @click="$parent.$refs.matrixRepresentation.openNav()"
        >Matrix Representation</button>
      </div>

      <!-- Add Custom Gate Button to open it's window -->
      <addcustomgate class="add-custom-gate-box" ref="addcustomgate"></addcustomgate>
      <!-- end Custom Gate -->

      <!-- Radian Degree Radio box  -->
      <input
        type="radio"
        id="degree"
        name="angleType"
        :value="false"
        v-model="jsonObject.radian"
        checked
      />
      <label for="degree" style="font-size: 15px;">degree</label>
      <input type="radio" id="radian" name="angleType" :value="true" v-model="jsonObject.radian" />
      <label for="radian" style="font-size: 15px;">radian</label>
      <!-- End Radian Degree Radio box -->

      <!-- Number of shots box -->
      <div class="number-of-shots">
        <label class="lbl1">Shots</label>
        <input class="ibmToken" type="number" placeholder="1024" v-model="shots" />
      </div>
      <!-- End Number of shots box -->
    
    </div>
    <!-- end tool box user tools -->
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
import addcustomgate from "./addcustomgate";
import { mapState, mapGetters } from "vuex";

export default {
  name: "Toolbox",
  display: "Toolbox",
  components: {
    draggable,
    addcustomgate
  },
  data() {
    return {
      customGates: [], // terminated
      shots: 1024
    };
  },

  // watcher for validate number of shots (i think it's over engineered)
  watch: {
    shots: {
      immediate: true,
      handler() {
        this.$nextTick(() => {
          this.inputisempty();
        });
      }
    }
  },
  computed: {
    ...mapState(["jsonObject"]),
    ...mapGetters(["gates"])
  },
  methods: {
    // The Function that responsible for clone the gate from toolbox to (Wire or Trash)
    // it take the name of gate and return gate object {name:gateName} append to (wire or trash) list
    cloneGate({ name }) {
      if (name == "Rx") {
        name = name + "(" + document.getElementById("RxAngle").value + ")";
      } else if (name == "Ry") {
        name = name + "(" + document.getElementById("RyAngle").value + ")";
      } else if (name == "Rz") {
        name = name + "(" + document.getElementById("RzAngle").value + ")";
      }
      return {
        name: name
      };
    },
    // Validate the number of shots  
    inputisempty() {
      if (this.shots.length) {
        alert("number of shots will be add 1024 if you entered nothing");
        this.jsonObject.shots = 1024;
      } else {
        this.jsonObject.shots = this.shots;
      }

      // ----------------------------------------------------
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.toolbox {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  flex-wrap: wrap;
  padding: 0px;
  margin: 0px;
  min-width: 49em;
}
.toolbox-labels {
  flex-basis: 100%;
}
.toolbox-gates-area {
  flex-basis: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: baseline;
}
.toolbox-gates {
  color: white;
  font-size: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-radius: 6px;
  margin: 0em 0.5em 0.5em 0.5em;
  padding: 0px;
  width: 35px;
  height: 35px;
  background-color: #5d6d7e;
  z-index: 0;
}
#Rx,
#Ry,
#Rz,
#Reset,
#Swap {
  align-self: center;
  font-size: 10px;
  color: white;
}
.angle-input {
  display: flex;
  flex-basis: 100%;
  margin: 0px auto;
  text-align: center;
  padding: 2px 0px 2px 0px;
  width: 75%;
  font-size: 10px;
  border-radius: 8px;
}
.user-tools {
  flex-basis: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: flex-start;
  align-items: baseline;
}
.qasm-box {
  margin:0px 0px 0px 20px;
  flex-basis: 10%;
}
.number-of-shots {
  margin:0px 40px;
}
.number-of-shots input {
  margin: 0em 0em 0em 1em;
  width: 70px;
  border-radius: 5px;
}
.degree-or-radian {
  margin: 0em 1.5em 0em 5.6em;
  flex-basis: 15%;
}
.add-custom-gate-box {
  flex-basis: 20%;
}

/* ==================  */

#hover-element {
  display: none;
  position: absolute;
  background-color: lightgray;
  padding: 10px;
  border: solid;
  border-radius: 5px;
  opacity: 0.001;
}
#hover-div:hover #hover-element {
  display: block;
}
button {
  border: 2px solid grey;
  margin: 0px 10px;
  background-color: white;
  border-radius: 0.5em;
  display: inline-block;
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type="number"] {
  -moz-appearance: textfield;
}

textarea:focus,
input:focus {
  outline: none;
}
</style>
