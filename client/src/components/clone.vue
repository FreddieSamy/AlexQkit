<template>
  <div class="circuit">
    <div class="upper-circuit">
      <toolbox></toolbox>
     <!-- <ibm></ibm> --> 
    </div>
    <br />
    <div class="qasmAndWires">
      <div class="qasm" v-if="qasmFlag">
        <textarea>OPENQASM 2.0; include "qelib1.inc";</textarea>
        <button class="qasmBtn">Run</button>
      </div>
      <div class="wiresBlock">
        <div class="wires">
          <wire v-for="row in rows" :key="row" :id="row" :ref="'wire'"></wire>
        </div>
      </div>
    </div>
    <div class="toolbox-2">
      <trash></trash>
      <div class="wires-buttons">
        <button class="add-wire" @click="rows++">Add Wire</button>
        <button class="remove-wire" @click="rows--">Remove Wire</button>
        <button class="add-wire" @click="sendSystem">send</button>
        <button class="add-wire" @click="resetSystem">reset system</button>
        <button class="add-wire" @click="clearConsole">Clear Console</button>
      </div>
    </div>
    <diracNotation></diracNotation>
    <div class="visual-row">
        <histoGram></histoGram>
        <blochSphere></blochSphere>
    </div>
  </div>
</template>
<!-- =============================================================  -->
<script>
import toolbox from "./toolbox.vue";
import wire from "./wire.vue";
//import ibm from "./ibm.vue";
import trash from "./trash.vue";
import axios from "axios";
import blochSphere from "./blochSphere.vue";
import histoGram from "./histoGram.vue";
import diracNotation from "./diracNotation.vue";

export default {
  name: "clone",
  display: "clone",
  components: {
    toolbox,
   //ibm,
    wire,
    trash,
    blochSphere,
    histoGram,
    diracNotation
  },
  data() {
    return {
      diracNotationData: "|00⟩",
      route: "http://localhost:5000/data",
      states: ["0", "1", "+", "-", "i", "-i"],
      rows: 2,          // number of wires
      maxWire: 0,       // maximum number of gates in a wire   
      system: {}, 
      qasmFlag: false,
      jsonObject: [
                  {
                    wire: 0,
                    init: [],
                    rows: []
                  }
      ],
    };
  },
  methods: {
    //---------------------------------------------
    showSystem:function(){
       for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        window.console.log(JSON.stringify(wireCaller.list));
      }
    },
    updateMaxWire: function() {
      let firstWire = this.$refs.wire[0];
      this.maxWire = firstWire.list.length;
      for (let i = 1 ; i < this.rows ; i++){
          let wireCaller = this.$refs.wire[i];
          if(wireCaller.list.length > this.maxWire){
              this.maxWire = wireCaller.list.length
          }
      }
      // window.console.log("max wire = "+this.maxWire); 
    }, 
    //---------------------------------------------
    resetSystem: function() {
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        wireCaller.resetWire();
      }
    },
    //---------------------------------------------
    addIdentityToColumn: function(wireId) {
      for (let i = 0; i < this.rows; i++) {
         if(i + 1 != wireId ){
           var wireCaller = this.$refs.wire[i];
           wireCaller.addIdentity();
         }
      }
    },
    //---------------------------------------------
    removeIdentityColumn: function() {

    },
    //---------------------------------------------
    isAllColumnIdentity:function(columnIndex){
     // var identiyCounter = 0
      for(let i = 0 ; i < this.rows ; i++){
          var wireList = this.$refs.wire[i].list;
          var gateName = wireList[columnIndex]['name'];
          if(gateName.localeCompare('i')!==0){
           //window.console.log("found a gate on column "+columnIndex+" is not identiy '+gateName");
           return false;
          }
      }
     // window.console.log("all coulmn is "+columnIndex+" identity");
      return true;
  
    },
       //---------------------------------------------
    removeIdentitySystem:function(){
      for(let i = this.maxWire-1 ; i >=0 ; i-- ){
          this.isAllColumnIdentity(i);

          
      }

    },
    //---------------------------------------------
    sendSystem: function() {
      var statesSystem = [];
      var gatesSystem = [];
      for (let i = 0; i < this.rows; i++) {
        var wireCaller = this.$refs.wire[i];
        statesSystem.push(wireCaller.getState());
        gatesSystem.push(wireCaller.getGates());
      }
      this.jsonObject[0] = {
        wires: this.rows,
        init: statesSystem,
        rows: gatesSystem
      };
      this.sendToServer(this.route, this.jsonObject);
    },
    //---------------------------------------------
    sendToServer: function(route, jsonObject) {
      axios.post(route, jsonObject).then(res => {
        window.console.log("the data success to returned be from the server");
        window.console.log(res);
        this.draw();
        this.diracNotationData = res.data.diracNotation;
      });
    },
    //---------------------------------------------
    clearConsole: function() {
      window.console.clear();
    },
    //---------------------------------------------
    draw: function() {
      var imgOfHistoGram = document.getElementById("chart");
      imgOfHistoGram.src = "http://127.0.0.1:5000/chart.png?time" + new Date();
      var imgofblochSphere = document.getElementById("bloch");
      imgofblochSphere.src =
        "http://127.0.0.1:5000/blochsphere.png?time=" + new Date();
    },
    //---------------------------------------------
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.circuit{
  white-space: nowrap;
}
.upper-circuit {
  /*border: 3px solid black;*/
  display: flex;
  margin: 0.2em 0.2em 0.2em 0.2em;
  padding: 0em 0em 0em 0em;
  width: 99%;
  white-space:normal;
}
.wires {
  /*border: 0.1em dashed blue;*/
  margin: 0em 0.1em 0em 0.1em;
  /*display: table-cell;*/
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
.qasm {
  display: block;
  width: 30%;
  margin: 0em 0.2em 0em 0em;
  /*border: 1px solid black;*/
  border-radius: 0.5em;
}
.qasmBtn {
  display: block;
  height: 2em;
  width: 5em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
  right: 0;
  top: 0;
}
.wiresBlock {
  /*display: table-cell;*/
  width: 99%;
  height: 99%;
  margin: 0em 0.2em 0em 0.2em;
}
.qasmAndWires {
  /*border: dashed firebrick;*/
  display: inline-flex;
  width: 99%;
  height: 99%;
  margin: 0.2em 0.2em 3em 0.2em;
}
.visual-row{
  display: flex;
}
textarea {
  width: 90%;
  height: 99%;
  bottom: 0;
  /*border: 1px solid black;*/
  border-radius: 0.5em;
  margin: auto;
}
</style>
