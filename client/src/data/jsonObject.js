export default {
  API_TOKEN: "",    // IBM TOKEN
  colsCount: 0,     // Columns Counter
  // custom: {},    stored in backend
  device: "",       // IBM Device Used
  rows: [[], []],   // 2D array for wires -> gates in each wire
  exeCount: 0,      // Pointer for the Tracing Line Execution
  init: ["0", "0"], // States of The Qubits
  radian: false,    // Flag for Rotation Angles degree or radian
  repeated: {},     // Object for Loops in the Circiut
  shots: 1024,      // Number of Shots
  wires: 2,         // Number of Wires

};
