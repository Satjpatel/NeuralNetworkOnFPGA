from cocotb_test.simulator import run
def test_hidden_output_layer():
    run(
        verilog_sources=["hidden_output_layer.sv", "fix_point_adder.sv", "fix_point_multiplier.sv", "sigmoid.sv"], # sources
        toplevel="hidden_output_layer",            # top level HDL
        module="tb_hidden_output_layer"        # name of cocotb test module
    )