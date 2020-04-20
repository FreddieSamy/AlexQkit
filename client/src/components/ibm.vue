<template>
  <div class="ibmBody">
    <div id="hover-div">
      <label class="ibm-label">IBM Token</label>
      <input class="ibmtoken" type="text" id="ibmtextfield" />
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
          >{{device}}</option>
        </optgroup>
      </select>
    </div>

    <div class="checkbox">
      <input type="checkbox" id="checkbox" />
      <label for="checkbox">Run on IBMQ</label>
      <button @click="sendto()">RUN</button>
    </div>
    <a id="link" target="_blank" :href="link">{{ link }}</a>
  </div>
</template>
<!-- =============================================================  -->
<script>
import { mapState } from "vuex";
export default {
  name: "ibm",
  display: "ibm",
  order: 3,
  data() {
    return {
      anchor: "https://quantum-computing.ibm.com/account",
      link: "",
      device: "ibmq_16_melbourne"
    };
  },
  computed: {
    ...mapState(["devices"])
  },
  methods: {
    sendto() {
      if (document.getElementById("checkbox").checked) {
        this.$parent.jsonObject.API_TOKEN = document.getElementById(
          "ibmtextfield"
        ).value;
        var sim = document.getElementById("simulater");
        this.device = sim.options[sim.selectedIndex].value;
        this.$parent.jsonObject.device = this.device;
        this.$parent.sendSystem();
        document.getElementById("checkbox").checked = false;
      } else {
        alert("make sure to select the checkbox to run on IBMQ devices");
      }
    }
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
