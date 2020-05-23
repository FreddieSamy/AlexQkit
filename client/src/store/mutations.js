import axios from "axios";
import { appRoute, defaultBlochSphereRoute } from "../data/routes";

export default {
  // Setters
  setCols: (state, count) => {
    state.jsonObject.colsCount = count;
  },
  setExe: (state, count) => {
    state.jsonObject.exeCount = count;
  },
  setRow: (state, { qstate, list, idx }) => {
    state.jsonObject.init[idx] = qstate;
    state.jsonObject.rows[idx] = list;
  },

  /* ================================================================= */

  // Appenders Functions
  appendInit: (state) => state.jsonObject.init.push("0"),
  appendWire: (state) => state.jsonObject.wire++,
  appendMessage: (state , {messageType,messageBody})=>{
    state.messages[messageType].push(messageBody)
  },

  /* ================================================================= */

  // Remove Functions
  removeInit: (state) => state.jsonObject.init.pop(),
  removeWire: (state) => {
    state.jsonObject.wire--;
    state.jsonObject.rows.pop();
  },
  removeMessages: (state) => {
    state.messages = {
      advanced:[],
      alert:[],
      violation:[],
      errors:[],
    };
  },

  /* ================================================================= */
  // Reset System
  reset: (state) => {
    state.jsonObject = {
      API_TOKEN: "",
      colsCount: 0,
      device: "",
      rows: [[], []],
      exeCount: 0,
      init: ["0", "0"],
      radian: false,
      repeated: {},
      shots: 1024,
      wires: 2,
    };
  },

  /* ================================================================= */
  // Validation Functions

  //Check for in every Column there is an even numbers of swaps
  swapConstrains: (state) => {
    for (let col = 0; col < state.jsonObject.exeCount; col++) {
      let count = 0;
      for (let row = 0; row < state.jsonObject.wires; row++) {
        if (state.jsonObject.rows[row][col] === "swap") {
          count++;
        }
      }
      if (count % 2 != 0) {
        window.console.log("odd number of swaps at col " + col);
        state.messages.violation.push('"odd number of swaps at columns')
      }
    }
  },

  /* ================================================================= */

  // Server Functions
  sendCircuit: (state) => {
    try {
      //window.console.log(state.jsonObject)
      axios.post(appRoute, state.jsonObject).then(
        (res) => {
          state.results = res.data;

          // 3ak fe 3ak lazem yet8ayer
          for (let i = 1; i <= state.jsonObject.wires; i++) {
            var imgofblochSphere = document.getElementById("bloch-sphere-" + i);
            imgofblochSphere.src =
              defaultBlochSphereRoute + "/" + i + "?time=" + new Date();
          }
        },
        (error) => {
          window.console.log(error);
        },
      );
    } catch (error) {
      window.console.log("i think there is an error " + error);
    }
  },
};
