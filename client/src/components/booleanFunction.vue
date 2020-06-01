  <template>
  <div class="boolean-function">
    <div id="myNav3" class="overlay" style="width:0%">
      <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>

      <div class="column">
        <h1>Boolean function</h1>
        <h3>variables</h3>
        <input type="text" id="variables" placeholder="x,y,z" required v-model="variables"/>
        <h3>expression</h3>
        <input type="text" id="booleanfunction" placeholder="(x or y) and not z" required  v-model="expression"/>
        <h3>wires indices</h3>
        <input type="text" id="indices" placeholder="0,1,4" />
        <button @click="createBooleanCircuit()">create</button>
        <!-- @click="createBooleanCircuit()" -->
      </div>
    </div>
    <div>
      <button @click="openNav()" class>Boolean Function</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "createBoolean",
  display: "createBoolean",
  components: {},
  data() {
    return {
      // capturedImage: ""
      variables:"",
      expression:""
    };
  },
  methods: {
      /* 
      - still working on it's validtion.
    */
    createBooleanCircuit() {
      var variablesToValidate=this.variables.split(",")
      window.console.log(variablesToValidate);
      //var reqexToVariables=/""/
      
      var indices = document.getElementById("indices").value.split(",");
     // window.console.log(variables);
      //window.console.log(booleanfunction);
      //window.console.log(indices);
      axios
        .post("http://127.0.0.1:5000/booleanExpression", {
          vars: this.variables,
          fn: this.expression,
          indices: indices
        })
        .then(res => {
          //window.console.log(res.data);
          // window.console.log(this.$parent.$parent.jsonObject);
          this.$parent.$parent.setAlgorithm(res.data
            //  ,true, {names: variables.split(","),positions: indices}
          );
        });
      this.closeNav();
    },
    openNav() {
      document.getElementById("myNav3").style.width = "100%";
      // document.getElementById("variables").value = null;
      //document.getElementById("booleanfunction").value = null;
    },
    // ----------------------------------------------------
    closeNav() {
      document.getElementById("myNav3").style.width = "0%";
    }
  }
};
</script>
<style scoped>
.overlay {
  height: 100%;
  top: 0;
  left: 0;
  position: fixed;
  z-index: 1;
  background-color: rgba(103, 106, 97, 0.55);
  overflow-x: hidden;
  transition: 0.5s;
  display: flex;
  justify-content: center;
  align-items: stretch;
  flex-wrap: wrap;
}
.overlay a {
  padding: 8px;
  text-decoration: none;
  font-size: 36px;
  color: rgba(255, 255, 255, 0.7);
  display: block;
  transition: 0.3s;
}

.overlay a:hover,
.overlay a:focus {
  color: #f1f1f1;
}

.overlay .closebtn {
  position: absolute;
  top: 20px;
  right: 45px;
  font-size: 30px;
}

@media screen and (max-height: 450px) {
  .overlay a {
    font-size: 20px;
  }
  .overlay .closebtn {
    font-size: 40px;
    top: 15px;
    right: 35px;
  }
}
button {
  display: inline-block;
  margin: 0em 0.2em 0em 0.2em;
  padding: 0.1em 0.5em 0.1em 0.5em;
  background-color: white;
  border-radius: 0.5em;
  border: 2px solid grey;
}
input {
  display: block;
  margin-top: 25px;
}
.column {
  background: rgb(47, 68, 85, 0.7);
  margin: 3em;
  padding: 1em;
  border-radius: 1em;
  display: table-column;
}

div {
  color: white;
}
</style>