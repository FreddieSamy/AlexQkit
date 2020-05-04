  <template>
  <div>
    <div id="myNav3" class="overlay" style="width:0%">
      <a href="javascript:void(0)"  class="closebtn" @click="closeNav()">&#10006;</a>

      <div class="column">
        <input type="text" id="variables" placeholder="x1,x2,x3" required /> 
        <input type="text" id="booleanfunction"  placeholder="not x1 or x2 and x3" required />
        <br />
        <button >create</button> 
        <!-- @click="createBooleanCircuit()" -->
      </div>

    
    </div>
    <div> 
        <button  @click="openNav()" class=""> Boolean</button>
        
    </div>
  </div>
</template>

<script>

//import axios from "axios";
export default {
  name: "createBoolean",
  display: "createBoolean",
  components: {
 
  },
  data() {
    return {
      // capturedImage: ""
    };
  },
  methods: {
      // createBooleanCircuit(){
      //       axios.post("http://127.0.0.1:5000/booleanExpression", json_object).then(res => {
      //       /*window.console.log(res.data);*/
           
      //     });
      // },
    openNav() {
      document.getElementById("myNav3").style.width = "100%";
     // document.getElementById("variables").value = null;
      //document.getElementById("booleanfunction").value = null;
    },
    // ----------------------------------------------------
    closeNav() {
      document.getElementById("myNav3").style.width = "0%";
      
    },
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
  justify-content:center;
  align-items:stretch;
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


    </style>