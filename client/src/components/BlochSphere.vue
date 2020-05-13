<template>
  <div class="bloch-sphere">
    <img :src="defaultBlockSphereRoute" :id="'bloch-sphere-'+this.$parent.id" style="width:2.5em;" />
  </div>
</template>
<!-- =============================================================  -->

<script>
import { defaultBlockSphereRoute } from "./../data/routes";

export default {
  name: "BlochSphere",
  display: "BlochSphere",
  data() {
    return {
      defaultBlockSphereRoute: defaultBlockSphereRoute + "/" + this.$parent.id
    };
  },
  mounted() {}
};
</script>
<!-- =============================================================  -->

<style scoped>
</style>