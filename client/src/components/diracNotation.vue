<template>
  <div class="diracNotation" id="diracNotation">
    <center>
      <h4>Dirac Notation</h4>
      <h4>{{ this.$parent.diracNotationData }}</h4>
    </center>
  </div>
</template>
<!-- =============================================================  -->
<script>
export default {
  name: "diracNotation",
  display: "diracNotation"
};
</script>
<!-- =============================================================  -->
<style scoped>
.diracNotation {
  border: 1px solid black;
  border-radius: 0.5em;
}
</style>
