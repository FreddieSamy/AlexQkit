<template>
  <div>
    <div>
      <input type ="number" v-model="from" placeholder="from"/>
      <label> : </label>
      <input type="number"  v-model="to" placeholder="to" />
       <label> -> </label>
      <input type="number"  v-model="repeat" placeholder="Repeat" />
    </div>
  
  </div>
</template>
<!-- ================================================  -->
<script>
// eslint-disable-next-line no-undef
export default {
  name: "loop",
  display: "loop",
  //props: ["maxWire"],
  data() {
    return {
      from:'from',
      to:'to',
      repeat:'repeat'
    };
  },

  computed: {},
  methods: {}
};
</script>
<!-- ================================================  -->
<style scoped>
input{
  padding: 0em 0em 0em 0.5em;
  width:60px;
  border-radius: 5px;
  margin-top: 100px;
  margin-left: 40px;
}
</style>

