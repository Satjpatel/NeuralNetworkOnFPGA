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
        output  [N-1:0] prod,
        output  reg overflow   
    );

// Internal Signals
reg [2*N-1:0] r_full_product;
reg [N-1:0] r_prod;

always @ (posedge clk or negedge rstn) begin : Multiplication
    if(!rstn) begin 
    r_full_product <= 'b0;
    overflow <= 1'b0;
    end
    else begin 
    r_full_product <= a[N-2:0] * b[N-2:0];
    overflow <= 1'b0;
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

endmodule
