<template>
  <div class="circiut-loops">
    <div>
      <button @click="openNav();">Add Loop</button>
    </div>
    <div id="myNav1" class="overlay">
      <div class="overlay-body">
        <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>

        <!-- loops  -->

        <h1>Loops</h1>
        <div class="loops">
          <Loop v-for="count in loopCounts" :key="count" :ref="'loops'" />
        </div>
        <div class="loops-btns">
          <button class="add" @click="loopCounts++;">Add</button>
          <button class="remove" v-if="loopCounts" @click="loopCounts--">Remove</button>
          <button class="apply" v-if="loopCounts" @click="applyLoop">Apply the loops</button>
        </div>
        <!-- end loops -->

        <!-- conditional Loop -->

        <div class="conditional-loop">
          <h1>Conditional Loop</h1>
          <label for>Choose Column</label>
          <select v-model="conditionColumn">
            <option v-for="(item, index) in jsonObject.colsCount" :key="index">{{index+1}}</option>
          </select>
          <div>
            <button @click="applyConditionalLoop">Apply Conditional Loop</button>
          </div>
        </div>
        <!-- end conditional Loop -->
      </div>
    </div>
  </div>
</template>
<!-- ================================================  -->
<script>
import Loop from "./Loop.vue";
import { mapState, mapActions } from "vuex";

// eslint-disable-next-line no-undef
export default {
  name: "CircuitLoops",
  display: "CircuitLoops",
  props: ["colsCount"],
  components: { Loop },
  data() {
    return {
      loopCounts: 1,
      ListOfPositions: [],
      Repeats: [],
      conditionColumn: null
    };
  },

  computed: {
    ...mapState(["jsonObject"])
  },
  methods: {
    ...mapActions(["addMessage"]),
    ...mapActions(["removeMessages"]),
    applyLoop() {
      this.removeMessages();
      this.ListOfPositions = [];
      this.Repeats = [];
      for (let i = 0; i < this.loopCounts; i++) {
        let loopCaller = this.$refs.loops[i];
        let arr = [parseInt(loopCaller.from) - 1, parseInt(loopCaller.to) - 1];
        this.ListOfPositions.push(arr);
        this.Repeats.push(parseInt(loopCaller.repeat));
      }
      let listOfPos = this.ListOfPositions;
      let listOfRep = this.Repeats;
      let repeated = { listOfPos, listOfRep };
      // start
      //window.console.log(this.startLessEnd(listOfPos));
      if (this.startLessEnd(listOfPos) === false) {
        alert("Start cannot More than end or unselected");
        return false;
      }
      //window.console.log(this.startLessEnd(listOfRep));
      if (this.checkRepeat(listOfRep) === false) {
        alert("Repeat cannot be less than one or Empty");
        return false;
      }
      //window.console.log(this.overreprsent(listOfPos));
      if(this.overreprsent(listOfPos)===false){
        alert("Cannot accept overlab or unordered loop");
        return false
      }
      //end
      this.jsonObject["repeated"] = repeated; // should be setter
      // let message = {messageType:'advanced',messageBody:repeated}
      this.addMessage({ messageType: "advanced", messageBody: repeated });
      //window.console.log(this.$parent.$parent.jsonObject)
      this.closeNav();
    },
    applyConditionalLoop() {
      if (this.conditionColumn) {
        for (let i = 0; i < this.jsonObject.wires; i++) {
          let wireCaller = this.$parent.$parent.$refs.wire[i];
          wireCaller.addGateByIndex(this.conditionColumn, "loop.*");
        }
        this.$parent.$parent.updateMaxWire();

      }
      this.closeNav();
    },
    openNav() {
      document.getElementById("myNav1").style.width = "25%";
    },
    // ----------------------------------------------------
    closeNav() {
      document.getElementById("myNav1").style.width = "0%";
    },
    startLessEnd(listOfPosition) {
      for (var ele of listOfPosition) {
        if (ele[0] > ele[1] || isNaN(ele[0] || isNaN(ele[1]))) {
          return false;
        }
      }
      return true;
    },

    checkRepeat(listOfRep) {
      for (var ele of listOfRep) {
        if (isNaN(ele) || ele < 1) {
          return false;
        }
      }

      return true;
    },
        overreprsent(listOfPosition){
      for (var i = 0 ; i < listOfPosition.length; i++){
        for(var j = i+1 ; j < listOfPosition.length ; j++){
          if(listOfPosition[i][1] >= listOfPosition[j][0]){
            return false
          }
        }
      }
      return true
    },
  }
};
</script>
<!-- ================================================  -->
<style scoped>
.loops-btns {
  margin: 20px 0px 0px 0px;
}
button {
  border: 2px solid grey;
  margin: 0;
  background: white;
  border-radius: 0.5em;
}

.remove {
  margin: 0px 50px 0px 10px;
}
.overlay-body {
  margin-left: 15px;
  /* border:3px double red; */
}
.overlay {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: rgba(11, 12, 16, 0.8);
  overflow-x: hidden;
  transition: 0.5s;
}

.button_over {
  background: none;
  color: white;
  border: 1px solid white;
}

.overlay a {
  padding: 5px;
  text-decoration: none;
  font-size: 36px;
  color: rgba(255, 255, 255, 0.7);
  display: block;
  transition: 0.3s;
}

.overlay a:hover,
.overlay a:focus {
  color: #f1f1f1;
}

.overlay .closebtn {
  position: absolute;
  top: 20px;
  right: 45px;
  font-size: 30px;
}
div {
  color: white;
}
</style>


