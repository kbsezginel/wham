"""
Python wrapper for Weighted Histogram Analysis Method as implemented by Grossfield et al.
"""
import os
import subprocess


class Wham:
    """
    WHAM class.
    """
    def __init__(self, simulations={}):
        """
        Initialize WHAM object.

        Parameters
        ----------
        simulations : dict
            Simulations to be included in the WHAM analysis.
            Each simulation data should be a dictionary containing
            'time', 'position', 'min', 'k', 'energy' keywords.
            Ex: {'1': {'time': [], 'position': [], 'min': 0.0, 'k': [], 'energy': None}, ...}

        """
        self.simulations = simulations

    def add_simulation(self, sim_id, time, position, min_position, k_spring, energy=None):
        """Add a simulation result.

        Parameters
        ----------
        sim_id : str or int
            Simulation identifier.
        time : list
            Simulation time.
        position : list
            Position of the system along the energy barrier during the simulation.
        min_position : float
            Location of the minimum of the biasing potential for this simulation.
        k_spring : flaot
            Spring constant for the biasing potential used in this simulation.
            Assuming a potential form of V = 0.5k(x - x0)^2.
            The unit should match the unit of the position. For example if position is in Å
            the spring constant must be in kcal/mol-Å2
        energy : list or None
            Potential energy of the system during simulation.
            Only used if a temperature is specified.

        """
        self.simulations[sim_id] = {'time': time, 'position': position,
                                    'min': min_position, 'k': k_spring,
                                    'energy': energy}

    def run(self, periodicity, hist_min, hist_max, num_bins, tolerance, temperature, numpad,
            executable, directory, verbose=True):
        """
        Run 1D WHAM analysis.

        Parameters
        ----------
        periodicity : str
            Periodicity of the reaction coordinate.
        hist_min : float
            Lower boundary of the histogram.
        hist_max : float
            Upper boundary of the histogram.
        num_bins : int
            Number of bins in the histogram, and as a result the number of points in the final PMF.
        tolerance : float
            Convergence tolerance.
        temperature : float
            Temperature at which the WHAM analysis is performed.
        numpad : int
            Number of “padding” values that should be printed for periodic PMFs.
        executable : str
            Path to WHAM 1D executable.
        directory : str
            Path to write input and output files for WHAM analysis.
        verbose : bool
            WHAM verbosity.

        Returns
        -------
        dict
            WHAM analysis results.

        """
        for sim_id, sim in self.simulations.items():
            ts_file = os.path.join(directory, f'{sim_id}.dat')
            self._write_timeseries_file(ts_file, sim['time'], sim['position'], sim['energy'])
            self.simulations[sim_id]['ts_file'] = ts_file
        data_file = os.path.join(directory, 'wham.in')
        tsfiles = [i['ts_file'] for i in self.simulations.values()]
        min_pos = [i['min'] for i in self.simulations.values()]
        k_spring = [i['k'] for i in self.simulations.values()]
        self._write_data_file(data_file, tsfiles, min_pos, k_spring)
        out_file = os.path.join(directory, 'wham.out')
        self.args = [executable, periodicity, hist_min, hist_max, num_bins,
                     tolerance, temperature, numpad, data_file, out_file]

        wham_process = subprocess.run(list(map(str, self.args)),
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
        if verbose:
            stdout, stderr = wham_process.stdout.decode(), wham_process.stderr.decode()
            print("Stdout:\n\n%s\nStderr:\n%s" % (stdout, stderr))
        return self.read_output(out_file)

    def read_output(self, filename):
        """
        Read WHAM analysis output.

        Parameters
        ----------
        filename : str
            WHAM output file name.

        Returns
        -------
        dict
            WHAM analysis results.

        """
        with open(filename, 'r') as f:
            lines = f.readlines()
        data = dict(coor=[], free=[], prob=[])
        for line in lines[1:]:
            ls = line.split()
            if ls[0] == '#Window':
                break
            else:
                data['position'].append(float(ls[0]))
                data['energy'].append(float(ls[1]))
                data['probability'].append(float(ls[3]))
        return data

    def _write_timeseries_file(self, filename, time, position, energy=None):
        """
        Write time series file including time, position, and energy (optional)
        data for a single simulation.

        Parameters
        ----------
        filename : str
            WHAM output file name.
        time : list
            Simulation time.
        position : list
            Position of the system along the energy barrier during the simulation.
        energy : list or None
            Potential energy of the system during simulation.
            Only used if a temperature is specified.

        """
        with open(filename, 'w') as f:
            if energy is None:
                for t, p in zip(time, position):
                    f.write('%.2f  %.5f\n' % (t, p))
            else:
                for t, p, e in zip(time, position, energy):
                    f.write('%.2f  %.5f  %.5f\n' % (t, p, e))

    def _write_data_file(self, filename, tsfiles, min_position, k_spring):
        """
        Read WHAM analysis output.

        Parameters
        ----------
        filename : str
            WHAM output file name.
        tsfiles : list
            List of time series files.
        min_position : list
            List of locations of the minimum of the biasing potential.
        k_spring : list
            List of spring constants for the biasing potential.

        """
        with open(filename, 'w') as f:
            for ts, m, k in zip(tsfiles, min_position, k_spring):
                f.write('%s  %.5f  %.2f\n' % (ts, m, k))