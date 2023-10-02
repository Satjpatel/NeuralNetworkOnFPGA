import random
import numpy
import math
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.types import LogicArray
from cocotb.binary import BinaryValue
from XOR_NN import *

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

def SignedFixedPoint2Binary(num, integer_bits, fractional_bits):
    return BinaryValue(float_list_to_binary_string(Decimal2FixedPoint(num, integer_bits, fractional_bits)), integer_bits+fractional_bits+1, True)


def BinaryStringToDecimal(binary_string, integer_bits, fraction_bits):
    # Calculate the total number of bits
    total_bits = integer_bits + fraction_bits + 1  # +1 for the sign bit
    
    # Ensure the binary string has the correct length
    if len(binary_string) != total_bits:
        raise ValueError(f"Binary string length must be {total_bits} bits")
    
    # Check the sign bit to determine if the number is negative
    is_negative = binary_string[0] == '1'
    
    # Initialize variables for integer and fractional parts
    int_part = 0
    frac_part = 0.0
    
    # Convert the integer part
    for i in range(1, integer_bits + 1):
        int_part <<= 1  # Shift left by 1 bit
        int_part |= int(binary_string[i])
    
    # Convert the fractional part
    for i in range(integer_bits + 1, total_bits):
        frac_part += int(binary_string[i]) / (2 ** (i - integer_bits))
    
    # Combine integer and fractional parts, and apply the sign
    result = int_part + frac_part
    return -result if is_negative else result


@cocotb.test()
async def tb_neural_network(dut):
    """
        To test the functionality of our neural network
    """
    
    clock = Clock(dut.clk_i, 10, units="ns")
    
    # Start the clock. Start it LOW --> Take this as Gospel
    cocotb.start_soon(clock.start(start_high=True))
    
    for _ in range(10):
        await RisingEdge(dut.clk_i)

    dut.rstn_i.value = 0
    for _ in range(5):
        await RisingEdge(dut.clk_i)
    dut.rstn_i.value = 1

    for _ in range(5):
        await RisingEdge(dut.clk_i)
    
    input_array = [0,0,1,1]
    for i in range(4):
        dut.data_in_i[i].value = SignedFixedPoint2Binary(input_array[i], 2, 13)
    # hidden_output, final_output = NeuralNetwork.predict(a, numpy.array([input_array]))


    await RisingEdge(dut.clk_i)
    dut.fire_i.value = 1
    await RisingEdge(dut.clk_i)
    print(f"fire = ", dut.fire_i.value)
    
    for _ in range(10):
        await RisingEdge(dut.clk_i)
    
    await RisingEdge(dut.done_o)
    
    val_final = dut.prediction_o.value
    val_dec = BinaryStringToDecimal(val_final, 2, 13)
    print(f"Prediction = ", val_dec) 
    print(f"Prediction 1 level up [0] = ", BinaryStringToDecimal(dut.hidden_layer_out[0].value, 2, 13)) 
    print(f"Prediction 1 level up [1] = ", BinaryStringToDecimal(dut.hidden_layer_out[1].value, 2, 13)) 
    # print(f"Neural Network hidden layer output ", hidden_output)
    # print(f"Neural Network ka final output = ", final_output)
    
    print(f" Done variable = ", dut.done_o.value) 
    