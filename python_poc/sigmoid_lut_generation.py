# Sigmoid LUT Generation
import math
import numpy
from helper_functions import *
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
            bin_num = 2**dataWidth - x  # Offsetting for the 2sig_int_size data_size, data_int_size
 
            bin_num = bin(bin_num)[2:]
    return bin_num

# Sigmoid LUT generation
def sigmoid_lut(sig_data_size, sig_int_size, data_size, data_int_size):
    frac_data_size = data_size - data_int_size - 1 #"1" for the sign bit
    # Largest Negative Number
    x = -(2**data_int_size - 2**(-frac_data_size))
    print(f"x = {x}")
    # Number of iterations 
    iterations = 2**(data_size) - 1
    print(f"iterations = {iterations}")
    step_size = 2**(-frac_data_size)
    print(f"Step size = {step_size}")
    f = open("sigmoid_lut.mif", "w")
    for i in range(0, iterations):
        y = __sigmoid(x)
        z = float_list_to_binary_string(Decimal2FixedPoint(y, sig_int_size, sig_data_size-sig_int_size-1))
        f.write(z+'\n') # Go to the next line
        x = x+step_size
    f.close()
    
if __name__ == "__main__":
    sigmoid_lut(16, 2, 10, 2)
    