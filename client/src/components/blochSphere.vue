<template>
  <div class="blochSphereGraph">
    <center>
      <img
        src="http://127.0.0.1:5000/blochsphere.png"
        alt="blochSphere"
        id="bloch"
        class="blochsphere-image responsive"
      />
    </center>
  </div>
</template>
<!-- ========================================================== -->
<script>
export default {
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
   max-width:32em;
}
.blochsphere-image{
  margin: 4em 0em 0em 0em;
  padding: 0em 0em 0em 0em;
  height:auto;
  width: auto;
  max-width:35em;
}
</style>
