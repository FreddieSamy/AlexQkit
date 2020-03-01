<template>
  <div class="circuitDrawing">
    <center>
      <img
        src="http://127.0.0.1:5000/circuit.png"
        alt="circuitDrawing"
        id="circuitDrawing"
        class="circutDrawing-image responsive"
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
.circuitDrawing {
  flex:1;
  border: 0.05em solid black;
  padding: 0em 0em 0em 0.1em;
  margin:  0em 0em 0em 0em;
  border-radius: 0.5em;
}
.circuitDrawing-image{
  margin: 4em 0em 0em 0em;
  padding: 0em 0em 0em 0em;
  height:auto;
  width: auto;
  max-width:35em;
}
</style>
