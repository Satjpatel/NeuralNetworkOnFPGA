# NeuralNetworkOnFPGA

An initial proof of concept for a neural network on FPGA. 

I created this project as a proof of concept to start working with Neural Networks on an FPGA. The goal was to demonstrate that a NN could be trained to perform a simple operation (4 input XOR, for its simplicity) and then save its learned weights and biases in a format suitable for FPGA implementation. 
This exercise serves as a foundational step in exploring the implementation of machine learning models on hardware platforms like FPGAs, which can be more efficient for certain types of computations. 
I plan to take this project forward with making an FPGA implementation of an audio autoencoder in the coming weeks. 


Neural Network Implemented:

![image](https://github.com/Satjpatel/NeuralNetworkOnFPGA/assets/44218342/2712abeb-d4d0-4417-aec6-e456939e9668)

A consistent data format used for **fixed point arithmetic** this entire project:

| Signed Bit |  Integer Bits | Fractional Bits | 
| ---------- | --------------| --------------- |
| 1          |  2            | 13              |


## Neural Network Brief

| Layer        | Number of Neurons | Description                                      |
|--------------|-------------------|--------------------------------------------------|
| Input Layer  | 4                 | Input for 4 input XOR function                   | asasdfasdfasdfasdfasdfsadfsdfsdf
| Hidden Layer | 2                 | Feature Extraction for the boolean pattern     |
| Output Layer | 1                 | If val > 0.5 --> TRUE, else val < 0.5 --> FALSE |


\### Project status

- [x] Python proof of concept
- [x] Fixed Point Adder
- [x] Fixed Point Multiplier
- [] Sigmoid LUT
- [] Neuron
- [] Neural Network Layer
- [] Neural Network
- [] Cocotb Verification 

## Cocotb QuickStart

Shoutout to AJ Steenhoek to introduce me to this, and showing me the basics! 

This project gave me an oppurtunity to try out [Cocotb](https://github.com/cocotb/cocotb). It is a simulation library for writing testbenches in Python. It is easy to use, and more importantly, compatible with standard Python libraries (makes verifying DSP modules damn easy, ha ha). 

I am using [cocotb_test](https://github.com/themperek/cocotb-test) with it too, to remove the need of Makefiles. Shoutout to AJ for this too! 

All the design and verification files are in the rtl directory. The reason for non-segregation into 'src' and 'sim' is because cocotb-test needs both design and verification files in the same directory. 

Naming convention: 

Design Units: <module_name>.sv
Cocotb Testbench: <tb_module_name>.py
Cocotb-test File: <test_module_name>.py

For Quick Reference, an example of a Cocotb test file: 

- Create a `<test_module_name>.py` file: 

```python
from cocotb_test.simulator import run
def test_fix_point_adder():
    run(
        verilog_sources=["fix_point_adder.sv"], # source
        toplevel="fix_point_adder",             # top level HDL
        module="tb_fix_point_adder"             # name of cocotb test module
    )
```
