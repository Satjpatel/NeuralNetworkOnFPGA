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

Neural Network Implemented:

![image](https://github.com/Satjpatel/NeuralNetworkOnFPGA/assets/44218342/2712abeb-d4d0-4417-aec6-e456939e9668)

A consistent data format used for **fixed point arithmetic** this entire project:

| Signed Bit |  Integer Bits | Fractional Bits | 
| ---------- | --------------| --------------- |
| 1          |  2            | 13              |


## Neural Network Brief

| Layer        | Number of Neurons | Description                                      |
|--------------|-------------------|--------------------------------------------------|
| Input Layer  | 4                 | Input for 4 input XOR function                  |
| Hidden Layer | 2                 | Feature Extraction for the boolean pattern     |
| Output Layer | 1                 | If val > 0.5 --> TRUE, else val < 0.5 --> FALSE |

![image](https://github.com/Satjpatel/NeuralNetworkOnFPGA/assets/44218342/0668c6da-89a4-46cf-9231-ad321661ba90)
