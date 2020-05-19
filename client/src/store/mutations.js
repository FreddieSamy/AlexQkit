
import axios from "axios";
import { appRoute, defaultBlochSphereRoute } from "../data/routes"


export default {

  // Setters
  setCols: (state, count) => { state.jsonObject.colsCount = count; },
  setExe: (state, count) => { state.jsonObject.exeCount = count; },
  setRow: (state, { qstate, list, idx }) => {
    state.jsonObject.init[idx] = qstate;
    state.jsonObject.rows[idx] = list;
  },
  setResult: (state, data) => {
    state.results.chart = data.chart
    state.results.diracNotation = data.diracNotation
    state.results.link = data.link
    state.results.matrixRepresentation = data.matrixRepresentation
    state.results.qasm = data.qasm
    state.results.qasmError = data.qasmError
  },


  // Appenders Functions
  appendInit: state => state.jsonObject.init.push("0"),
  appendWire: state => state.jsonObject.wire++,


  // Remove Functions
  removeInit: state => state.jsonObject.init.pop(),
  removeWire: (state) => {
    state.jsonObject.wire--;
    state.jsonObject.rows.pop();
  },

  // Reset System
  reset: (state) => {
    state.jsonObject.maxWire = 0;
    state.jsonObject.exeCount = 0;
    state.jsonObject.wires = 2;
    state.jsonObject.init = ['0', '0'];
    state.jsonObject.rows = [[], []];
  },


  //Check for in every Column there is an even numbers of swaps
  swapConstrains:(state)=>{
        for( let col = 0 ; col < state.jsonObject.exeCount ; col++ ){
          let count = 0;
          for( let row = 0 ; row < state.jsonObject.wires ; row++ ){
            if(state.jsonObject.rows[row][col] === 'swap'){count++}
          }
          if(count%2 != 0 ){window.console.log("odd number of swaps at col "+col)}
        }
  },


  // Server Functions
  sendCircuit: (state) => {
    try {
      window.console.log(state.jsonObject)
      axios.post(appRoute, state.jsonObject).then(
        res => {
          state.results = res.data;
          //update blochSphere images
          var i;
          for (i = 1; i <= state.jsonObject.wires; i++) {
            var imgofblochSphere = document.getElementById("bloch-sphere-" + i);
            imgofblochSphere.src =
              defaultBlochSphereRoute + "/" + i + "?time=" + new Date();
          }
        },
        error => { window.console.log(error) }
      )
    } catch (error) {
      window.console.log("i think there is an error " + error);
    }

  },
};
