<template>
  <div class="toolbox">
 
    <draggable
      :list="gates"
      :group="{ name: 'gates', pull: 'clone', put: false }"
      :clone="cloneGate"
    >
      <transition-group type="transition" name="flip-list" class="toolbox-gates-area">

      <!--------------------- Gates ----------------should be a component------------->
        <div class="toolbox-gates" v-for="gate in this.gates" :key="gate.id" :id="gate.name">
          <div class="gate-name" id="hover-div" v-if="gate.name[0]!='c'">
            {{ gate.name.toUpperCase() }}
            <!-- <span id="hover-element">{{ gate.info }}</span> -->
            <input
              v-if="gate.name == 'rx' || gate.name == 'ry' || gate.name == 'rz' "
              class="angle-input"
              :id="gate.name+ 'Angle'"
              type="number"
              :name="gate.name"
              value="90"
            />
          </div>
          <div v-else>{{ gate.id }}</div>  <!-- in case of custom gates -->
        </div>
        <!---------------------end of Gates --------------------------------------->
      </transition-group>
    </draggable>


    <div class="user-tools">
      <div class="qasm-box">
        <button id="qasmToolboxBtn" class="qasm" @click="$parent.$refs.qasm.qasm()">| qasm ⟩</button>
        <button
          class="matrix-btn"
          @click="$parent.$refs.matrixRepresentation.openNav()"
        >Matrix Representation</button>
      </div>

      <div class="circiut-loop">
        <Circiutloops :colsCount="this.jsonObject.colsCount" />
      </div>

      <div class="number-of-shots">
        <label class="lbl1">Shots</label>
        <input class="ibmToken" type="number" placeholder="1024" v-model="jsonObject.shots" />
      </div>

      <div class="degree-or-radian">
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
      </div>
      <div>
        <addcustomgate class="add-custom-gate-box" ref="addcustomgate"></addcustomgate>
      </div>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
import addcustomgate from "./addcustomgate";
import Circiutloops from "./CircuitLoops.vue";
import { mapState , mapGetters } from "vuex";

export default {
  name: "Toolbox",
  display: "Toolbox",
  components: {
    draggable,
    addcustomgate,
    Circiutloops
  },
  data() {
    return {
      //  gates: this.gates(),
      customGates: [] // terminated
    };
  },
  computed: {
    ...mapState(["jsonObject"]),
    ...mapGetters(['gates'])
  },
  methods: {
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
    }
    // ----------------------------------------------------
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
.gates-name {
  display: flex;
  flex-basis: 100%;
  flex-wrap: wrap;
}

.custom-gates {
  margin: 0em;
  flex-basis: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: baseline;
}
.custom-gates span {
  display: flex;
}

#rx,
#ry,
#rz {
  align-self: center;
}

#rx,
#ry,
#rz,
#reset,
#swap {
  font-size: 10px;
  color: white;
}

#rx .gate-name,
#ry .gate-name,
#rz .gate-name,
#reset .gate-name,
#swap .gate-name {
  font-size: 10px;
  padding: 0px;
  margin: 0px;
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
  flex-basis: 10%;
}
.circiut-loop {
  flex-basis: 12%;
}
.number-of-shots {
  flex-basis: 10%;
}
.number-of-shots input {
  margin: 0em 0em 0em 1em;
  width: 70px;
  border-radius: 5px;
}

.degree-or-radian {
  margin: 0em 0em 0em 1em;
  flex-basis: 18%;
}
.add-custom-gate-box {
  flex-basis: 20%;
}

/* ==================  */

.flip-list-move {
  transition: transform 0.3s;
}

.shots {
  display: inline-block;
  margin: 0em 1em 0em 1em;
}

.qasm {
  margin: 0em 0em 0em 0.2em;
  background-color: white;
  border-radius: 0.5em;
  display: inline-block;
}

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
input[type=number] {
  -moz-appearance: textfield;
}

textarea:focus, input:focus{
    outline: none;
}
</style>
