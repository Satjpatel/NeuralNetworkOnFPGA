# Helper functions for the Neural Network, chiefly related to fixedpoint 
# number manipulation

import numpy
import math
import csv 


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
        list_data = [[0 for _ in range(size[1])] for _ in range(size[0])]  # Convert numpy data into list to write into a CSV 
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

if __name__ == "__main__":
    a = float_list_to_binary_string(Decimal2FixedPoint(-2.5, 2, 13))
    print(f"a in binary string is {a}")
    # Convert to Decimal Back
    a_dec = BinaryStringToDecimal("0001000000000000", 2, 13)
    print(f"a back in decimal is {a_dec}")
    