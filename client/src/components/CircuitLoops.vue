<template>
  <div class="circiut-loops">
    <div>
          <button @click="loopCounts++">Add Loop</button>
    </div>

    <loop v-for="count in loopCounts" :key="count" :ref="'loops'" ></loop>

    <div>
      <button v-if="loopCounts" @click="applyLoop">Apply Loops</button>
    </div>
    <div>
      <button v-if="loopCounts" @click="loopCounts--">Remove Loop</button>
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
        this.Repeats.push(loopCaller.repeat)
      }

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

</style>


