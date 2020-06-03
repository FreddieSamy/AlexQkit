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
  box-sizing: border-box;

}
.cline{
  position: absolute;
  background-color: black;
  z-index :-1;
}
#X , #Y ,#Z{

  background:#306BA2;
}
#○,
#●{

  background:#4390FC;
}
#M{

  background:#C8D82D;
}
#H{

  background:#5E5E8C;
}
#S , #T{

  background:#198C9B;
}
#Sdg , #Tdg{
  font-weight: bold;
  background: #3FB979;
}

#Rx,#Ry,#Rz{
  background:#FF8C61;
}
#Swap , #Reset{
  background:#F15374;
}

</style>
