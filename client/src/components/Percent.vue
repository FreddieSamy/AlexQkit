<template>
  <div>
    <svg>
      <rect width="100%" height="100%" stroke="black" stroke-width="1" fill="white" />
      <rect :y="(100-this.probability)+'%'" width="100%" :height="this.probability+'%'" fill="#318BD2" rx="0" />
      <text
        x="50%"
        y="50%"
        font-size="10"
        text-anchor="middle"
        alignment-baseline="central"
      >{{this.probability}}%</text>
    </svg>
  </div>
</template>
<!-- =============================================================  -->
<script>
import { mapGetters } from "vuex";
export default {
  name: "Percent",
  display: "Percent",
  props: ["probability"],
  data() {
    return {};
  },
  computed: {
    ...mapGetters(["liveResults"]),
  },
};
</script>
<!-- =============================================================  -->
<style scoped>
div {
  display: flex;
  margin: 0px 20px 0px 0px;
}
svg {
  text-align: center;
  width: 35px;
  height: 35px;
  transition: transform 0.2s;
}
svg:hover {
  transform: scale(2.5);
}
</style>
