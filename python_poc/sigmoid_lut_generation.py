# Sigmoid LUT Generation
import math
import numpy

# Sigmoid Function
def __sigmoid(x):
    return 1 / (1 + numpy.exp(-x))

# Function for converting decimal values into binary
def Decimal2Binary(x, dataWidth, fracBits):
    if x >= 0:
        x = x * (2**fracBits) # Getting rid of the decimal point
        bin_num = bin(int(x))[2:] #[2:] is to get rid of the first 2 literals '0b'
    else:
        x = -x
        x = x * (2**fracBits) # Getting rid of the decimal point
        x = int(x)
        if x == 0:
            bin_num = 0
        else:
            bin_num = 2**dataWidth - x  # Offsetting for the 2's complement
            bin_num = bin(bin_num)[2:]
    return bin_num

# Sigmoid LUT generation
def sigmoid_lut(dataWidth, sigmoid_input_size, weight_bias_sum_int_size):
    f = open("sigmoid_lut.mif", "w")
    fractBits = sigmoid_input_size - (weight_bias_sum_int_size)
    if fractBits < 0: 
        fractBits = 0
    x = -2**((weight_bias_sum_int_size-1))
    for i in range(0, 2**sigmoid_input_size):
        y = __sigmoid(x)
        z = Decimal2Binary(y, dataWidth, fractBits)
        f.write(z+'\n') # Go to the next line
        x = x+(2**(-fractBits))
    f.close()
    
if __name__ == "__main__":
    sigmoid_lut(dataWidth=16, sigmoid_input_size=16, weight_bias_sum_int_size=2)
    