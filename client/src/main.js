import Vue from "vue";
import App from "./App.vue";
import axios from "axios";
import store from './store'

Vue.config.productionTip = false;

new Vue({
  store,
  methods: {
  },
  render: h => h(App),

  mounted() {
    axios
      .get(this.$store.state.routes.serverRoute, { useCredentials: true })
      .then(res => {
        window.console.log("Server Request responds  : "+res.data);
      });
    /*
    axios.post("http://localhost:5000/data",{msg:"marioooo"}).then((res)=>{
      window.console.log(res);
    });
    */
  }
}).$mount("#app");
