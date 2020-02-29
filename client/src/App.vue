<template>
  <div id="app">
     <clone ref="clone"></clone>
  </div>
</template>
<script>

import clone from "./components/clone.vue";
export default {
  name: "app",
  components:{
    clone,
  },
  data(){
    return{
    }
  },
  methods: {    
  },
};
</script>

<style>
body {
  background-color: white ;
}
.im {
  text-align: center;
}
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  /*
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  */
  color: #2c3e50;
  margin-top: 0px;
  overflow: auto;
 
  border: 2px dashed black;
}
</style>
