<template>
  <div class="ibmBody">
    <label class="lbl1">IBM Token</label>
    <input class="ibmToken" type="text" name="" placeholder="ibmToken (not working yet)" id="" />
  </div>
</template>
<!-- =============================================================  -->
<script>
export default {
  name: "ibm",
  display: "ibm",
  order: 3
};
</script>
<!-- =============================================================  -->
<style scoped>
.ibmBody {
  /*border: 2px dashed grey;*/
  flex: 1;
  padding: 0.2em 0.2em 0.2em 0.2em;
  margin: 0.2em 0.2em 0.2em 0.2em;
  width: 29%;
}
.lbl1{
  display:block;
}
.ibmToken{
  display:block;
  margin: 0.5em 0.2em 0.2em 0.2em;
}
</style>
