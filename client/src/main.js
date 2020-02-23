import Vue from "vue";
import App from "./App.vue";
import clone from "./components/clone.vue";
import axios from "axios";

//import BootstrapVue from 'bootstrap-vue';

Vue.config.productionTip = false;

//Vue.use(BootstrapVue);

new Vue({
  methods: {
    data() {
      return {
        info: null
      };
    },
    countWire: function() {
      window.console.log("Vue instance called function by clone component");
      return "nothing to return";
    }
  },
  components: {
    clone
  },
  render: h => h(App),

  mounted() {
    axios
      .get("http://localhost:5000/data", { useCredentials: true })
      .then(res => {
        window.console.log(res);
      });
    /*
    axios.post("http://localhost:5000/mario",{msg:"marioooo"}).then((res)=>{
      window.console.log(res);
    });
    */
  }
}).$mount("#app");
