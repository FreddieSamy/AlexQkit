<template>
  <div class="histoGram">
      <img
      src="http://127.0.0.1:5000/chart.png"
      alt="histogram"
      id="chart"
      class="histogram-image responsive"
      />
  </div>
</template>
<!-- ========================================================== -->
<script>
export default {
  }
</script>
<!-- ========================================================== -->
<style scoped>
.histoGram {
  flex:1;
  border: 0.05em solid black;
  padding: 0em 0em 0em 0em;
  margin: 0em 0em 0em 1em;
  border-radius: 0.5em;

}
.histogram-image{
  margin: 4em 0em 0em 0em;
  padding: 0em 0em 0em 0em;
  height:auto;
  width: auto;
  max-width:35em;
}
</style>
