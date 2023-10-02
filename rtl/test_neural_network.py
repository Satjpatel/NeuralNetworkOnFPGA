from cocotb_test.simulator import run
def test_neural_network():
    run(
        verilog_sources=["neural_network.sv", "hidden_output_layer.sv", "input_hidden_layer.sv", "fix_point_adder.sv", "fix_point_multiplier.sv", "sigmoid.sv"], # sources
        toplevel="neural_network",            # top level HDL
        module="tb_neural_network"        # name of cocotb test module
    )