# NeuralNetworkOnFPGA

An initial proof of concept for neural network on FPGA. 

This project aims to create a basic framework for a basic neural network on an FPGA. 

Hierarchy of the project: 

neuralnetwork.sv
	• neuralnetwork_layer.sv 
		○ neuron.sv
			§ fixed_point_add.sv
			§ fixed_point_mult.sv
sigmoid_lut.sv![image](https://github.com/Satjpatel/NeuralNetworkOnFPGA/assets/44218342/f06f9fb3-15fc-48c6-90f7-f86e582a9aba)

