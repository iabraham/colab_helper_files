import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class Field:
    """ A class to hold the details of a field

    Parameters
    ----------
    timestamps:
        An array of timestamps
    firingrates:
        An array of neuronal firing rates at each time stamp
    """
            
    def __init__(self, times, rates, name):
        """ Constructor for the field class

        Parameters
        ----------
        times:
            Array to store in field timestamps
        rates:
            Array to store in field firingrates
        name:
            A string to identify the field
        """

        self.timestamps = times
        self.firingrates = rates
        self.name = name

    def get_timeseries(self):
        """ A getter function to get the data in a Field instance

        Returns
        -------
        array:
            A 2-row array where first row is timestamps and second row is
            firing rates. 
        """

        times = np.asarray(self.timestamps) - self.timestamps[0]
        return np.vstack((times, self.firingrates)) 

    def __repr__(self):
        """ Pretty print a Field instance """

        N = np.count_nonzero(~np.isnan(self.firingrates))
        return "Data for {x} with length {n}.".format(x=self.name, n=N)

    def __len__(self):
        """Return a tuple (n,m) where n is not np.nan and m is total."""

        N = np.count_nonzero(~np.isnan(self.firingrates))
        M, = self.firingrates.shape 
        
        return N, M


class Neuron:
    """ A class to hold data corresponding to a neuron 

    Parameters
    ----------
    fields: A dictionary with keys that are field names in a neuron and values
            are Field instances. 
    """

    def __init__(self, field_list, dataframe, dtype):
        """ Constructor for the Neuron class 

        Parameters
        ----------
        field_list:
            A list of neuron names from the dataset
        dataframe:
            A pandas dataframe generated from the "*spline.csv" file
        dtype:
            String, either "SPLINE" or not spline (i.e. "CELL")
        """
        self.fields = dict()

        for fieldname in field_list:
            data = dataframe[fieldname]
            if dtype=="SPLINE":
                times = np.asarray(data.keys().tolist())
                rates = data.values
                self.fields[fieldname] = Field(times, rates, fieldname)
            else:
                times = data['timestamps'].values
                rates = data['firingrates'].values
                self.fields[fieldname] = Field(times, rates, fieldname)

            
    def __repr__(self):
        """ Pretty print a Neuron instance"""

        temp = list(self.fields.keys())
        return "A Neuron object with fields: " + ", ".join(temp)

    
    def __len__(self):
        """Print how many fields a Neuron object has"""

        return sum(1 for _ in self.fields.keys())

    
def plot_neurons(neuron_dict):
    """A function to plot the neuronal data one in multiple 3 x 3 grids.

    Parameters
    ----------
    data_dict:
        A dictionary whose keys are the neuron names and values are instances
        of Neuron objects. 

    """

    for name, neuron in neuron_dict.items():
        fig = plt.figure(figsize=(16,16))
        grid = gridspec.GridSpec(ncols=3, nrows=3, figure=fig)
        idxs = [(i,j) for i in range(3) for j in range(3)]
        
        for idx, (field, data) in zip(idxs, neuron.fields.items()):
            ax = fig.add_subplot(grid[idx])
            ax.plot(*data.get_timeseries(), '--o', linewidth=1, markersize=4)
            ax.set_xlabel("Time stamps")
            ax.set_ylabel("Firing rate")
            ax.set_title(field)
            
        fig.suptitle(name)
