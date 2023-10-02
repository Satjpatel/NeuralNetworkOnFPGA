from cocotb_test.simulator import run
def test_fix_point_multiplier():
    run(
        verilog_sources=["input_hidden_layer.sv", "fix_point_adder.sv", "fix_point_multiplier.sv", "sigmoid.sv"], # sources
        toplevel="input_hidden_layer",            # top level HDL
        module="tb_input_hidden_layer"        # name of cocotb test module
    )