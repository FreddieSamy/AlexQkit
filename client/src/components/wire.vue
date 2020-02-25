<template>
  <div class="wire" :id="'wire-' + id">
    <div class="delete-wire" :id="'d-' + id">
      <button class="delete" @click="deleteWire">x</button>
      <label class="lbl-wire">{{ id }}</label>
    </div>
    <div class="qubit">
      <button class="qubitState"  :id="'q' + id + '-0'" @click="qubitState">
          {{state}}
      </button>
    </div>
    <draggable
      class="wire-drop-area"
      :list="list"
      group="gates"
      @change="update"
      @add="onAdd"
    >
      <div class="circuit-gates" v-for="element in list" :key="element.id" :id="element.name" >
        <div class="gate-name">{{ element.name }}</div>
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
    draggable,
  },
  data() {
    return {
      list: [],
      state: "0",
      gates:[]
    };
  },
  props: ["id"],
  methods: {
    update: function(/*evt*/) {
      var  wireData  = [ this.state,this.objectNames(this.list)];
      this.$parent.updateSystem(this.id,wireData);
    },
    qubitState: function(evt) {
      var i = (parseInt(evt.target.id["3"]) + 1) % 6;
      var id = evt.target.id.substring(0, 3);
      evt.target.id = id + i;
      evt.target.innerHTML = this.$parent.states[i];
      this.state = this.$parent.states[i];
      this.update();
    },
    deleteWire: function(evt) {
      var el = evt.target.parentNode.parentNode;
      el.parentNode.removeChild(el);
    },   
    addIdentity:function() {
      this.list.push({ name: "i"});
      this.update();
    },
    showWire:function(){
        return "wire "+this.id+" called by Clone " + JSON.stringify(this.list);
    },
    resetWire:function(){
         this.list  = [];
    },
    lastIdentity:function(){
        if(this.list.length == this.$parent.maxWire){
          return this.list[this.$parent.maxWire-1]['name'];
        }else{
          return "";
        } 
    },
    popLast:function(){
        this.list.pop();
    },
    onAdd(/*evt*/) {
        this.$parent.rowIdentity(this.id);
      },
    getState:function(){
      return this.state;
    },
    getGates:function(){
      this.gates = [];
      for(let i = 0 ; i < this.list.length ; i++){
        this.gates.push(this.list[i]['name']);
      }
      return this.gates;
    },
    getGateIdenx:function(idx){
      return this.list[idx]['name']
    },
    objectNames:function(listOfObject){
       var names = [];
        for(let i = 0 ; i<listOfObject.length ;i++){
            names.push(listOfObject[i]['name']);
        }
        return names;
    }
    
  },
};
</script>
<!-- =============================================================  -->
<style scoped>
.wire {
  margin: 0.7em 0em 0em 0em;
}
.gate-name {
  text-align: center;
  margin: 0.8em 0.5em 0.5em 0.5em;
}
.circuit-gates {
  color: white;
  border: 0.15em solid black;
  border-radius: 0.7em;
  display: inline-block;
  margin: 0.7em 0.5em 0.5em 0.5em;
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
#i{
 opacity:0.33;
}
#c{
  /*
  color:black;
  background-color:white;
  background-size: 2.4em 2.9em;
  background-image: url("../assets/c.png");
  border:transparent;
  */
}
</style>
