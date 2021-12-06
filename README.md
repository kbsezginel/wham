# wham
Python wrapper for Weighted Histogram Analysis Method as implemented by Grossfield et al.

Tested on Version 2.0.9.

## Installation
1. Download WHAM from [here](http://membrane.urmc.rochester.edu/?page_id=126)
2. Install Python wrapper:
```
pip install git+https://github.com/kbsezginel/wham
```

## Usage
Currently, the wrapper only supports 1D WHAM calculations but feel free to open an issue or a pull request if you would like 2D WHAM implemented.

Make sure you check out [WHAM documentation](http://membrane.urmc.rochester.edu/sites/default/files/wham/doc.pdf) before using it. It's fairly short and very informative. All the parameters below would make much more sense after you read it.

Note: Since periodicity is not an optional argument, an empty string should be entered for it if the collective variable is not periodic.

```python
from wham import Wham


W = Wham()
"""
Add your simulations with and id, simulation time, position,
equilibrium position for the spring, and spring constant in kcal/mol
"""
W.add_simulation(sim_id, time, position, eq_position, k_spring)

# You can plot position histograms before running WHAM
W.plot_histograms(title='WHAM histograms', save='wham-hist.png'))

"""
You can run WHAM 1D as follows.
The input parameters are in the same order as the WHAM executable:
periodicity of the reaction coordinate, lower and upper boundary of the histogram, number of bins in the histogram, convergence tolerance, temperature at which the WHAM analysis is performed, number of “padding” values that should be printed for periodic PMFs, path to WHAM 1D executable, path to write input and output files for WHAM analysis, cleanup WHAM files after running and finally WHAM verbosity.
"""
W.run(periodicity, hist_min, hist_max, num_bins, tolerance, temperature,
      numpad, executable, directory, cleanup=False, verbose=True)

# Finally, you can plot the free energy barrier using the function below
W.plot_energy_barrier(save='wham-barrier.png'))
```
