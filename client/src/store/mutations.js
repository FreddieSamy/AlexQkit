import axios from "axios";
import { appRoute, defaultBlochSphereRoute } from "../data/routes";

export default {
  /*=== Setters ==*/
  setCols: (state, count) => {
    state.jsonObject.colsCount = count;
  },
  setExe: (state, count) => {
    state.jsonObject.exeCount = count;
  },
  setContorls: (state, val) => {
    // counter
    state.specialGatesCounter.controls += val;
  },
  setSwaps: (state, val) => {
    // counter
    state.specialGatesCounter.swaps += val;
  },
  setCustoms: (state, val) => {
    // counter
    state.specialGatesCounter.customs += val;
  },
  setRow: (state, { qstate, list, idx }) => {
    state.jsonObject.init[idx] = qstate;
    state.jsonObject.rows[idx] = list;
  },
  setAlgorithms(state,algorithms){
    state.algorithms = algorithms;
  },
  /* ================================================================= */
  /*=== Appenders Functions ===*/
  appendInit: (state) => state.jsonObject.init.push("0"),
  appendWire: (state) => {
    state.jsonObject.wires++;
    state.jsonObject["rows"].push(
      new Array(state.jsonObject.colsCount).fill("i"),
    );
  },
  appendMessage: (state, { messageType, messageBody }) => {
    state.messages[messageType].push(messageBody);
  },
  appendCustomGate: (state, customGate) => {
    state.gates.push(customGate);
  },

  /* ================================================================= */
  /*=== Remove Functions ===*/
  popInit: (state) => state.jsonObject.init.pop(),
  popWire: (state) => {
    state.jsonObject.wires--;
    //state.jsonObject.wires = Math.max(0, this.jsonObject.wires - 1);
    state.jsonObject.rows.pop();
  },
  /* ================================================================= */
  /*=== Reset System== =*/
  resetJsonObject: (state) => {
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
  resetMessages: (state) => {
    state.messages = {
      advanced: [],
      alert: [],
      violation: [],
      errors: [],
    };
  },
  resetSpecialGates: (state) => {
    state.specialGatesCounter = {
      controls: 0,
      swaps: 0,
      customs: 0,
    };
  },

  /* ================================================================= */
  // Count the occurence of specific gate by it's name
  countGate: (state, gateName) => {
    var count = 0;
    for (let i = 0; i < state.jsonObject.rows; i++) {
      for (let j = 0; j < state.jsonObject.colsCount; j++) {
        if (state.jsonObjectObject.rows[i][j] === gateName) {
          count += 1
        }
      }
    }
    return count;
  },
  /* ================================================================= */
  /*=== Validation Functions ===*/

  //Check for in every Column there is an even numbers of swaps
  swapConstrains: (state) => {
    //window.console.log("check swap")
    for (let col = 0; col < state.jsonObject.exeCount; col++) {
      let count = 0;
      for (let row = 0; row < state.jsonObject.wires; row++) {
        if (state.jsonObject.rows[row][col] === "Swap") {
          count++;
        }
      }
      // i think i should have a file of messages
      if (count == 1) {
        state.messages.violation.push(
          "on column(" +
          (col + 1) +
          ") : you need to put more swap gate at same column",
        );
      } else if (count > 2) {
        state.messages.violation.push(
          "on column (" +
          (col + 1) +
          ") : you can put only two swaps in one column",
        );
      }
    }
  },

  /* ================================================================= */
  /* 
    - wirecustom function: it's validate function on the circuit to check  how many times user put custom gate on wires
    and compare it with real wires for this gate .
    
  */
  wirescustom: (state) => {

    let dicwire = {};
    for (let indx in state.gates) {
      if (state.gates[indx]["wires"]) {
        var wire = state.gates[indx]["wires"];
        var name = state.gates[indx]["name"];
        dicwire[name] = wire;
      }
    }


    for (let col = 0; col < state.jsonObject.colsCount; col++) {
      let dicCount = {};
      for (let row = 0; row < state.jsonObject.wires; row++) {
        if (state.jsonObject.rows[row][col][0]=="c") {
          var nameofgate = state.jsonObject.rows[row][col];  //custom_q.0
          nameofgate = nameofgate.substring(0, nameofgate.indexOf(".")); //custom_q
          if (!(nameofgate in dicCount)) {
            dicCount[nameofgate] = 1;
          }
          else {
            dicCount[nameofgate] += 1;
          }
        }
      }


      for (let indx in dicCount) {
        var count = dicCount[indx];
        if (indx in dicwire) {
          var wires = dicwire[indx];
          if (count != wires) {
            var realname = indx.substring(7);
            state.messages.violation.push("gate " + realname + " at column " + (col + 1) + " can be put only for " + wire + " wires" + " not " + dicCount[nameofgate]);
          }
        }
      }
    }
  },

  /* ================================================================= */
  /*=== Server Functions ==*/
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

  /* ================================================================= */
  // browser localStorage functions 
  storeLocal: (state, objectName) => {
    localStorage.setItem(objectName, JSON.stringify(state[objectName]))
  },

  getLocal: (state, objectName) => {
    state[objectName] = JSON.parse(localStorage.getItem(objectName))
    return state[objectName]
  }
}
