
def execute(dipha_input, dipha_output, parallels=1, dual=False):
    import homcloud.dipha_alt_ext as dipha_alt_ext
    del parallels, dual
    input_binary = dipha_input.get_binary()
    output_binary = dipha_alt_ext.compute(input_binary)
    dipha_output.binary = output_binary
