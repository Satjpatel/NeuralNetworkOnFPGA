# NeuralNetworkOnFPGA

An initial proof of concept for neural network on FPGA. 

This project aims to create a basic framework for a basic neural network on an FPGA. 

Hierarchy of the project: 

- `neuralnetwork.sv`
 - `neuralnetwork_layer.sv`
  - `neuron.sv`
    - `fixed_point_add.sv`
    - `fixed_point_mult.sv`
    - `sigmoid_lut.sv`


