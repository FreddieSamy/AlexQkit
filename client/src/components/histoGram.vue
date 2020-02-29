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
<style scoped>
.histoGram {
  flex:1;
  border: 0.2em solid black;
  padding: 0em 0em 0em 0em;
  margin: 0em 1em 1em 1em;
  border-radius: 0.5em;
  width:45%;
}
.histogram-image{ 
  margin: 0em 0em 0em 0em;
  padding: 0em 0em 0em 0em;
  width:38em; 
}
</style>
