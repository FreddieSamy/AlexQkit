<template>
  <div class="ibmBody">
    <div id="hover-div">
      <label class="lbl1">IBM Token</label>
      <span id="hover-element">
        <div>Get your API_TOKEN from:</div>
        <div>
          <a id="link" target="_blank" :href="anchor">{{anchor}}</a>
        </div>
        <div>To run your circuit on IBM Q</div>
      </span>
    </div>
    <input class="ibmtoken" type="text" id="ibmtextfield" />
    <div>
      <label>Device</label>
      <select id="simulater" v-model="device">
        <optgroup v-for="(type,index) in devices" :key="index" :label="index">
          <option
            v-for="device in type"
            :key="device"
            :value="device"
            :selected=" device =='IBMQ_16_melbourne' ? true : false "
          >{{device}}</option>
        </optgroup>
      </select>
    </div>

    <div class="checkbox">
      <input type="checkbox" id="checkbox" />
      <label for="checkbox">Run on IBMQ</label>
      <button @click="sendto()">Send</button>
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
      device: "IBMQ_16_melbourne"
    };
  },
  computed: {
    ...mapState(["devices"])
  },
  methods: {
    sendto() {
      /*  all of this can be optimized */
      this.$parent.API_TOKEN = document.getElementById("ibmtextfield").value;
      var sim = document.getElementById("simulater");
      window.console.log(sim.options[sim.selectedIndex].value);
      this.$parent.device = sim.options[sim.selectedIndex].value;
      this.$parent.sendSystem();
    },
    returnshots() {
      if (document.getElementById("numberofshots").value == "") {
        document.getElementById("numberofshots").value = 1024;
      }
      return document.getElementById("numberofshots").value;
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
.ibmBody {
  background: white;
  border:1px solid black;
  padding: 0.2em 0.2em 0.2em 0.2em;
  margin: 0.2em 0.2em 0.2em 0.2em;
  border-radius:10px;
}
.ibmToken {
  display: block;
  margin: 0.5em 0.2em 0.2em 0.2em;
}
.checkbox {
  display: block;
}
input {
  border-radius: 5px;
}
select {
  margin: 1em;
  border: 1px solid black;
  padding: 1px;
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
  padding: 10px;
  border: solid;
  border-radius: 5px;
  transition-delay: 3s;
}
#hover-div:hover #hover-element {
  display: block;
}
</style>
