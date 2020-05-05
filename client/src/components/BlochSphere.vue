<template>
  <div>
    <img src="../assets/b.png" alt="">
  </div>
</template>
<!-- =============================================================  -->
<script>

export default {
  name: "BlochSphere",
  display: "BlochSphere",
  components: {},
  //props: ["percent"],
  data(){
     return {   
         
     }
  },
  computed:{
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
div {


  display: flex;
  transition: transform .2s;
  z-index: 0;
}
img {
  width:50px;
}

div:hover{
  transform: scale(3);
  z-index: 2;
}
svg{
    text-align: center;
}
</style>
