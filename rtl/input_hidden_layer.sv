module input_hidden_layer
#(
    parameter Q = 13,   // Fractional part
    parameter N = 16, 
    parameter NUM_OF_INPUTS = 4,
    parameter NUM_OF_OUTPUTS = 2 
)
(
    input          clk,
    input          rstn,
    input    [N-1:0] data_in [0:NUM_OF_INPUTS-1],

    input           fire,
    output   [N-1:0] data_out [0:NUM_OF_OUTPUTS-1],
    output              done
);

wire done_int [NUM_OF_OUTPUTS-1:0];
wire overflow_int [0:NUM_OF_INPUTS-1][0:NUM_OF_OUTPUTS-1];
wire [N-1:0] data_out_int [0:NUM_OF_OUTPUTS-1];

reg [N-1:0] WeightMem [0:NUM_OF_INPUTS-1][0:NUM_OF_OUTPUTS-1];
reg [N-1:0] BiasMem [0:NUM_OF_OUTPUTS-1];

// Load the weights and biases
always @(negedge rstn) begin
 
 // Neuron 1
WeightMem[0][0] <= 16'b1110010000111100; 
WeightMem[1][0] <= 16'b0111100010001000; 
WeightMem[2][0] <= 16'b0111100010001000; 
WeightMem[3][0] <= 16'b0111100010001000; 
// Neuron 2
WeightMem[0][1] <= 16'b1111011011000010; 
WeightMem[1][1] <= 16'b0110111001100111; 
WeightMem[2][1] <= 16'b0110111001100111; 
WeightMem[3][1] <= 16'b0110111001100111; 
   
// Bias
BiasMem[0] <= 16'b1111011110010110;
BiasMem[1] <= 16'b1111010010111110; 
end



reg mult_done [0:NUM_OF_INPUTS-1][0:NUM_OF_OUTPUTS-1];
reg [N-1:0] prod_result [0:NUM_OF_INPUTS-1][0:NUM_OF_OUTPUTS-1];


// ------------------------ Neuron 1 ------------------------------ 

genvar i; 
generate 
    for(i = 0; i < NUM_OF_INPUTS ; i = i + 1) begin 
        fix_point_multiplier fp_mult_n1
        (
            .a(data_in[i]),
            .b(WeightMem[i][0]),
            .clk(clk), 
            .rstn(rstn),
            .poke(fire),
            .prod(prod_result[i][0]),
            .overflow(overflow_int[i][0]),
            .peek(mult_done[i][0])   
        );
    end
endgenerate

// Adders
// ------ Adder Layer 1 -------------
reg [N-1:0] adder1_l1_n1, adder2_l1_n1;
reg adder1_l1_n1_done, adder2_l1_n1_done;

fix_point_adder layer1_add1_n1
   
    (
    .clk(clk),
    .rstn(rstn),
    .a(prod_result[0][0]),
    .b(prod_result[1][0]),
    .poke(mult_done[0][0]), 
    .sum(adder1_l1_n1), 
    .peek(adder1_l1_n1_done)
    );

fix_point_adder layer1_add2_n1
   
    (
    .clk(clk),
    .rstn(rstn),
    .a(prod_result[2][0]),
    .b(prod_result[3][0]),
    .poke(mult_done[2][0]), 
    .sum(adder2_l1_n1), 
    .peek(adder2_l1_n1_done)
    );


    
// ------ Adder Layer 2 -------------
reg [N-1:0] adder3_l2_n1;
reg adder3_l2_n1_done;

fix_point_adder layer2_add3_n1 
    (
    .clk(clk),
    .rstn(rstn),
    .a(adder1_l1_n1),
    .b(adder2_l1_n1),
    .poke(adder1_l1_n1_done), 
    .sum(adder3_l2_n1), 
    .peek(adder3_l2_n1_done)
    );

// ----- Adder Layer 3 -------------- 
fix_point_adder layer3_add4_n1 
    (
    .clk(clk),
    .rstn(rstn),
    .a(adder3_l2_n1),
    .b(BiasMem[0]),
    .poke(adder3_l2_n1_done), 
    .sum(data_out_int[0]), 
    .peek(done_int[0])
    );
    
// ------------------------ End of Neuron 1 ------------------------------ 

// ------------------------ Neuron 2 ------------------------------ 

genvar j; 
generate 
    for(j = 0; j < NUM_OF_INPUTS ; j = j + 1) begin 
        fix_point_multiplier fp_mult_n2
        (
            .a(data_in[j]),
            .b(WeightMem[j][1]),
            .clk(clk), 
            .rstn(rstn),
            .poke(fire),
            .prod(prod_result[j][1]),
            .overflow(overflow_int[j][1]),
            .peek(mult_done[j][1])   
        );
    end
endgenerate

// Adders
// ------ Adder Layer 1 -------------
reg [N-1:0] adder1_l1_n2, adder2_l1_n2;
reg adder1_l1_n2_done, adder2_l1_n2_done;

fix_point_adder layer1_add1_n2
    
    (
    .clk(clk),
    .rstn(rstn),
    .a(prod_result[0][1]),
    .b(prod_result[1][1]),
    .poke(mult_done[0][1]), 
    .sum(adder1_l1_n2), 
    .peek(adder1_l1_n2_done)
    );

fix_point_adder layer1_add2_n2
    
    (
    .clk(clk),
    .rstn(rstn),
    .a(prod_result[2][1]),
    .b(prod_result[3][1]),
    .poke(mult_done[2][1]), 
    .sum(adder2_l1_n2), 
    .peek(adder2_l1_n2_done)
    );


    
// ------ Adder Layer 2 -------------
reg [N-1:0] adder3_l2_n2;
reg adder3_l2_n2_done;

fix_point_adder layer2_add3_n2 
    (
    .clk(clk),
    .rstn(rstn),
    .a(adder1_l1_n2),
    .b(adder2_l1_n2),
    .poke(adder1_l1_n2_done), 
    .sum(adder3_l2_n2), 
    .peek(adder3_l2_n2_done)
    );

// ----- Adder Layer 3 -------------- 
fix_point_adder layer3_add4_n2 
    (
    .clk(clk),
    .rstn(rstn),
    .a(adder3_l2_n2),
    .b(BiasMem[0]),
    .poke(adder3_l2_n2_done), 
    .sum(data_out_int[1]), 
    .peek(done_int[1])
    );
    
// ------------------------ End of Neuron 2 ------------------------------ 

reg sigmoid_done [0:NUM_OF_OUTPUTS-1];
// ----------- Sigmoid Activation ----------------------------------------------------
sigmoid n1
    (
      .clk(clk),
      .rstn(rstn),
      .sigmoid_in(data_out_int[0]),
      .poke(done_int[0]),
      .sigmoid_out(data_out[0]),
      .peek(sigmoid_done[0])
    );

sigmoid n2
    (
      .clk(clk),
      .rstn(rstn),
      .sigmoid_in(data_out_int[1]),
      .poke(done_int[1]),
      .sigmoid_out(data_out[1]),
      .peek(sigmoid_done[1])
    );
// ----------- End of Sigmoid Activation ----------------------------------------------




assign done = sigmoid_done[0] & sigmoid_done[1];
    
initial begin
    $dumpfile("input_hidden_layer.vcd");
    $dumpvars(1, input_hidden_layer);
  end

endmodule