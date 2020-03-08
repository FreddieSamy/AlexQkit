<template>
  <div class="wire" :id="'wire-' + id">
    <!--
    <div class="delete-wire" :id="'d-' + id">
      <button class="delete" @click="deleteWire">x</button>
    </div>
    -->
    <div class="qubit">
      <button class="qubitState" :id="'q' + id + '-0'" @click="qubitState">
        |{{ state }}⟩
      </button>
    </div>
    <draggable
      class="wire-drop-area"
      :list="list"
      group="gates"
      @add="add"
      @remove="remove"
      @update="update"
      @onEnd="change"
    >
      <div
        class="circuit-gate"
        v-for="element in list"
        :key="element.id"
        :id="element.name"
      >
      {{element.name}}
      </div>
    </draggable>
  </div>
</template>
<!-- =============================================================  -->
<script>
import draggable from "vuedraggable";

export default {
  name: "wire",
  display: "wire",
  components: {
    draggable
  },
  data() {
    return {
      list: [],
      state: "0",
      gates: []
    };
  },
  props: ["id"],
  methods: {
    //-----------------------------------------------------------------------
    add: function(evt) {
      this.updateGate(evt);
      this.$parent.updateMaxWire(); 
      this.$parent.addIdentityToColumn(this.id);
      this.$parent.removeIdentitySystem();
      this.$parent.controlSystem();
    },
    update: function(evt) {
      this.updateGate(evt);
      this.$parent.updateMaxWire(); 
      this.$parent.removeIdentitySystem();
      this.$parent.controlSystem();
    },
    remove: function() {
      this.addIdentity();
      this.$parent.removeIdentitySystem();   
      this.$parent.updateMaxWire();
      this.$parent.controlSystem();
    },
    change: function(/*evt*/) {
     this.$parent.updateSystem();
    },
    updateGate:function(evt){
      var gate = evt.to.childNodes[evt.newIndex];
      var row = this.id;
      var col = (evt.newIndex+1);
      gate.setAttribute('row',"_"+row);
      gate.setAttribute('col',"_"+col);
      this.$parent.updateMaxWire();
    },
    //-----------------------------------------------------------------------
    qubitState: function(evt) {
      var i = (parseInt(evt.target.id["3"]) + 1) % 6;
      var id = evt.target.id.substring(0, 3);
      evt.target.id = id + i;
      evt.target.innerHTML = "|" + this.$parent.states[i] + "⟩";
      this.state = this.$parent.states[i];
    },
    //-----------------------------------------------------------------------
    deleteWire: function(evt) {
      var el = evt.target.parentNode.parentNode;
      el.parentNode.removeChild(el);
    },
    //-----------------------------------------------------------------------
    addIdentity: function() {
      for (let i = this.list.length; i < this.$parent.maxWire; i++) {
        this.list.push({ name: "i" });
      }
    },
    //-----------------------------------------------------------------------
    getGateByIndex: function(gateIndex) {
      window.console.log(this.list[gateIndex]);
      return this.list[gateIndex];
    },
    //-----------------------------------------------------------------------
    removeGateByIndex: function(gateIndex) {
      if (this.list[gateIndex]["name"] == "i") {
        //window.console.log("remove "+gateIndex+" th gate at wire"+this.id);
        this.list.splice(gateIndex, 1);
      }
    },
    //-----------------------------------------------------------------------
    resetWire: function() {
      this.list = [];
    },
    //-----------------------------------------------------------------------
    lastIdentity: function() {
      if (this.list.length == this.$parent.maxWire) {
        return this.list[this.$parent.maxWire - 1]["name"];
      } else {
        return "";
      }
    },
    //-----------------------------------------------------------------------
    popLast: function() {
      this.list.pop();
    },
    //-----------------------------------------------------------------------
    getState: function() {
      return this.state;
    },
    //-----------------------------------------------------------------------
    getGates: function(rowId) {
      this.gates = [];
      for (let colIdx = 0; colIdx < this.list.length; colIdx++) {
        if (this.list[colIdx]["name"].startsWith("custom_")) {
          this.gates.push(this.list[colIdx]["name"] + "." + rowId);
        } else {
          this.gates.push(this.list[colIdx]["name"]);
        }
      }
      return this.gates;
    },
    //-----------------------------------------------------------------------
    setState: function(state) {
      this.state = state;
    },
    //-----------------------------------------------------------------------
    setGates: function(gatesList) {
      this.list = [];
      for (let colIdx = 0; colIdx < gatesList.length; colIdx++) {
        this.list.push({ name: gatesList[colIdx] });
      }
    },
    //-----------------------------------------------------------------------
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.wire {
  margin: 0.7em 0em 0em 0em;
  z-index:-1;
}
.circuit-gate {
  color: white;
  text-align: center;
  line-height: 2.5em;
  border: 0.15em solid black;
  border-radius: 0.7em;
  display: inline-block;
  margin: 0.8em 0.5em 0.5em 0.5em;
  padding: 0em 0em 0em 0em;
  width: 2.5em;
  height: 2.5em;
  background-color: #5d6d7e;
  z-index:2;
}

.lbl-wire {
  margin: 0.8em 0.5em 0.5em 0.5em;
}
.qubit {
  float: left;
  margin: 0.7em 0em 0em 0em;
  padding: 0em 0em 0em 0em;
  width: 3em;
  height: 3em;
  display: inline-table;
}
.qubitState {
  margin: 0.9em 0em 0em 0em;
  border-radius: 0.5em;
  width: 2.5em;
  height: 2em;
  background-color: white;
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
.wire-drop-area {
  height: 70px;
  width: 100%;
  margin: auto;
  max-width: 90%;
  padding: auto;
  display: inline-table;
  background-size: contain;
  background-image: url("../assets/wire.png");
  /*border: 0.1em dashed black;*/
}
#i {
  opacity: 0.5;
}
/*
#c{
  
  color:black;
  background-color:white;
  background-size: 2.4em 2.9em;
  background-image: url("../assets/c.png");
  border:transparent;
  
}
*/


</style>
