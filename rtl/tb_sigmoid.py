# Testing fix point adder to cocotb
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
async def tb_sigmoid(dut):
    """
        Testing out the sigmoid memory
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
        
    print('reset value = ', dut.rstn.value)
    
    dut.sigmoid_in.value = SignedFixedPoint2Binary(2.3, 2, 13)
    # Synchronize with the clock. 
 
    # await RisingEdge(dut.clk)
    
    # dut.a.value = SignedFixedPoint2Binary(a_arr[i], 2, 13) 
    # dut.b.value = SignedFixedPoint2Binary(b_arr[i], 2, 13)
    
    await RisingEdge(dut.clk)
    print(f"Value of sigmoid data in is {dut.sigmoid_in.value}")
    
    await RisingEdge(dut.clk)
    print(f"Value of sigmoid data out is {dut.sigmoid_out.value}")

    
    # res = SignedFixedPoint2Binary(expected_res[i], 2, 13)
    # if (dut.sum.value == res):
    #     print(f"PASS: Expected value {dut.sum.value} == {res}")
    # else: 
    #     raise AssertionError(f"Expected value {dut.sum.value} != {res}")
