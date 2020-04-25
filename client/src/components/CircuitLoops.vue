<template>
  <div class="circiut-loops">
    <div>
      <button @click="openNav();">Add Loop</button>
    </div>
    <div id="myNav1" class="overlay">
      <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>
      <h1>Loops</h1>
      <div class="loops">
        <loop v-for="count in loopCounts" :key="count" :ref="'loops'"></loop>
      </div>
      <div class="loops-btns">
        <button v-if="loopCounts" @click="loopCounts--" class="button_over">Remove Loop</button>
        <button @click="loopCounts++;" class="button_over">Add Loop</button>
        <div>
          <button v-if="loopCounts" @click="applyLoop" class="button_over">Apply Loops</button>
        </div>
      </div>
    </div>
  </div>
</template>
<!-- ================================================  -->
<script>
import loop from "./loop.vue";
// eslint-disable-next-line no-undef
export default {
  name: "CircuitLoops",
  display: "CircuitLoops",
  props: ["maxWire"],
  components: { loop },
  data() {
    return {
      loopCounts: 1,
      ListOfPositions: [],
      Repeats: []
    };
  },

  computed: {},
  methods: {
       applyLoop() {
      this.ListOfPositions = [];
      this.Repeats = [];
      for (let i = 0; i < this.loopCounts; i++) {
        let loopCaller = this.$refs.loops[i];
        let arr = [parseInt(loopCaller.from), parseInt(loopCaller.to)];
        this.ListOfPositions.push(arr);
        this.Repeats.push(parseInt(loopCaller.repeat));
        this.closeNav();
      }
      let listOfPos = this.ListOfPositions;
      let listOfRep = this.Repeats;
      let repeated = { listOfPos, listOfRep };
      this.$parent.$parent.jsonObject["repeated"] = repeated;
      //window.console.log(this.$parent.$parent.jsonObject)
    },
    openNav() {
      document.getElementById("myNav1").style.width = "30%";
    },
    // ----------------------------------------------------
    closeNav() {
      document.getElementById("myNav1").style.width = "0%";
    },
    hey() {
      window.console.log("hey");
    }
  }
};
</script>
<!-- ================================================  -->
<style scoped>
.loops {
  margin: 100px 0px 0px 0px;
}
.loops-btns {
  margin: 5px 10px 10px -50px;
  text-align: center;
}
button {
  border-radius: 7px;
  background-color: white;
  margin: 0em;
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
  margin-left: 30px;
  background: none;
  color: white;
  border: 1px solid white;
  font-size: 15px;
  margin-top: 10px;
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
div{
  color:white
}
</style>


