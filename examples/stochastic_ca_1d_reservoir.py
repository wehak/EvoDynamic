""" Cellular automata 1D - Self-organized criticality"""

import evodynamic.experiment as experiment
import evodynamic.connection.cellular_automata as ca
import evodynamic.cells.activation as act
import evodynamic.connection as connection
import numpy as np
import time
from PIL import Image

width = 200
timesteps = 400

exp = experiment.Experiment()
g_ca = exp.add_group_cells(name="g_ca", amount=width)
neighbors, center_idx = ca.create_pattern_neighbors_ca1d(3)
g_ca_bin = g_ca.add_binary_state(state_name='g_ca_bin', init="zeros")
g_ca_bin_conn = ca.create_conn_matrix_ca1d('g_ca_bin_conn',width,\
                                           neighbors=neighbors,\
                                           center_idx=center_idx,
                                           is_wrapped_ca=True)

"""
Best 2
80;4.375510397876782;{'norm_ksdist_res': 0.9613162536023352,
'norm_coef_res': 1.6377095314393233, 'norm_unique_states': 1.0,
'norm_avalanche_pdf_size': 0.9659114597767141, 'norm_linscore_res': 0.8704469695084798,
'norm_R_res': 0.7277920719335422, 'fitness': 4.375510397876782};
[0.39422172047670734, 0.09472197628905793, 0.2394927250526252, 0.4084554505943707, 0.0, 0.7302038703441202, 0.9150343715586952, 1.0]
"""
fargs_list = [( [0.39422172047670734, 0.09472197628905793,\
                 0.2394927250526252, 0.4084554505943707, 0.0,\
                 0.7302038703441202, 0.9150343715586952, 1.0],)]



exp.add_connection("g_ca_conn",
                     connection.WeightedConnection(g_ca_bin,g_ca_bin,
                                                   act.rule_binary_sca_1d_width3_func,
                                                   g_ca_bin_conn, fargs_list=fargs_list))

exp.add_monitor("g_ca", "g_ca_bin", timesteps)

exp.initialize_cells()

start = time.time()

exp.run(timesteps=timesteps)

print("Execution time:", time.time()-start)

exp.close()

#ca_result = np.invert(exp.get_monitor("g_ca", "g_ca_bin").astype(np.bool)).astype(np.uint8)*255
ca_result = exp.get_monitor("g_ca", "g_ca_bin").astype(np.uint8)*255

img = Image.fromarray(ca_result).resize((5*width,5*timesteps), Image.NEAREST)
timestr = time.strftime("%Y%m%d-%H%M%S")
img.save("results/evolved_stochastic_ca_zeros_"+timestr+".png")
