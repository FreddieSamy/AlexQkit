<template>
  <div class="ibmBody">
    <div id="hover-div">
      <label class="lbl1">IBM Token</label>
      <span id="hover-element">
        Get your API_TOKEN from
        <a
          id="link"
          target="_blank"
          href="https://quantum-computing.ibm.com/account"
          >https://quantum-computing.ibm.com/account</a
        >
        <br />To run your circuit on IBM Q
      </span>
    </div>
    <input class="ibmtoken" type="text" id="ibmtextfield" />
    <!-- <div>
    <label class="lbl1">number of shots</label>
    <input class="ibmToken" type="text" />
    </div>-->
    <div class="checkbox">
      <input type="checkbox" id="checkbox" /><label for="checkbox"
        >Run on IBMQ</label
      >
    </div>
    <div>
      <button @click="save_ibm_token()">Send</button>
    </div>
    <a id="link" target="_blank" :href="link">{{ link }}</a>
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
  data() {
    return { link: "" };
  },
  methods: {
    save_ibm_token() {
      this.$parent.API_TOKEN = document.getElementById("ibmtextfield").value;
      this.$parent.sendSystem();
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
  /*display: block;*/
}
.lbl1 {
  display: block;
}
.ibmToken {
  display: block;
  margin: 0.5em 0.2em 0.2em 0.2em;
}
.checkbox {
  display: block;
}
#hover-element {
  display: none;
  position: absolute;
  background-color: lightgray;
  padding: 10px;
  border: solid;
  border-radius: 5px;
}

#hover-div:hover #hover-element {
  display: block;
}
</style>
