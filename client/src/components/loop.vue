<template>
  <div>
    <div>
      <input type="number" min="1" v-model="from" placeholder="from " />
      <label>:</label>
      <input type="number" min="1" v-model="to" placeholder="to " />
      <label>-></label>
      <input type="number" min="1" v-model="repeat" placeholder="Repeat" />
    </div>
  </div>
</template>
<!-- ================================================  -->
<script>
// eslint-disable-next-line no-undef
export default {
  name: "loop",
  display: "loop",
  data() {
    return {
      from: "from",
      to: "to",
      repeat: "repeat"
    };
  }
};
</script>
<!-- ================================================  -->
<style scoped>
input {
  padding: 0em 0em 0em 0.5em;
  width: 60px;
  border-radius: 5px;
  margin:1em;
}
</style>

