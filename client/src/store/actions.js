
export default {

  setWire:({ commit }, wire) => {
    commit('setRow',wire)
  },
  addWire:({commit}) => {
     commit('appendInit')
     commit('appendWire')
  },
  removeWire:({commit}) => {
    commit('popInit')
    commit('popWire')
  }

}


