<template>
  <div class="wire" :id="'wire-' + id">
    <div class="delete-wire" :id="'d-' + id">
      <button class="delete" @click="deleteWire">x</button>
    </div>
    <div class="qubit">
      <button class="qubitState" :id="'q' + id + '-0'" @click="qubitState">
        |{{ state }}⟩
      </button>
    </div>
    <draggable
      class="wire-drop-area"
      :list="list"
      group="gates"
      @change="change"
    >
      <div
        class="circuit-gate"
        v-for="element in list"
        :key="element.id"
        :id="element.name"
        v-text="element.name"
      ></div>
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
    change: function(event) {
      this.$parent.updateMaxWire(); // update wire that has maximum gates
      var eventName = Object.keys(event)[0];
      /*var gateName = event[eventName]["element"]["name"]; */
      //var gateIndex = event[eventName]['newIndex'];
      if (eventName == "added") {
        this.$parent.addIdentityToColumn(this.id);
      }
      this.$parent.removeIdentitySystem();
      /* this.$parent.showSystem(); */
    },
    //-----------------------------------------------------------
    qubitState: function(evt) {
      var i = (parseInt(evt.target.id["3"]) + 1) % 6;
      var id = evt.target.id.substring(0, 3);
      evt.target.id = id + i;
      evt.target.innerHTML = "|" + this.$parent.states[i] + "⟩";
      this.state = this.$parent.states[i];
      this.update();
    },
    //-----------------------------------------------------------
    deleteWire: function(evt) {
      var el = evt.target.parentNode.parentNode;
      el.parentNode.removeChild(el);
    },
    //-----------------------------------------------------------
    addIdentity: function() {
      for (let i = this.list.length; i < this.$parent.maxWire; i++) {
        this.list.push({ name: "i" });
      }
    },
    getGateByIndex: function(gateIndex) {
      window.console.log(this.list[gateIndex]);
      return this.list[gateIndex];
    },
    removeGateByIndex: function(gateIndex) {
      if (this.list[gateIndex]["name"] == "i") {
        //window.console.log("remove "+gateIndex+" th gate at wire"+this.id);
        this.list.splice(gateIndex, 1);
      }
    },
    //-----------------------------------------------------------
    resetWire: function() {
      this.list = [];
    },
    //-----------------------------------------------------------
    lastIdentity: function() {
      if (this.list.length == this.$parent.maxWire) {
        return this.list[this.$parent.maxWire - 1]["name"];
      } else {
        return "";
      }
    },
    //-----------------------------------------------------------
    popLast: function() {
      this.list.pop();
    },
    //-----------------------------------------------------------
    getState: function() {
      return this.state;
    },
    //-----------------------------------------------------------
    getGates: function() {
      this.gates = [];
      for (let i = 0; i < this.list.length; i++) {
        this.gates.push(this.list[i]["name"]);
      }
      return this.gates;
    },
    setState: function(state) {
      this.state = state;
    },
    //-----------------------------------------------------------
    setGates: function(gatesList) {
      this.list = gatesList;
    },
    //-----------------------------------------------------------
    objectNames: function(listOfObject) {
      var names = [];
      for (let i = 0; i < listOfObject.length; i++) {
        names.push(listOfObject[i]["name"]);
      }
      return names;
    }
    //-----------------------------------------------------------
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.wire {
  margin: 0.7em 0em 0em 0em;
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
  opacity: 0.03;
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
