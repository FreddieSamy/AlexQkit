export default [
  {
    name: "tele_algorithm1",
    circuit: {
      wires: 3,
      init: ["0", "0", "0"],
      rows: [
        ["x", "i", "●", "h", "i", "h"],
        ["i", "h", "●", "x", "●", "i"],
        ["i", "i", "x", "i", "h", "●"],
      ],
    },
  },
  {
    name: "mario_algorithm2",
    circuit: {
      wires: 3,
      init: ["0", "0", "0"],
      rows: [
        ["x", "i", "●", "x", "i", "h"],
        ["x", "h", "●", "x", "●", "i"],
        ["x", "i", "x", "x", "h", "●"],
      ],
    },
  },
  {
    name: "tele_algorithm3",
    circuit: {
      wires: 3,
      init: ["0", "0", "0"],
      rows: [
        ["x", "i", "●", "h", "x", "h"],
        ["i", "x", "●", "x", "x", "i"],
        ["i", "i", "x", "i", "x", "●"],
      ],
    },
  },
  {
    name: "tele_algorithm4",
    circuit: {
      wires: 3,
      init: ["0", "0", "0"],
      rows: [
        ["x", "x", "x", "x", "x", "x"],
        ["i", "h", "●", "x", "●", "x"],
        ["i", "i", "x", "i", "h", "x"],
      ],
    },
  },
];
