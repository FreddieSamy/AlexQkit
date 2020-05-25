<template>
  <div>
    <div>
      <input type="number" min="1"  max="4" id="wires" v-model="wires" value="1" />
    </div>
    <form id="inputField" role="form"></form>
    <!--
    <input
      type="button"
      @click="design()"
      value="design"
      name="design"
      
    />
    -->
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
    design() {
      this.clear();
      //var wire = document.getElementById("wires").value;
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
          input.setAttribute("placeholder", "1.0+3.5i");
          input.style.padding = '3px';
          input.style.margin = '3px';
          input.style.borderRadius = '8px';
          input.id = "" + i + k;

          this.removeel.push("" + i + k);
          document.getElementById("inputField").appendChild(input);
        }
      }
    },
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
      var matrix = this.split(myArr, wire);

      return {matrix,numwires};
    },

    clear() {

      for (let i = 0; i < this.removeel.length; i++) {
        var element = document.getElementById(this.removeel[i]);

        element.remove(element);

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
input{
  padding:0px 0px 0px 5px;
  border-radius:10px;
  width:50px;
}
#inputField{
  margin:20px;
}
</style>
