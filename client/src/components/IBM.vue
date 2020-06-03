<template>
  <div class="ibmBody">
    <div id="hover-div">
      <label class="ibm-label">IBM Token</label>
      <input class="ibmtoken" type="text" id="ibmtextfield" v-model="ibmtoken"/>
      <span id="hover-element">
        <div>Get your API_TOKEN from:</div>
        <div>
          <a id="link" target="_blank" :href="anchor">{{anchor}}</a>
        </div>
        <div>To run your circuit on IBM Q</div>
      </span>
    </div>

    <div>
      <label class="device-label">Device</label>
      <select id="simulater" v-model="device">
        <optgroup v-for="(type,index) in devices" :key="index" :label="index">
          <option
            v-for="device in type"
            :key="device"
            :value="device"
            :selected=" device =='ibmq_16_melbourne' ? true : false "
            :disabled="parseInt(index.slice(0,2))<jsonObject.wires"
          >{{device}}</option>
        </optgroup>
      </select>
    </div>

    <div class="checkbox">
      <input type="checkbox" id="checkbox" v-model="checkboxibm"/>
      <label for="checkbox">Run on IBMQ</label>
      <button @click="sendto()">RUN</button>
    </div>
    <a id="link" target="_blank" :href="this.liveResults.link">{{ this.liveResults.link }}</a>
  </div>
</template>
<!-- =============================================================  -->
<script>
import { ibmLink } from "./../data/routes";
import devices from "./../data/IBM_Devices";
import { mapGetters, mapState } from "vuex";

export default {
  name: "ibm",
  display: "ibm",
  order: 3,
  data() {
    return {
      anchor: ibmLink,
      device: "ibmq_16_melbourne",
      devices: devices,
      ibmtoken:"",
      checkboxibm:false
    };
  },
  computed: {
    ...mapState(["jsonObject"]),
    ...mapGetters(["liveResults"])
  },
  methods: {
    sendto() {
      // validation for ibm 
      this.ibmtoken=this.ibmtoken.replace(/\s/g, "");
      if(this.ibmtoken.length != 64){
        alert("ibmtoken was entered isn't correct");
        }
      var{isempty,msg}=this.inputisempty(this.ibmtoken)

      //
      if (this.checkboxibm && !isempty) {
        this.jsonObject.API_TOKEN = this.ibmtoken;
        
        this.jsonObject.device = this.device;
        if (this.jsonObject.API_TOKEN) {
          this.$parent.runCircuit();
        } else {
          this.$parent.$refs.qasm.sendQasm();
        }
        this.checkboxibm= false;
      }
      else if(isempty){
        alert(msg);

      } 
      else {
        alert("make sure to select the checkbox to run on IBMQ devices");
      }
    },
    // ----------------------------------------------------
    /*
      -inputisempty function : used to check field of input is empty or not 
    */
    inputisempty(valueOfInput) {
      var isempty = false;
      var msg = "";
      if (valueOfInput == "" || valueOfInput.length == 0) {
        isempty = true;
        msg = "you have to fill variables and expression  ";
        return { isempty, msg };
      }
      return { isempty, msg };
    },
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.ibmBody {
  background: white;
  padding: 0px;
  margin: 0.2em 0.2em 0.2em 0.2em;
  border-radius: 10px;
}
.ibmToken {
  margin: 0.5em 0.2em 0.2em 0.2em;
}

.ibm-label {
  margin: 0em 1.1em 0em 0em;
}
.device-label {
  margin: 0em 2em 0em 0em;
}
input {
  border-radius: 5px;
}
select {
  margin: 0.7em;
  border: 1px solid black;
  padding: 0px;
  border-radius: 5px;
  background: white;
}
button {
  border-radius: 7px;

  margin: 0px 0px 0px 15px;
}
#hover-element {
  display: none;
  position: absolute;
  background-color: lightgray;
  padding: 5px;
  border: solid;
  border-radius: 5px;
  transition-delay: 3s;
}
#hover-div:hover #hover-element {
  display: block;
}
</style>
