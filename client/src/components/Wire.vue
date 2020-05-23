<template>
  <div class="wire" :id="'wire-' + id">
    <!--
    <div class="delete-wire" :id="'d-' + id">
      <button class="delete" @click="deleteWire">x</button>
    </div>
    -->
    <div class="qubit">
      <button class="qubitState" :id="'q' + id + '-0'" @click="qubitState">|{{ state }}⟩</button>
    </div>

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
import { mapActions, mapGetters, mapState } from "vuex";
import { states } from "./../data/gates_and_states";

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
    //let wire = { qstate: this.state, list: this.getGates(), idx: this.id - 1 };
    //this.setWire(wire);
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
        // window.console.log("hello from wire "+this.id)
        this.$nextTick(() => {
          if (this.id == this.jsonObject.wires) {
            //window.console.log("wire :"+this.id+" send the system");
            //this.$parent.controlSystem();
            //this.runCircuit();
            //window.console.log("hello watcher of "+this.id)
          }
        });

      }
    }
  },

  methods: {
    ...mapActions(["setWire"]),
    ...mapActions(["runCircuit"]),
    //-----------------------------------------------------------------------
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
    findswap: function() {
      //window.console.log(this.$parent.jsonObject);
      for (let rowsx = 0; rowsx < this.jsonObject.rows.length; rowsx++) {
        if (this.jsonObject.rows[rowsx][0] == "swap") {
          window.console.log(this.jsonObject.rows[rowsx][0]);

          window.console.log("rows=" + rowsx + "column 0");
          //this.helperswapcols(rowsx,0);
        }
      }
    },
    //-------------------------------------------------------------------------
    // helperswapcols:function(rowindex,columnindex){
    //  var countswaps=0;
    //   for (let rowsx = 0; rowsx < this.$parent.jsonObject.rows.length; rowsx++){
    //     if(rowindex==rowsx){
    //       continue;
    //     }
    //     else{
    //       if(this.$parent.jsonObject.rows[rowindex][columnindex]=="swap"){
    //         countswaps=countswaps+1;

    //       }
    //     }

    //   }
    //   window.console.log(countswaps);

    // },
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
    //-----------------------------------------------------------------------
    updateGate: function(gate, row, col) {
      gate.setAttribute("row", "_" + row);
      gate.setAttribute("col", "_" + col);
    },
    //-----------------------------------------------------------------------
    updateWireAttributes: function() {
      // replace it by javascript numpy alternative
      let wire = document.querySelector("#list" + this.id + "");
      if (this.list.length) {
        let gates = wire.childNodes;
        for (let i = 0; i < this.list.length; i++) {
          this.$nextTick(() => {
            this.updateGate(gates[i], this.id, i + 1);
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
    deleteWire: function(evt) {
      var el = evt.target.parentNode.parentNode;
      el.parentNode.removeChild(el);
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
    setGates: function(gatesList,append=true) {
      if(append == false){
        this.list = [];  // disabled to push on the wire 
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
    displayName: function(name) {
      if (name.startsWith("custom_")) {
        return name.slice(7).toUpperCase();
      } else {
        return name.toUpperCase();
      }
    },
    //-----------------------------------------------------------------------
    renderBlochSphere: function() {
      this.renderComponent = false;
      this.$nextTick(() => {
        // Add the component back in
        this.renderComponent = true;
      });
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.wire {
  margin: 0px;
  z-index: -1;
  display: flex;
  align-items: flex-start;
  height: 45px;
  background-size: 20px 38px;
  background-image: url("../assets/wire.png");
  /* border: 0.5px dashed black; */
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
.wire-drop-area {
  height: 40px;
  display: flex;
  flex-basis: 80%;
}
.qubit {
  margin: -1px 0px 0px 0px;
  padding: 0px;
  width: 3em;
  height: 3em;
  display: flex;
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
  color: black;
  line-height: 10px;
  margin: 0em 0.265em 0em 0.265em;
  font-size: 30px;
  background: none;
  border: none;
}
#○ {
  background-image: url("../assets/whitedot.png");
  background-repeat: no-repeat;
  background-position: center;
  background-size: 11px 11px;
}

.lbl-wire {
  margin: 0.8em 0.5em 0.5em 0.5em;
}

.qubitState {
  margin: 0.5em 0em 0em 0em;
  border-radius: 0.5em;
  width: 2.5em;
  height: 2em;
  background-color: white;
  border: 2px solid #306ba2;
}
.delete-wire {
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
  /*opacity:0.4;*/
}
img {
  width: 40px;
  height: 40px;
}
#i {
  opacity: 0.01;
}
#m .circuit-gate text {
  opacity: 0.01;
}
</style>
