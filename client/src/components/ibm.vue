<template>
  <div class="ibmBody">
    <label class="lbl1">IBM Token</label>
    <input class="ibmtoken" type="text" id="ibmtextfield" />
    <!-- <div>
    <label class="lbl1">number of shots</label>
    <input class="ibmToken" type="text" />
    </div>-->
    <div>
      <button @click="save_ibm_token()">save</button>
    </div>
    <!-- <div>
    <label class="lbl1">simulator</label>
    <input class="ibmToken" type="text"/>
    </div>-->
  </div>
</template>
<!-- =============================================================  -->
<script>
export default {
  name: "ibm",
  display: "ibm",
  order: 3,
  methods: {
    save_ibm_token() {
      this.$parent.API_TOKEN = document.getElementById("ibmtextfield").value;
      //   //   //window.console.log(ibmtext);
      // return ibmtext;
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.ibmBody {
  /*border: 2px dashed grey;*/
  padding: 0.2em 0.2em 0.2em 0.2em;
  margin: 0.2em 0.2em 0.2em 0.2em;
  width: 29%;
  float: right;
}
.lbl1 {
  display: inline-block;
}
.ibmToken {
  display: inline-block;
  margin: 0.5em 0.2em 0.2em 0.2em;
}
</style>
