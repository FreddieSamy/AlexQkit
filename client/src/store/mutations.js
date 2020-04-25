export default {

  setRow: (state, { qstate, list, idx }) => {
    state.jsonObject.init[idx] = qstate
    state.jsonObject.rows[idx] = list ;
  },
  
  appendInit:state => state.jsonObject.init.push("0"),
  removeInit:state => state.jsonObject.init.pop(),
  appendWire:state => state.jsonObject.wire++ ,

  remoceWire:(state) => {
    state.jsonObject.wire--;
    state.jsonObject.rows.pop();
  } 
};
