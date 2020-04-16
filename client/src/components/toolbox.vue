<template>
  <div class="toolbox">
    <!-- toolcox-labels -->
    <div class="toolbox-labels">
      <label>Toolbox</label>
      <label v-if="customGates.length">Custom Gates</label>
    </div>
    <!--end box-labels-->

    <!-- ---------------------- gates  -------------------------- -->

    <draggable
      :list="gates"
      :group="{ name: 'gates', pull: 'clone', put: false }"
      :clone="cloneGate"
      @change="log"
    >
      <transition-group type="transition" name="flip-list" class="toolbox-gates-area">
        <div class="toolbox-gates" v-for="gate in gates" :key="gate.id" :id="gate.name">
          <!-- in case of angle-gates -->
          <div
            v-if="gate.name == 'rx' || gate.name == 'ry' || gate.name == 'rz' "
            class="gate-name"
            id="hover-div"
          >
            {{ gate.name }}
            <div>
              <input
                class="angle"
                :id="gate.name+ 'Angle'"
                type="number"
                :name="gate.name"
                value="90"
              />
            </div>
            <span id="hover-element">{{ gate.info }}</span>
          </div>
          <!-- else cases (add built in gates ) -->
          <div v-else class="gate-name" id="hover-div">
            {{ gate.name }}
            <span id="hover-element">{{ gate.info }}</span>
          </div>
        </div>
      </transition-group>
    </draggable>

    <!-- ------------------- end built in gates and start custom gates ---------- -->
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

    <!--------------------   end of custom gates  ----------------------- -->
    <div class="user-tools">
      <div class="qasm-box">
        <button id="qasmToolboxBtn" class="qasm" @click="this.$parent.qasm">| qasm ⟩</button>
      </div>

      <div class="number-of-shots">
        <label class="lbl1">Number Of Shots</label>
        <input class="ibmToken" type="number" placeholder="1024" id="numberofshots" />
      </div>

      <div class="degree-or-radian">
        <input type="radio" id="degree" name="angleType" value="degree" checked />
        <label for="degree" style="font-size: 15px;">degree</label>
        <input type="radio" id="radian" name="angleType" value="radian" />
        <label for="radian" style="font-size: 15px;">radian</label>
      </div>

      <div class="add-custom-gate-box">
        <addcustomgate ref="addcustomgate"></addcustomgate>
      </div>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import { mapState } from "vuex";
import draggable from "vuedraggable";
import addcustomgate from "./addcustomgate";

export default {
  name: "toolbox",
  display: "toolbox",
  components: {
    draggable,
    addcustomgate
  },
  computed: {
    ...mapState(["gates"])
  },
  data() {
    return {
      customGates: [],
      w: "width:7.7em",
      customsrever: {}
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
    sendtoclone() {
      var z = this.$refs.addcustomgate;
      return z.sendtotoolbox();
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
}
.toolbox-labels {
  flex-basis: 100%;
}

.toolbox-gates-area {
  margin: 1em;
  flex-basis: 100%;

  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: baseline;
}

.toolbox-gates {
  text-align: center;
  margin: 0.3em 0.7em 0.3em 0.5em;
  width: 2.5em;
  height: 2.5em;
  border-radius: 0.3em;
  background-color: #979a9a;
}

.toolbox-gates input {
  text-align: center;
  margin: 0px 0px 0px 0px;
  padding: 3px 0px 2px 0px;
  width: 90%;
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
  flex-basis: 15%;
}

.number-of-shots {
  flex-basis: 15%;
}
.number-of-shots input {
  margin: 0em 0em 0em 1em;
  border-radius: 5px;
}

.degree-or-radian {
  margin: 0em 0em 0em 2em;
  flex-basis: 25%;
}
.add-custom-gate-box {
  margin: 0em 0em 0em 2em;
  flex-basis: 25%;
}

/* ==================  */

.angle-gates {
  border: 1px solid black;
  border-radius: 0.5em;
  margin: 0.1em 0.1em 0.1em 0.1em;
  /* white-space: pre-wrap; */
}
.custom-gates {
  border: 1px solid black;
  display: inline-block;
  height: 7.4em;

  border-radius: 0.3em;
  min-width: 7.7em;
}

.flip-list-move {
  transition: transform 0.3s;
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
}
#hover-div:hover #hover-element {
  display: block;
}
</style>
