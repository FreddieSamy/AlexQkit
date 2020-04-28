
import axios from "axios";

export default {

  // Setters
  setCols:(state, count) => { state.jsonObject.colsCount = count ;},
  setExe: (state, count) => { state.jsonObject.exeCount  = count ;},
  setRow: (state, { qstate, list, idx }) => {
    state.jsonObject.init[idx] = qstate ;
    state.jsonObject.rows[idx] = list ;
  },

  
  // Appenders Functions
  appendInit:state => state.jsonObject.init.push("0"),
  appendWire:state => state.jsonObject.wire++ ,


  // Remove Functions
  removeInit:state => state.jsonObject.init.pop(),
  removeWire:(state) => {
    state.jsonObject.wire--;
    state.jsonObject.rows.pop();
  },
  
  // Reset System
  reset:(state) => {
    state.jsonObject.maxWire = 0;
    state.jsonObject.exeCount = 0;
    state.jsonObject.wires = 2 ;
    state.jsonObject.init = ['0','0'];
    state.jsonObject.rows = [[],[]];
  },


  // Server Functions
  fetchData:  (state,{route,jsonObject}) => {


    try {
      axios.post(route, jsonObject).then(
        res => {

          var data = res.data;
          window.console.log(data)
          window.console.log(state.results)
          state.results = data;
          window.console.log(state.results)
        },
      )
    } catch (error) {
      window.console.log("i think there is an error " + error);
    }

  }
};
