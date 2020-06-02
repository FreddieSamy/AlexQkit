<template>
  <div class="wire" :id="'wire-' + id">
    <div class="delete-wire" :id="'d-' + id">
      <button class="delete-btn" @click="deleteWire">x</button>
    </div>

    <label class="qubit-name">
      q
      <sub>{{id-1}}</sub>
    </label>

    <!-- <div class="qubit"> -->
    <button class="qubit-state" :id="'q' + id + '-0'" @click="qubitState">|{{ state }}⟩</button>
    <!-- </div> -->
    <!-- <svg height="210" width="500" style="z-index=10;position:absolute">
    <line x1="1000" y1="0" x2="100" y2="300" style="stroke:rgb(255,0,0);stroke-width:10" />
    </svg>-->
    <hr class="wire-hr" />
    <draggable
      class="wire-drop-area"
      :id="'list' + id"
      :list="list"
      group="gates"
      @add="add"
      @remove="remove"
      @update="update"
    >
      <div class="circuit-gate" v-for="element in list" :key="element.id" :id="element.name">
        {{displayName(element.name)}}
        <select v-if="element.name[0]=='c'" class="custom-gate-order">
          <!-- we will put a v-for here -->
          <option value="0">0</option>
          <option value="1">1</option>
        </select>
      </div>
    </draggable>

    <Percent :probability="this.liveResults.probabilities[id-1]||0" />

    <BlochSphere />
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";
import Percent from "./Percent";
import BlochSphere from "./BlochSphere";
import { states } from "./../data/gates_and_states";
import { mapActions, mapGetters, mapState } from "vuex";

export default {
  name: "wire",
  display: "wire",
  components: {
    draggable,
    Percent,
    BlochSphere
  },
  props: ["id"],
  created: function() {
    this.addIdentityRow(this.jsonObject.colsCount);
  },
  updated() {
    // why this
    let wire = {
      qstate: this.state,
      list: this.getGates(this.id - 1),
      idx: this.id - 1
    };
    this.setWire(wire);
  },
  destroyed() {
    this.$parent.controlSystem();
  },
  computed: {
    ...mapGetters(["wiresCount"]),
    ...mapGetters(["liveResults"]),
    ...mapState(["jsonObject"])
  },
  data() {
    return {
      list: [],
      state: states[0]
    };
  },
  watch: {
    list: {
      immediate: true,
      handler() {
        this.updateWireAttributes();
      }
    }
  },

  methods: {
    ...mapActions(["setWire"]),
    ...mapActions(["runCircuit"]),
    ...mapActions(["setCountControls"]),
    ...mapActions(["setCountSwaps"]),
    ...mapActions(["setCountCustoms"]),

    //== Events Handling Functions ===============================================
    add: function(evt) {
      // in case droped between 2 gates
      if (
        evt.newIndex < this.jsonObject.colsCount &&
        this.list[evt.newIndex + 1]["name"] == "i"
      ) {
        this.list.splice(evt.newIndex + 1, 1);
      } else {
        this.$parent.addIdentityColumn(this.id, evt.newIndex);
      }

      // in case gate draged from wire droped to another wire : evt.from.id = list(n)
      if (evt.from.id[0] == "l") {
        var wire = evt.from.id.replace("list", "");
        this.$parent.$refs.wire[wire - 1].addGateByIndex(evt.oldIndex, "i");
      } else if (evt.clone.id === "●" || evt.clone.id === "○") {
        this.setCountControls(1);
      } else if (evt.clone.id == "swap") {
        this.setCountSwaps(1);
      }
      this.$parent.updateMaxWire();
    },
    //-----------------------------------------------------------------------
    update: function() {
      this.$parent.updateMaxWire();
      this.$parent.removeIdentitySystem();
    },
    //-----------------------------------------------------------------------
    remove: function() {
      this.$parent.updateMaxWire();
      this.$parent.removeIdentitySystem();
    },
    //=============================================================================
    updateGateAtrributes: function(gate, row, col) {
      gate.setAttribute("row", "_" + row);
      gate.setAttribute("col", "_" + col);
    },
    //-----------------------------------------------------------------------
    updateWireAttributes: function() {
      // should be optimzed more
      //window.console.log("update Wire " + this.id + " Attributes");
      let wire = document.querySelector("#list" + this.id + "");
      if (this.list.length) {
        let gates = wire.childNodes;
        for (let i = 0; i < this.list.length; i++) {
          this.$nextTick(() => {
            this.updateGateAtrributes(gates[i], this.id, i + 1);
          });
        }
      }
    },
    //-----------------------------------------------------------------------
    qubitState: function(evt) {
      var i = (parseInt(evt.target.id.slice(-1)) + 1) % 6;
      var id = evt.target.id.substring(0, evt.target.id.search("-") + 1);
      evt.target.id = id + i;
      this.state = states[i];
      evt.target.innerHTML = "|" + this.state + "⟩";
      this.jsonObject.init[id.slice(1, -1) - 1] = this.state;
      // this.runCircuit();
    },
    //-----------------------------------------------------------------------
    deleteWire: function() {
      this.jsonObject.rows.splice(this.id - 1, 1); // vuex it
      this.jsonObject.init.splice(this.id - 1, 1); // vuex it
      this.jsonObject.wires--; // vuex it
      this.$parent.setAlgorithm({ circuit: this.jsonObject }, false, false);
      this.$parent.removeIdentitySystem();
    },
    //-----------------------------------------------------------------------
    addIdentityRow: function(length) {
      this.list.push(...new Array(length).fill({ name: "i" }));
    },
    //-----------------------------------------------------------------------
    addGateByIndex: function(columnIndex, gateName) {
      this.list.splice(columnIndex, 0, { name: gateName });
    },
    //-----------------------------------------------------------------------
    removeGateByIndex: function(gateIndex) {
      if (this.list[gateIndex]["name"] == "i") {
        this.list.splice(gateIndex, 1);
      }
    },
    //-----------------------------------------------------------------------
    resetWire: function() {
      this.list = [];
      this.setState("0");
    },
    //-----------------------------------------------------------------------
    getGates: function(rowId) {
      var gates = [];
      for (let colIdx = 0; colIdx < this.list.length; colIdx++) {
        if (this.list[colIdx]["name"].startsWith("custom_")) {
          gates.push(this.list[colIdx]["name"] + "." + rowId);
        } else {
          gates.push(this.list[colIdx]["name"]);
        }
      }
      return gates;
    },
    //-----------------------------------------------------------------------
    setState: function(state) {
      let i = this.$store.state.states.indexOf(this.state);
      document.getElementById("q" + this.id + "-" + i).innerHTML =
        "|" + state + "⟩";
      document.getElementById("q" + this.id + "-" + i).id =
        "q" + this.id + "-" + state;
      this.state = state;
    },
    //-----------------------------------------------------------------------
    setGates: function(gatesList, append = true) {
      if (append == false) {
        this.list = []; // disabled to push on the wire
      }
      for (let colIdx = 0; colIdx < gatesList.length; colIdx++) {
        // can be optimized more
        this.list.push({ name: gatesList[colIdx] });
        if (gatesList[colIdx] === "●" || gatesList[colIdx] === "○") {
          this.setCountControls(1);
        } else if (gatesList[colIdx] === "swap") {
          this.setCountSwaps(1);
        }
      }
    },
    //-----------------------------------------------------------------------
    //should be put in vuex because we need it in toolbox (or could be terminated)
    displayName: function(name) {
      if (name.startsWith("custom_")) {
        return name.slice(7).toUpperCase();
      } else {
        return name.toUpperCase();
      }
    }
    //-----------------------------------------------------------------------
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.wire {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  
  /* background-position: cover;
  background-repeat: repeat;
  background-image: url("../assets/wire.png"); */
  width: 100%;
  z-index: 0;
  margin: 5px 0px 5px 0px;
}

.wire-drop-area {
  height: 37px;
  display: flex;
  flex-basis: 75%;
}
.wire-hr{
  position: fixed;
  stroke-width: 10;
  width: 100%;
  margin:0px;
  z-index: -4;
  stroke: black;
  color:black;
}

.delete-wire {
  margin: 0px;
  padding: 0px 5px 0px 5px;
  background: white;
  /* border:1px solid black; */
}
.delete-btn {
  color: white;
  background: #ff9890;
  border-radius: 100%;
  padding: 0px 3px 0px 3px;
  border: transparent;
  opacity: 0.5;
}
.delete-btn:hover {
  opacity: 1;
  transform: scale(1.5);
}
.qubit-name {
  margin: 0;
  padding: 0px 7px 0px 7px;
  background: white;
  justify-self: center;
  align-self: center;
  /* border:1px solid black; */
}
.qubit-state {
  border-radius: 0.5em;
  width: 2.5em;
  height: 2em;
  margin-right: 0.6em;
  background-color: white;
  border: 2px solid #306ba2;
}
.circuit-gate {
  color: white;
  font-size: 15px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-radius: 20%;
  margin: 0 5px;
  padding: 0;
  width: 35px;
  height: 35px;
  background-color: #5d6d7e;
  z-index: 0;
}

.custom-gate-order {
  display: flex;
  flex-basis: 100%;
  height: 15px;
  max-width: 30px;
  padding: 0;
  margin: -5px 0px 0px 0px;
  font-size: 10px;
  border-radius: 10px;
}
.angle-input {
  display: flex;
  flex-basis: 100%;
  margin: 0px auto;
  text-align: center;
  padding: 2px 0px 2px 0px;
  width: 75%;

  border-radius: 8px;
}

#rx,
#ry,
#rz {
  align-self: center;
}

div[id^="r"],
#swap {
  font-size: 10px;
  margin: 0em 5px 0em 5px;
}

div[id^="rx"],
div[id^="ry"],
div[id^="rz"] {
  font-weight: bold;
  background: #ff8c61;
}
#○,
#● {
  color: black;
  line-height: 10px;
  margin: -2px 5px 0px 5px;
  /* margin: 0px 7.5px 0px 7.5px; */
  /* font-size: 20px; */
  transform: scale(1.7);
  background: none;
  border: none;
}
#○ {
  background-image: url("../assets/whitedot.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 7px 6px;
}

#i {
  opacity: 0;
}
#m .circuit-gate text {
  opacity: 0.01;
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

option:focus,
select:focus,
textarea:focus,
input:focus {
  outline: none;
}
</style>
