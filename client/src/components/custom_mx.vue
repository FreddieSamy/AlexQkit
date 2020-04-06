<template>
  <div>
    <div>
      <input type="text" id="wires" />
    </div>
    <form id="inputField" role="form"></form>
    <input
      type="button"
      @click="design()"
      value="design"
      name="design"
      
    />
    <!-- <input type="button" @click="pulldata()" value="pulldata" name="pulldata"  /> -->
    <!-- <input type="button" @click="clear()" value="clear" name="clear"  /> -->
    <div id="resultField"></div>
  </div>
</template>
<!-- =============================================================  -->
<script>
export default {
  name: "CustomMx",
  display: "CustomMx",

  data() {
    return {
      removeel: []
    };
  },
  methods: {
    design() {
      this.clear();
      var wire = document.getElementById("wires").value;
      
      if(wire==0||wire==""){
      
      alert("number of wire can't be zero");
      this.clear();
      return 0;
      }
      wire = Math.pow(2, wire);
      window.console.log(wire);
      for (let i = 0; i < wire; i++) {
        var div = document.createElement("div");
        document.getElementById("inputField").appendChild(div);

        for (let k = 0; k < wire; k++) {
          var input = document.createElement("input");
          input.type = "text";
          input.setAttribute("size", "3");
          // input.style = ("border-radius: 70px;");
          input.id = ""+i+k;
         // window.console.log(input.id);
          this.removeel.push(""+i+k);
          document.getElementById("inputField").appendChild(input);
        }
      }
      
    },
    pulldata() {
      var wire = document.getElementById("wires").value;
      wire = Math.pow(2, wire);
      var myArr = document.forms.inputField;
      var name_value_array = [];
      for (var i = 0; i < myArr.length; i++) {
        if (myArr.type != "button") {
          name_value_array.push(myArr[i].value);
        }
      }
      var matrix = this.split(myArr, wire);
     // window.console.log("this");
      //window.console.log(matrix);
      // show map values as a popup
      //window.console.log(name_value_array.map(Number));
      return matrix;
    },

    clear() {
      //window.console.log(this.removeel);
      for (let i = 0; i < this.removeel.length; i++) {
        var element = document.getElementById(this.removeel[i]);
      //  window.console.log(element);
        element.remove(element);
       // window.console.log(this.removeel);
      }
      this.removeel = [];
     // document.getElementById("wires").value=null;

    },

    split(myArray, chunk_size) {
      let results = [];
      var count = chunk_size;
      var sub = [];

      for (let i = 0; i < myArray.length; i++) {
        sub.push(myArray[i].value);
        if (count - 1 == i) {
          results.push(sub);
          sub = [];
          count = count + chunk_size;
        }
      }

      return results;
    }
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
</style>
