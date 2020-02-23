<template>
  <div class="circuit">
    <div class="upper-circuit">
      <toolbox></toolbox>
      <ibm></ibm>
    </div>
    <!-- <trash></trash> -->
    <div class="wires">
      <wire v-for="row in rows" :key="row" :id="row" :ref="'wire'"></wire>
    </div>
    <div class="toolbox-2">
      <trash></trash>
      <div class="wires-buttons">
        <button class="add-wire" @click="rows++">Add Wire</button>
        <button class="remove-wire" @click="rows--">Remove Wire</button>
        <button class="add-wire" @click="showSystem">show system on console</button>
        <button class="add-wire" @click="systemStates">send</button>
        <button class="add-wire" @click="resetSystem">reset system</button>
      </div>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import toolbox from "./toolbox.vue";
import wire from "./wire.vue";
import ibm from "./ibm.vue";
import trash from "./trash.vue";
import axios from "axios";

export default {
  name: "clone",
  display: "clone",
  components: {
    toolbox,
    ibm,
    wire,
    trash
  },
  data() {
    return {
      states: ["0", "1", "i", "-i", "+", "-"],
      rows: 4,
      system: {},
      globalId: 0,
      maxWire: 0,
      statesSystem: [],
      gatesSystem: {},
      jobject: []
    };
  },
  methods: {
    showSystem: function() {
      //window.console.log("my parent app called me");
      //for (let i in this.system) {
      //window.console.log(i + ": " + JSON.stringify(this.system[i]) + "\n");
      //}
      //window.console.log(typeof(this.system));
      //window.console.log(this.system);
      this.$parent.allSystem = this.system;
      //this.$parent.showAllSystem();
      this.$root.info;

      /*
     this.systemStates();
      //window.console.log(JSON.stringify(this.system));
      axios.post("http://localhost:5000/mario",this.system).then((res)=>{
      window.console.log(res);
      this.systemStates();
    });
      
 */
    },
    updateSystem: function(wireId, wireData) {
      //window.console.log("update ");
      this.system[wireId] = wireData;
      if (this.maxWire < wireData[1].length) {
        this.maxWire = wireData[1].length;
        //window.console.log("maximum wire length " + this.maxWire);
      }
    },
    /*
    accessWire: function(wireId) {
      var wireCaller = this.$refs.wire[wireId - 1];
      window.console.log(wireCaller.showWire());
    },
    */
    resetSystem: function() {
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.resetWire();
      }
    },
    rowIdentity: function(wireId) {
      for (let i = 0; i < this.rows; i++) {
        if (i + 1 != wireId) {
          var wireCaller = this.$refs.wire[i];
          wireCaller.addIdentity();
        }
      }
    },

    allRowIsIdentiy: function() {
      //window.console.log("reached from wire");
      //var count = 0;
      /*
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        if (wireCaller.lastIdentity() == "i") {
          //count++;
          wireCaller.popLast();
        }
      }
    
      if (count == this.rows) {
        this.pruneIdentityRow();
      }
      */
    },
    pruneIdentityRow: function() {
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.popLast();
      }
      this.maxWire--;
    },
    controlWire: function(wireId) {
      for (let i = wireId + 1; i < this.rows; i++) {
        //var wireCaller = this.$refs.wire[i];
      }
    },
    systemStates: function() {
      this.jobject = [];
      this.statesSystem = [];
      this.gatesSystem = [];
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        this.statesSystem.push(wireCaller.getState());
        this.gatesSystem.push(wireCaller.getGates());
      }
      window.console.log(this.statesSystem);
      window.console.log(this.gatesSystem);
      this.send();
    },
    send: function() {
      this.jobject.push({
        wires: this.rows,
        init: this.statesSystem,
        rows: this.gatesSystem
      });

      axios.post("http://localhost:5000/data", this.jobject).then(res => {
        window.console.log(res);
      });
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.upper-circuit {
  /*border: 3px solid black;*/
  display: inline-block;
  margin: 0.2em 0.2em 0.2em 0.2em;
  padding: 0em 0em 0em 0em;
  width: 99%;
}
.wires {
  /*border: 0.1em dashed blue;*/
  margin: 1em 0.1em 0em 0.1em;
}
.flip-list-move {
  transition: transform 10.9s;
}
.wires-buttons {
  display: inline-block;
  margin: 0.9em 0.2em 0.2em 0.2em;
  padding: 0em 0em 0em 0em;
}
.add-wire {
  display: inline-block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
.remove-wire {
  display: inline-block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
}
.trashArea {
  color: #ef9494;
  border: 0.1em dashed #ef9494;
  border-radius: 0.2em;
  display: block;
  margin: 0.2em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  width: 97%;
  text-align: center;
}
</style>
