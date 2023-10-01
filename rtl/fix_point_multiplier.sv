`timescale 1ns / 1ps

module fix_point_multiplier
    #(
        parameter FRACTIONAL_BITS = 13,   // Fractional
        parameter N = 16 
    )
    (
        input   [N-1:0] a,
        input   [N-1:0] b,
        input          clk, 
        input          rstn,
        input          poke,
        output  [N-1:0] prod,
        output  reg overflow,
        output reg peek   
    );

// Internal Signals
reg [2*N-1:0] r_full_product;
reg [N-1:0] r_prod;
reg peek_delayed;

always @ (posedge clk or negedge rstn) begin : Multiplication
    if(!rstn) begin 
    r_full_product <= 'b0;
    overflow <= 1'b0;
    peek <= 1'b0;
    peek_delayed <= 1'b0;
    end
    else begin 
    peek_delayed <= peek; 

    if(poke) begin 
    r_full_product <= a[N-2:0] * b[N-2:0];
    overflow <= 1'b0;
    peek <= #0.1 1'b1;
    end
    if(peek_delayed) begin 
        peek <= 1'b0;
    end
    end
end

always @(r_full_product) begin
    r_prod[N-2:0] <= r_full_product[N-2+FRACTIONAL_BITS:FRACTIONAL_BITS];
    if((r_prod[2*N-2:N-1+FRACTIONAL_BITS] > 0)) 
        overflow <= 1'b1;
end

// Final Product
assign prod[N-2:0] = r_prod[N-2:0];
assign prod[N-1] = a[N-1] ^ b[N-1]; // Signed bit

initial begin
    $dumpfile("fp_mult.vcd");
    $dumpvars(1, fix_point_multiplier);
  end

endmodule
