# 4 Bit XOR Neural Network
# As a proof of concept to start working on the FPGA
import numpy
import math
import csv 

class NeuralNetwork:
    def __init__(self):
        # Defining our architecture
        self.input_layer_size = 4
        self.hidden_layer_size = 2
        self.output_layer_size = 1
        
        # Initialize weights and biases
        self.weights_input_hidden = 2 * numpy.random.random((self.input_layer_size, self.hidden_layer_size)) - 1
        self.weights_hidden_output = 2 * numpy.random.random((self.hidden_layer_size, self.output_layer_size)) - 1
        
        # Initialize the biases
        self.bias_hidden = numpy.zeros((1, self.hidden_layer_size))
        self.bias_output = numpy.zeros((1, self.output_layer_size))
    

    # We pass the weighted sum of the inputs through a Sigmoid function to normalise them between 0 and 1.
    def __sigmoid(self, x):
        return 1 / (1 + numpy.exp(-x))

    # The d/dx of the Sigmoid function (gradient), it indicates our confidence about the existing weight.
    def __sigmoid_derivative(self, x):
        return x * (1 - x)  
        
    
    # Forward pass through the network
    def forward_NN(self, X):
        # Calculate the hidden layer input (dot product of inputs and weights + bias)
        hidden_input = numpy.dot(X, self.weights_input_hidden) + self.bias_hidden
        # Apply the activation function
        hidden_output = self.__sigmoid(hidden_input)
        
        # Calculating the output layer input 
        output_input = numpy.dot(hidden_output, self.weights_hidden_output) + self.bias_output

        output_output = self.__sigmoid(output_input)
        
        return hidden_output, output_output
        
     
    # Back Propogation for weight update
    def backpropagation_NN(self, X, y, iterations):
        for iteration in range(iterations):
            # Do the forward pass first
            hidden_output, output_output = self.forward_NN(X)
            
            # Calculate errors
            output_error = y - output_output
            hidden_error = output_error.dot(self.weights_hidden_output.T)
            
            # Calculate deltas (gradients)
            delta_output = output_error * self.__sigmoid_derivative(output_output)
            delta_hidden = hidden_error * self.__sigmoid_derivative(hidden_output)
            
            # Update weights and biases
            self.weights_hidden_output += hidden_output.T.dot(delta_output)
            self.weights_input_hidden += X.T.dot(delta_hidden)
            
            # Update biases
            self.bias_output += numpy.sum(delta_output, axis = 0)
            self.bias_hidden += numpy.sum(delta_hidden, axis = 0)
            
    # Final prediction
    def predict(self, X):
        _, output = self.forward_NN(X) # We don't need the first argument (the hidden layer)
        return output

def Decimal2FixedPoint(num, integer_bits, fraction_bits):
    fixed_point_number = numpy.zeros((integer_bits+fraction_bits+1)) #One extra signed bit
    # Getting the signed bit
    if(num>0):
        fixed_point_number[0] = 0
    else:
        fixed_point_number[0] = 1
        num = -num
    
    # Getting the integer parts
    int_part = int(num)
    if (int_part > 2**integer_bits):
        for i in range(1,integer_bits+1):
            fixed_point_number[i] = 1  # Max possible number
    else:
        temp = bin(int_part)[2:]  # Getting rid of the '0b'
        size_temp = len(temp)
        k = 0 
        for i in range(integer_bits-size_temp+1, integer_bits+1):
            fixed_point_number[i] = temp[k]
            k = k + 1
    
    # Getting the fractional part
    frac_part = num - int_part
    for i in range(integer_bits+1, integer_bits+fraction_bits+1):
        frac_part = frac_part*2
        fixed_point_number[i] = int(frac_part)
        frac_part, _ = math.modf(frac_part)
       
    return numpy.array2string(fixed_point_number)

def float_list_to_binary_string(float_list_str):
    # Remove square brackets and split the values
    float_list = float_list_str.strip('[]').split()
    # Convert the elements to binary and join them into a string
    binary_string = ''.join(str(int(float(x))) for x in float_list)
    return binary_string

def FileConvert2FixedPoint (X, filename, integer_bits, fractional_bits):
        size = X.shape
        list_data = [[0 for _ in range(size[1])] for _ in range(size[0])]
        for i in range(size[0]):
            for j in range(size[1]):
                list_data[i][j] = float_list_to_binary_string(Decimal2FixedPoint(X[i,j],  integer_bits, fractional_bits))
        
        file = filename + ".csv"
        with open(file, mode = 'w', newline='') as file:
            writer = csv.writer(file)
            
            # Write each row(list) from the data list to the CSV file
            for row in list_data:
                writer.writerow(row)
        # numpy.savetxt('file',X, delimiter = ',')


 
if __name__ == "__main__":
    # Initialize the neural network
    neuralnet = NeuralNetwork()
    
    # Getting the training data 
    training_data = numpy.loadtxt(open("xor_training.csv"), delimiter = ",", skiprows=1)
    
    training_inputs = training_data[:, :4]
    training_outputs = (training_data[:, 4:])
    
    # Now we training the network
    neuralnet.backpropagation_NN(training_inputs, training_outputs, 10000)
    
    # Writing out our weights and biases into a seperate file
    FileConvert2FixedPoint(neuralnet.weights_input_hidden, "WeightsL12", 2, 13)
    FileConvert2FixedPoint(neuralnet.weights_hidden_output, "WeightsL23", 2, 13)
    FileConvert2FixedPoint(neuralnet.bias_hidden, "BiasL2", 2, 13)
    FileConvert2FixedPoint(neuralnet.bias_output, "BiasL3", 2, 13)

    print(neuralnet.predict(numpy.array([1,0,0,1])))