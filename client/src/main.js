import Vue from "vue";
import App from "./App.vue";
import axios from "axios";

Vue.config.productionTip = false;

new Vue({
  methods: {
  },
  render: h => h(App),

  mounted() {
    axios
      .get("http://localhost:5000/", { useCredentials: true })
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
