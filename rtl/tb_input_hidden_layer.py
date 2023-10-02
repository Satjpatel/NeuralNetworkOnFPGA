import random
import numpy
import math
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.types import LogicArray
from cocotb.binary import BinaryValue

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



@cocotb.test()
async def tb_input_hidden_layer(dut):
    """
        Test out if this layer is working correctly
    """
    
    clock = Clock(dut.clk, 10, units="ns")
    
    # Start the clock. Start it LOW --> Take this as Gospel
    cocotb.start_soon(clock.start(start_high=True))
    
    for _ in range(10):
        await RisingEdge(dut.clk)

    dut.rstn.value = 0
    for _ in range(5):
        await RisingEdge(dut.clk)
    dut.rstn.value = 1

    for _ in range(5):
        await RisingEdge(dut.clk)
    
    for i in range(4):
        dut.data_in[i].value = SignedFixedPoint2Binary(0, 2, 13)
    

    
    dut.fire.value = 1
    
    # for _ in range(10):
    #     await RisingEdge(dut.clk)
    
    await RisingEdge(dut.done)
    
    print(f"data output value[0] ", dut.data_out[0].value) 
    print(f"data output value[1] ", dut.data_out[1].value)
    print(f" Done variable = ", dut.done.value) 
    