<template>
  <div id="app">
     <Clone ref="clone" />
  </div>
</template>
<script>
import Clone from "./components/Clone.vue";
export default {
  name: "app",
  components:{
    Clone,
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
  /*overflow: auto;*/
}
.cline{
  position:absolute;
  background-color: black;
  z-index :-1;
}
#x , #y ,#z{
  font-weight: bold;
  background:#306BA2;
}
#c, #oc{
  font-weight: bold;
  background:#4390FC;
}
#m{
  font-weight: bold;
  background:#C8D82D;
}
#h{
  font-weight: bold;
  background:#5E5E8C;
}
#s , #t{
  font-weight: bold;
  background:#198C9B;
}
#sdg , #tdg{
  font-weight: bold;
  background: #3FB979;
}

#rx,#ry,#rz{
  font-weight: bold;
  background:#FF8C61;
}
#swap , #reset{
  font-weight: bold;
  background:#F15374;
}

</style>
