export default {
  chart: [
    ["00", 1],
    ["01", 0],
    ["10", 0],
    ["11", 0],
  ],
  diracNotation: " |00⟩ ",
  link: "",
  matrixRepresentation: [
    ["1", "0", "0", "0"],
    ["0", "1", "0", "0"],
    ["0", "0", "1", "0"],
    ["0", "0", "0", "1"]
  ],
  qasm: 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\ncreg c[2];',
  qasmError: ""
}