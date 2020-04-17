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
  background: #F1F2F1;
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
#s{
  font-weight: bold;
  background:#8BD7D2;
}
#t{
  font-weight: bold;
  background:#8BD7D2;
}
</style>
