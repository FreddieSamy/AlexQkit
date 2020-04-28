

export default {
  setColsCount: ({commit},count)=>{
    commit('setCols', count)
  },
  setExeCount: ({ commit }, count) => {
    commit('setExe', count)
  },
  setWire: ({ commit }, wire) => {
    commit('setRow', wire)
  },
  addWire: ({commit}) => {
     commit('appendInit')
     commit('appendWire')
  },
  removeWire: ({commit}) => {
    commit('popInit')
    commit('popWire')
  },
  resetCircuit: ({commit}) => {
    commit('reset')
  },
  runCircuit:({commit}) => {
    commit('sendCircuit')
  },


}
  

