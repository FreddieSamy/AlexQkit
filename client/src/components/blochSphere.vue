<template>
  <div class="blochSphereGraph">
    <center>
      <img
        :src="defaultBlockSphereRoute"
        alt="blochSphere"
        id="bloch"
        class="blochsphere-image responsive"
      />
    </center>
  </div>
</template>
<!-- ========================================================== -->
<script>
import {defaultBlockSphereRoute} from './../data/routes'
export default {
  data(){
    return{
      defaultBlockSphereRoute : defaultBlockSphereRoute
    }
  }
}
</script>
<!-- ========================================================== -->
<style scoped>
.blochSphereGraph {
  flex:1;
  border: 0.05em solid black;
  padding: 0em 0em 0em 0.1em;
  margin:  0em 0em 0em 0em;
  border-radius: 0.5em;
}
.blochsphere-image{
  margin: 4em 0em 0em 0em;
  padding: 0em 0em 0em 0em;
  height:auto;
  width: auto;
  max-width:35em;
}
</style>
