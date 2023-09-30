`timescale 1us/1ns

module fix_point_adder
    #(
        parameter Q = 13,   // Fractional
        parameter N = 16 
    )
    (
        input          clk,
        input          rstn,
        input    [N-1:0] a,
        input    [N-1:0] b,
        output  [N-1:0] sum
    );

reg [N-1:0] r_sum;

always @(posedge clk or negedge rstn) begin
    if(!rstn) begin 
        r_sum = 'b0;
    end
    // If both numbers are of same sign
    else if(a[N-1] == b[N-1]) begin 
        r_sum[N-2:0] = a[N-2:0] + b[N-2:0]; // Since they have the same sign, absolute sum increases
        r_sum[N-1] = a[N-1];
    end
    
    // a > 0 and b < 0
    else if(a[N-1] == 0 && b[N-1] == 1) begin  // a - b
        //  If a > b
        if(a[N-2:0] > b[N-2:0]) begin 
            r_sum[N-2:0] = a[N-2:0] - b[N-2:0]; 
            r_sum[N-1] = 0; // Final answer is positive
        end
        else begin // a < b 
            r_sum[N-2:0] = b[N-2:0] - a[N-2:0]; 
            if(r_sum[N-2:0] == 0)
                r_sum[N-1] = 0; // The zero case
            else
                r_sum[N-1] = 1; // Final answer is negative
        end
    end

    // a < 0 and b > 0
    else if(a[N-1] == 1 && b[N-1] == 0) begin  // b - a
        //  If b > a
        if(b[N-2:0] > a[N-2:0]) begin 
            r_sum[N-2:0] = b[N-2:0] - a[N-2:0]; 
            r_sum[N-1] = 0; // Final answer is positive
        end
        else begin // a > b 
            r_sum[N-2:0] = a[N-2:0] - b[N-2:0]; 
            if(r_sum[N-2:0] == 0)
                r_sum[N-1] = 0; // The zero case
            else
                r_sum[N-1] = 1; // Final answer is negative
        end
    end

end

// Final result
assign sum = r_sum;

initial begin
    $dumpfile("dump.vcd");
    $dumpvars(1, fix_point_adder);
  end

endmodule