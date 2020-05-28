<template>
  <div>
    <div>
      <input class="from" type="number" min="1" v-model="from" placeholder="from " /> :
      <input class="to" type="number" min="1" v-model="to" placeholder="to " />
      <input class="repeat" type="number" min="1" v-model="repeat" placeholder="Repeat" />
    </div>
  </div>
</template>
<!-- ================================================  -->
<script>
// eslint-disable-next-line no-undef
export default {
  name: "Loop",
  display: "Loop",
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
  width: 40px;
  border-radius: 5px;
  background: #f3f3f3;
}
.repeat{
  margin:0px 0px 0px 50px;
  width:60px;
}
</style>

