module hidden_output_layer
#(
    parameter Q = 13,   // Fractional part
    parameter N = 16, 
    parameter NUM_OF_INPUTS = 2,
    parameter NUM_OF_OUTPUTS = 1 
)
(
    input          clk,
    input          rstn,
    input    [N-1:0] data_in [0:NUM_OF_INPUTS-1],
    input           fire,
    output   [N-1:0] data_out,
    output              done
);

wire done_int;
wire overflow_int [0:NUM_OF_INPUTS-1];
wire [N-1:0] data_out_int;

reg [N-1:0] WeightMem [0:NUM_OF_INPUTS-1];
reg [N-1:0] BiasMem;

// Load the weights and biases
always @(negedge rstn) begin
 
    // Neuron 1
    WeightMem[0] <= 16'b1111100011101110; 
    WeightMem[1]<= 16'b0111100011101100; 
    
    // Bias
    BiasMem <= 16'b1010110001100011;

end

reg mult_done [0:NUM_OF_INPUTS-1];
reg [N-1:0] prod_result [0:NUM_OF_INPUTS-1];


// ------------------------ Neuron 1 ------------------------------ 

genvar i; 
generate 
    for(i = 0; i < NUM_OF_INPUTS ; i = i + 1) begin 
        fix_point_multiplier fp_mult_n1
        (
            .a(data_in[i]),
            .b(WeightMem[i]),
            .clk(clk), 
            .rstn(rstn),
            .poke(fire),
            .prod(prod_result[i]),
            .overflow(overflow_int[i]),
            .peek(mult_done[i])   
        );
    end
endgenerate

// Adders
// ------ Adder Layer 1 -------------
reg [N-1:0] adder1_l1_n1;
reg adder1_l1_n1_done;

fix_point_adder layer1_add1_n1
   
    (
    .clk(clk),
    .rstn(rstn),
    .a(prod_result[0]),
    .b(prod_result[1]),
    .poke(mult_done[0]), 
    .sum(adder1_l1_n1), 
    .peek(adder1_l1_n1_done)
    );


    
// ------ Adder Layer 2 -------------
reg [N-1:0] adder3_l2_n1;

fix_point_adder layer2_add3_n1 
    (
    .clk(clk),
    .rstn(rstn),
    .a(adder1_l1_n1),
    .b(BiasMem),
    .poke(adder1_l1_n1_done), 
    .sum(data_out_int), 
    .peek(done_int)
    );

// ------------------------ End of Neuron 1 ------------------------------ 

reg sigmoid_done;
// ----------- Sigmoid Activation ----------------------------------------------------
sigmoid n1
    (
      .clk(clk),
      .rstn(rstn),
      .sigmoid_in(data_out_int),
      .poke(done_int),
      .sigmoid_out(data_out),
      .peek(sigmoid_done)
    );

// ----------- End of Sigmoid Activation ----------------------------------------------


assign done = sigmoid_done;
    
initial begin
    $dumpfile("hidden_output_layer.vcd");
    $dumpvars(1, hidden_output_layer);
    $display("Inside the hidden_output_layer");
  end

endmodule