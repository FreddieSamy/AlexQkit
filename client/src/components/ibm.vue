<template>
  <div class="ibmBody" >
    <div id="hover-div">
    <label class="lbl1">IBM Token</label>
    <span id="hover-element">
            Go to ibm and copy the token then place it in the box.
        </span>
    </div>
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
