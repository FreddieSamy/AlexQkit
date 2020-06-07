  <template>
  <div class="boolean-function">
    <div id="myNav3" class="overlay" style="width:0%">
      <a href="javascript:void(0)" class="closebtn" @click="closeNav()">&#10006;</a>

      <div class="column">
        <h1>Boolean function</h1>
        <h3>variables</h3>
        <input type="text" id="variables" placeholder="x,y,z" required v-model="variables" />
        <h3>expression</h3>
        <input
          type="text"
          id="booleanfunction"
          placeholder="(x or y) and not z"
          required
          v-model="expression"
        />
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
      variables: "",
      expression: ""
    };
  },
  methods: {
    /* 
      - still working on it's validtion.
    */
    createBooleanCircuit() {
      
      var indices = document.getElementById("indices").value.split(",");
      var variablesToValidate = this.variables.split(",");
       
      var {
        variablesValidate,
        msgVar,
        dictionaryOfVariables
      } = this.ValidatevariableFn(this.variables);

      var { ValidateExpression, msgEx } = this.ValidateExpressionFnAndIndices(
        this.expression,
        dictionaryOfVariables,
        indices
        
      );
        if (variablesValidate && ValidateExpression) {
           axios.post("http://127.0.0.1:5000/booleanExpression", {
          vars: this.variables,
          fn: this.expression,
          indices: indices
        })
        .then(res => {
          window.console.log(indices);
          if (indices[0] == "") {
            indices = [...Array(variablesToValidate.length + 1).keys()];
            window.console.log(indices);
          }

          //convert variables names to wires names
          var name = this.expression;
          for (let i = 0; i < variablesToValidate.length; i++) {
            name = name.replace(variablesToValidate[i], "q" + indices[i]);
          }
          name = "q" + indices[indices.length - 1] + "=" + name;
          window.console.log(res.data);
          var algorithmObject = { name: name, circuit: res.data };
          this.$parent.$parent.setAlgorithm(algorithmObject, true);
        });
      this.closeNav();
        }
      else {
        if (msgVar == "") {
          alert(msgEx);
        } else {
          alert(msgVar);
        }
      }
    },
    openNav() {
      document.getElementById("myNav3").style.width = "100%";
      // document.getElementById("variables").value = null;
      //document.getElementById("booleanfunction").value = null;
    },
    // ----------------------------------------------------

     ValidatevariableFn(variables) {
      // this.variables=this.variables.replace(/\s/g, "");
      var variablesValidate = true;
      var dictionaryOfVariables = {};
      var msgVar = "";
      var arrayofvariables;
      var regex = /^[a-z A-Z]+([0-9]+)?$/;
      arrayofvariables = variables.split(",");
      window.console.log(arrayofvariables);

      // check if the variables input is empty
      var { isempty, msg } = this.inputisempty(variables);
      if (isempty == true) {
        msgVar = msg;
        variablesValidate = false;
        return { variablesValidate, msgVar, dictionaryOfVariables };
      }

      //check the value of the variable is only string and number
      for (let indx in arrayofvariables) {
        arrayofvariables[indx] = arrayofvariables[indx].replace(/\s/g, "");
        variablesValidate = regex.test(arrayofvariables[indx]);

        if (arrayofvariables[indx] == "") {
          msgVar = "check if you duplicate comma (,,)";
          return { variablesValidate, msgVar, dictionaryOfVariables };
        } else if (variablesValidate == false) {
          msgVar =
            "check the value of this element " +
            "( " +
            arrayofvariables[indx] +
            " )";
          return { variablesValidate, msgVar, dictionaryOfVariables };
        }
      }
      // check the dublicate of variables
      for (let indx in arrayofvariables) {
        if (!(arrayofvariables[indx] in dictionaryOfVariables)) {
          dictionaryOfVariables[arrayofvariables[indx]] = 1;
        } else {
          msgVar = "dublicate of variables";
          variablesValidate = false;
          return { variablesValidate, msgVar, dictionaryOfVariables };
        }
      }

      return { variablesValidate, msgVar, dictionaryOfVariables };
    },
    // ----------------------------------------------------
     /*
      -ValidateExpressionFnAndIndices function : used to check that the expression and indices is 
       correct or not 
    */
    ValidateExpressionFnAndIndices(expression, dicvar,indices) {
      window.console.log(dicvar);
      var ValidateExpression = true;
      var msgEx = "";

      // check empty
      var { isempty, msg } = this.inputisempty(expression);
      if (isempty == true) {
        msgEx = msg;
        ValidateExpression = false;
        window.console.log(ValidateExpression);
        return { ValidateExpression, msgEx };
      }

      // to check bracket ()
      expression = expression.replace(/\s/g, "");
      var regex = /^([a-z A-Z]+([0-9]+)?)?\([a-z A-Z]+([0-9]+)?\)+([a-z A-Z]+([0-9]+)?)?$|^[a-z A-Z]+([0-9]+)?$/;
      ValidateExpression = regex.test(expression);
      if (ValidateExpression == false) {
        msgEx = "please,check the brackets";
        return { ValidateExpression, msgEx };
      }
      
      // check the strings in the expression
      expression = expression.split(/\s|\(|\)|or|and|not/);
      expression = expression.filter(arr => arr); //check if the expression (array) contain empty string and delete it
      for (let indx in expression) {
        if (!(expression[indx] in dicvar)) {
          ValidateExpression = false;
          msgEx =
            " the variable " +
            "( " +
            expression[indx] +
            " )" +
            "undefined in variales !";
          return { ValidateExpression, msgEx };
        } else {
          dicvar[expression[indx]] = 0;
        }
      }
      
      // check if any variable user didn't use it in expression .
      for (let indx in dicvar) {
        if (dicvar[indx] == 1) {
          ValidateExpression = false;
          msgEx =
            " the variable " +
            "( " +
            indx+
            " )" +
            "you didn't use it ";
          return { ValidateExpression, msgEx };
        }
      }
     
     
     if(ValidateExpression ==false && msg !=""){
       return { ValidateExpression, msgEx };
     }
      //----
     //check the indeces is integer or not
     else{

       // if the indices are empty it's okay 
       isempty,msg=this.inputisempty("indices");
       if (isempty== false){
          
         return { ValidateExpression, msgEx };
         
       }
      // window.console.log(this.inputisempty("indices"));
       regex=/^\d$/;
       for(let indx in indices){
         if(indices[indx]==""){
           msgEx="check the indices";
           ValidateExpression=false;
           return{ValidateExpression, msgEx};
         }

         ValidateExpression=regex.test(indices[indx]);
        if(ValidateExpression ==false){
           msgEx =
            " check  " +
            "( " +
            indices[indx] +
            " )" +
            " !";
            return{ValidateExpression, msgEx};
        }
       }
       return{ValidateExpression, msgEx};
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