

export default {
appendWire: (state, { qstate, list, idx }) => {
    state.jsonObject.init[idx] = qstate
    state.jsonObject.rows[idx] = list ;
  },
};
