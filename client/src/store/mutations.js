export default {

  setRow: (state, { qstate, list, idx }) => {
    state.jsonObject.init[idx] = qstate
    state.jsonObject.rows[idx] = list ;
  },
  
  appendInit:state => state.jsonObject.init.push("0"),
  removeInit:state => state.jsonObject.init.pop(),
  appendWire:state => state.jsonObject.wire++ ,

  removeWire:(state) => {
    state.jsonObject.wire--;
    state.jsonObject.rows.pop();
  },
  
  reset:(state) => {
    state.maxWire = 0;
    state.jsonObject.exeCount = 0;
    state.jsonObject.wires = 2 ;
    state.jsonObject.init = ['0','0'];
    state.jsonObject.rows = [[],[]];
  }
};
