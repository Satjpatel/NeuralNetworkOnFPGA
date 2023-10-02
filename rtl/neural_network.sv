module neural_network 
#(
    parameter Q = 13,   // Fractional part
    parameter N = 16, 
    parameter NUM_OF_INPUTS = 4,
    parameter NUM_OF_OUTPUTS = 1 
)
(
    input          clk_i,
    input          rstn_i,
    input    [N-1:0] data_in_i [0:NUM_OF_INPUTS-1],
    input           fire_i,
    output    [N-1:0]   prediction_o,
    output              done_o
);

// Internal Helper Signals 
wire layer_12_done, layer_23_done;
   
// Layer 1: Input layer - Hidden layer
wire [N-1:0] hidden_layer_out [0:1];

input_hidden_layer layer_12
( 
.clk(clk_i),
.rstn(rstn_i),
.data_in(data_in_i),
.fire(fire_i),
.data_out(hidden_layer_out),
.done(layer_12_done)
);
    
// Layer 2: Hidden Layer - Output layer
wire [N-1:0] output_layer_out;

hidden_output_layer layer_23
(
.clk(clk_i),
.rstn(rstn_i),
.data_in(hidden_layer_out),
.fire(layer_12_done),
.data_out(output_layer_out),
.done(layer_23_done)
);

assign prediction_o = output_layer_out; 

assign done_o = layer_23_done;


initial begin
    $dumpfile("neural_network.vcd");
    $dumpvars(1, neural_network);
end
     

endmodule