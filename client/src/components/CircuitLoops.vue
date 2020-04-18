<template>
  <div class="circiut-loops">
    
    
    <div >
          <button @click="loopCounts++; openNav();">make Loop</button>
    </div>
<div id="myNav1" class="overlay">
  <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>
  
  
    <loop v-for="count in loopCounts" :key="count" :ref="'loops'" ></loop>

    <div>
      <button v-if="loopCounts" @click="applyLoop" class="button_over" >Apply Loops</button>
    
    
      <button v-if="loopCounts" @click="loopCounts--" class="button_over" >Remove Loop</button>
      <button @click="loopCounts++;" class="button_over">Add Loop</button>
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
  components:{loop},
  data() {
    return {
      loopCounts:0,
      ListOfPositions:[],
      Repeats:[]
    };
  },

  computed: {
    
  },
  methods: {
    applyLoop(){
      this.ListOfPositions=[]
      this.Repeats=[]
      for (let i = 0; i < this.loopCounts; i++) {
        let loopCaller = this.$refs.loops[i];
        let arr = [ loopCaller.from, loopCaller.to ]
        this.ListOfPositions.push(arr);
        this.Repeats.push(loopCaller.repeat);
        this.closeNav();
      }

    },
     openNav() {
       document.getElementById("myNav1").style.width = "30%";
      
    },
    // ----------------------------------------------------
     closeNav() {
       document.getElementById("myNav1").style.width = "0%";
    
     },
     hey(){
       window.console.log("hey")
     }
  }
};
</script>
<!-- ================================================  -->
<style scoped>
/*
@import url("./../../node_modules/nouislider/distribute/nouislider.min.css");
*/

button{
  border-radius: 7px;
  background-color: white;
  margin:0em 0em 0.5em 0em;
  
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

.button_over{
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

</style>


