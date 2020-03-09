<template>
  <div class="ibmBody">
     <div style="float:right">
      <label class="lbl1">number of shots</label>
      <input class="ibmToken" type="number" placeholder="1024" id="numberofshots" />
    </div>
    <div id="hover-div">
      <label class="lbl1">IBM Token</label>
      <span id="hover-element">
        Get your API_TOKEN from:
        <br />
        <a
          id="link"
          target="_blank"
          href="https://quantum-computing.ibm.com/account"
        >https://quantum-computing.ibm.com/account</a>
        <br />To run your circuit on IBM Q
      </span>
    </div>
    <input class="ibmtoken" type="text" id="ibmtextfield" />

<div>
      <label class="lbl1">simulator</label>
    </div>
    <div>
      <select id="simulater" style="width:37%;">
        <option value=''>Please choose device</option>
        <optgroup label="1 qubit">
          <option value="ibmq_armonk">ibmq_armonk</option>
        </optgroup>
        <optgroup label=" 5 qubits">
          <option value="ibmq_london">ibmq_london</option>
          <option value="ibmq_burlington">ibmq_burlington</option>
          <option value="ibmq_essex">ibmq_essex</option>
          <option value="ibmq_ourense">ibmq_ourense</option>
          <option value="ibmq_vigo">ibmq_vigo</option>
          <option value="ibmq_5_yorktown">ibmq_5_yorktown</option>
        </optgroup>
        <optgroup label="15 qubits">
          <option value="ibmq_16_melbourne">ibmq_16_melbourne</option>
        </optgroup>

        <optgroup label="up to 32 qubits">
          <option value="ibmq_qasm_simulator">ibmq_qasm_simulator</option>
        </optgroup>
      </select>
    </div>
    


    
    <div class="checkbox">
      <input type="checkbox" id="checkbox" />
      <label for="checkbox">Run on IBMQ</label>
    </div>
    <div>
      <button @click="snedto()">Send</button>
    </div>
    <a id="link" :href="link">{{ link }}</a>
    <a id="link" target="_blank" :href="link">{{ link }}</a>
    
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
    snedto() {
      this.$parent.API_TOKEN = document.getElementById("ibmtextfield").value;
      
      var sim = document.getElementById("simulater");
      window.console.log(sim.options[sim.selectedIndex].value);
      this.$parent.device = sim.options[sim.selectedIndex].value;
      this.$parent.sendSystem();
      
    },
     returnshots(){
      if(document.getElementById("numberofshots").value==""){
        document.getElementById("numberofshots").value=1024;
      }
    return (document.getElementById("numberofshots").value);
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
