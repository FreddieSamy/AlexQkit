<template>
<!--
     - this component for custom gate as matrix to make design of matrix and pull
     the data form the inputs
-->
  <div>
    <!--  begin  number of wires  -->
    <div>
      <input type="number" min="1"  max="4" id="wires" v-model="wires" value="1" />
    </div>
    <!--  end number of wires  -->

    <!--  begin  inputs for matrix   -->
    <form id="inputField" role="form"></form>
    <div id="resultField"></div>
    <!--  end   inputs for matrix   -->
  </div>
</template>
<!-- =============================================================  -->
<script>
export default {
  name: "CustomMx",
  display: "CustomMx",

  data() {
    return {
      removeel: [],
      wires: 1
    };
  },
  watch: {
    wires: {
      immediate: true,
      handler() {
        this.$nextTick(() => {
          this.design();
        });
      }
    }
  },
  methods: {
    /* 
      - design function: take input wire and design the shape of matrix
    */
    design() {
      this.clear();
      var wire = this.wires;
      if (wire == 0 || wire == "") {
        alert("number of wire can't be zero");
        this.clear();
        return 0;
      }
      wire = Math.pow(2, wire);

      for (let i = 0; i < wire; i++) {
        var div = document.createElement("div");
        document.getElementById("inputField").appendChild(div);

        for (let k = 0; k < wire; k++) {
          var input = document.createElement("input");
          input.type = "text";
          input.setAttribute("size", "4");
          input.setAttribute("value", 0);
          input.style.padding = '3px';
          input.style.margin = '3px';
          input.style.borderRadius = '8px';
          input.id = "" + i + k;
          this.removeel.push("" + i + k);
          document.getElementById("inputField").appendChild(input);
        }
      }
    },
    // ----------------------------------------------------
     /* 
      - pulldata function: pull the data from the inputs as array
    */
    pulldata() {
      
      var numwires = document.getElementById("wires").value;
      var wire = Math.pow(2, numwires);
      var myArr = document.forms.inputField;
      var name_value_array = [];
      for (var i = 0; i < myArr.length; i++) {
        if (myArr.type != "button") {
          name_value_array.push(myArr[i].value);
        }
      }
      var matrix = this.split(myArr, wire); // the matrix
      return {matrix,numwires};
    },
    // ----------------------------------------------------
    /* 
      - clear function: clear the inputs that user enter value for the gate
    */
    clear() {

      for (let i = 0; i < this.removeel.length; i++) {
        var element = document.getElementById(this.removeel[i]);
        element.remove(element);
      }
      this.removeel = [];
    },
    // ----------------------------------------------------
    /* 
      - split function: take array and convert it to matrix accroding the number of wires
    */
    split(myArray, size) {
      let result = [];
      var count = size;
      var sub = [];

      for (let indx = 0; indx < myArray.length; indx++) {
        sub.push(myArray[indx].value);
        if (count - 1 == indx) {
          result.push(sub);
          sub = [];
          count = count + size;
        }
      }
      return result;
    }
    // ----------------------------------------------------
  }
};
</script>
<!-- =============================================================  -->
<style scoped>
input{
  padding:0px 0px 0px 5px;
  border-radius:10px;
  width:50px;
}
#inputField{
  margin:20px;
}
</style>
