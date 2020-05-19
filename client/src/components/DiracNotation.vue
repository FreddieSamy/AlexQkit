<template>
  <div class="DiracNotation" id="diracNotation">
    <p class="dirac-label">Dirac Notation :</p>
    <p class="dirac-value">{{this.liveResults.diracNotation}}</p>
  </div>
</template>
<!-- =============================================================  -->
<script>
import { mapGetters } from "vuex";

export default {
  name: "DiracNotation",
  display: "DiracNotation",
  computed: {
    ...mapGetters(["liveResults"])
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.DiracNotation {
  border: 2px solid #aaaaaa;
  border-radius: 10px;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  width: 100%;
}
.dirac-label {
  flex-basis: 7%;
  font-weight: bolder;
}
.dirac-value {
  flex-basis: 30%;
  background: lightgray;
  padding: 2px 10px 2px 10px;
}
p {
  border-radius: 10px;
  margin: 5px;
}
</style>
