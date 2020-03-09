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
  },methods:{
   
  }
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
  color: #2c3e50;
  margin-top: 0px;
  overflow: auto;
}
.cline{
  position:absolute;
  background-color: black;
  z-index :-1;
}

</style>
