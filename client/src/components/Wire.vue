<template>
  <div class="wire" :id="'wire-' + id">
    <div class="delete-wire" :id="'d-' + id">
      <button class="delete" @click="deleteWire">x</button>
    </div>

    <label class="qubit-name">
      q
      <sub>{{id-1}}</sub>
    </label>

    <!-- <div class="qubit"> -->
    <button class="qubit-state" :id="'q' + id + '-0'" @click="qubitState">|{{ state }}⟩</button>
    <!-- </div> -->

    <draggable
      class="wire-drop-area"
      :id="'list' + id"
      :list="list"
      group="gates"
      @add="add"
      @remove="remove"
      @update="update"
    >
      <div
        class="circuit-gate"
        v-for="element in list"
        :key="element.id"
        :id="element.name"
        v-html="displayName(element.name)"
      ></div>
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
    this.setGatesIdentity();
  },
  updated() {
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

    //== Events Handling Functions ===============================================
    add: function(evt) {
      if (evt.from.id[0] == "l") {
        var wire = evt.from.id.replace("list", "");
        this.$parent.$refs.wire[wire - 1].addGateByIndex(evt.oldIndex);
      }
      this.$parent.updateMaxWire();
      this.$parent.addIdentityToColumn(this.id);
      this.$parent.removeIdentitySystem();
    },
    //-----------------------------------------------------------------------
    update: function() {
      this.$parent.updateMaxWire();
      this.$parent.addIdentityToColumn(this.id);
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
      window.console.log("update Wire " + this.id + " Attributes");
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
      this.runCircuit();
    },
    //-----------------------------------------------------------------------
    deleteWire: function() {
      this.jsonObject.rows.splice(this.id - 1, 1);
      this.jsonObject.init.splice(this.id - 1, 1);
      this.jsonObject.wires--;
      window.console.log(this.jsonObject);
      this.$parent.setAlgorithm(this.jsonObject, false);
      this.$parent.removeIdentitySystem();
    },
    //-----------------------------------------------------------------------
    addIdentity: function() {
      // add identiy across the columns of same wire (row)
      for (let i = this.list.length; i < this.jsonObject.colsCount; i++) {
        this.list.push({ name: "i" });
      }
    },
    //-----------------------------------------------------------------------
    getGateByIndex: function(gateIndex) {
      return this.list[gateIndex];
    },
    //-----------------------------------------------------------------------
    addGateByIndex: function(gateIndex) {
      this.list.splice(gateIndex, 0, { name: "i" });
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
    getState: function() {
      return this.state;
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
        this.list.push({ name: gatesList[colIdx] });
      }
    },
    //-----------------------------------------------------------------------
    setGatesIdentity: function() {
      // when add a new wire
      var maxWire = this.jsonObject.colsCount;
      let list = [...this.list];
      for (let colIdx = 0; colIdx < maxWire; colIdx++) {
        list.push({ name: "i" });
      }
      this.list = list;
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
  background-size: 20px 40px;
  background-position: center;
  background-image: url("../assets/wire.png");
  z-index: -1;
}
.wire-drop-area {
  height: 37px;
  display: flex;
  flex-basis: 80%;
  /* border: 1px solid black; */
}

.qubit-name {
  margin: 0px 5px 0px -5px;
  padding: 0px 5px 0px 0px;
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
  justify-content: center;
  align-items: center;
  text-align: center;
  border: 0.5px solid grey;
  border-radius: 0.5em;
  margin: 0em 0.5em 0em 0.5em;
  padding: 0px;
  width: 35px;
  height: 35px;
  background-color: #5d6d7e;
  z-index: 0;
}
#rx,
#ry,
#rz {
  align-self: center;
}

div[id^="r"],
#swap {
  font-size: 10px;
  margin: 0em 0.75em 0em 0.75em;
}

div[id^="rx"],
div[id^="ry"],
div[id^="rz"] {
  font-weight: bold;
  background: #ff8c61;
}
#○,
#● {
  /* hena fe moshkela  */
  color: black;
  line-height: 10px;
  margin: 0em 0.265em 0em 0.265em;
  font-size: 30px;
  background: none;
  border: none;
}
#○ {
  /* need to edit this over engineering*/
  background-image: url("../assets/whitedot.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 11px 11px;
}

/* .delete-wire {
  float: left;
  margin: 0.7em 0em 0em 0em;
  padding: 0.5em 0em 0em 0em;
  width: 1.5em;
  height: 1em;
  display: inline-table;
}
.delete {
  opacity: 0.9;
  margin: 0.9em 0em 0em 0em;
  padding: 0em 0em 0em 0em;
  border-radius: 10em;
  width: 1.5em;
  height: 2em;
  background-color: #ef9494;
  color: white;
  border-color: transparent;
  font-size: 0.6em;
} 
*/
img {
  width: 40px;
  height: 40px;
}
#i {
  opacity: 0.91;
}
#m .circuit-gate text {
  opacity: 0.01;
}
</style>
