import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
from sklearn.decomposition import PCA
from sklearn.manifold import SpectralEmbedding
#from check_dict import check_dict
from sklearn.cluster import KMeans, MeanShift, AffinityPropagation
from sklearn.preprocessing import StandardScaler


inv_mapper = dict(zip([(i, j) for i in range(4) for j in range(8)], range(32)))
mapper = {value: key for key, value in inv_mapper.items()}


class EMG:
    """ Class to hold EMG data. 

        Required initialization values:
    
            name: Subject identifier
            part: Upperarm or Forearm
            side: Left or right
            activity: push or pull
    """

    def __init__(self, name: str, side: str, part: str, activity: str):
        self.name, self.side, self.part = name, side, part
        self.activity = activity
        self.time = None
        self.rampnum = None  # Will store ramp number as integer
        self.forcemoments = None  # `nparray`
        self.emgs = None  # `nparray`

        # Introduced 10/04
        self.modified = False  # Boolean, channels deleted or no?

        # Keep a list of muscles for plotting purposes
        self.muscles = [
            "Middle deltoid",
            "Triceps Brachii Lateral Head",
            "Biceps Brachii",
            "Extensor Carpi Radialis",
            "Flexor Carpi Radialis",
            "Upper Trapezius",
            "Infraspinatus",
            "Latissimus Dorsi",
            "Semitendinosus",
            "Adductor Magnus",
            "Rectus Femoris",
            "Vastus Medialis",
            "Anterior Tibialis",
            "Medial Gastrocnemius",
            "Rectus Abdominus",
            "Erector Spinae",
        ]

        # Map between channel nums and names
        self.chann_names = dict(zip(range(32), self.muscles + self.muscles))

    def __str__(self):
        """ String representation for pretty printing. """
        temp1 = "Subj:\t" + self.name + "\n" + "Side:\t" + self.side
        temp2 = "Part:\t" + self.part + "\n" + "Motion:\t" + self.activity
        return "\n".join((temp1, temp2))

    def __repr__(self):
        """ Short representation useful for debugging. """
        return "_".join((self.name, self.part, self.activity, str(self.rampnum)))

    def pc_compute(self, item):
        data = getattr(self, item)
        if data is None:
            raise AttributeError
        else:
            skpca = PCA() 
            reduced = skpca.fit_transform(data.T)

        return reduced.T, skpca

    def ec_compute(self, item, gamma=None):
        data = getattr(self, item)
        if data is None:
            raise AttributeError
        else:
            n_comp = data.shape[0]
            diffmap = SpectralEmbedding(n_components=n_comp, affinity="rbf",
                                        gamma=gamma)
            evals, reduced = diffmap.fit_transform(data.T)

        return reduced.T, (diffmap.affinity_matrix_, evals)

    def kmeans_compute(self, item, n_clusters):

        data = getattr(self, item)
        if data is None:
            raise AttributeError
        else:
            kmeans = KMeans(n_clusters=n_clusters, n_init=50)
            labels = kmeans.fit_predict(data.T)

        return labels, kmeans


    def plot_emgs(self, num, fig=None):
        """ A function plot all the EMG activations. """

        if self.modified:
#            key = "_".join((self.part, self.activity))
#            rem_channs = [x-1 for x in
#                    check_dict[self.name][key][self.rampnum]]
            skip_idx = [mapper[rc] for rc in self.modified]
        else:
            skip_idx = []

        if fig is None:
            fig = plt.figure(num, figsize=(15,10))

        gs = gridspec.GridSpec(4, 8)
        idxs = [(i, j) for i in range(4) for j in range(8)]
        chann_dict = dict(zip(idxs, self.chann_names.values()))
        
        for idx in skip_idx:
            idxs.remove(idx)

        for idx, chann in zip(idxs, self.emgs):
            ax = plt.subplot(gs[idx])
            ax.plot(self.time, chann)
            ax.set_title(chann_dict[idx])
            ax.set_xlabel("Time (s)")
            ax.set_ylim(-1, 1)

        title = "Ramp {r} EMG data for {sub}'s {s} {p} {a}".format(r=self.rampnum,\
                sub=self.name, s=self.side, p=self.part, a=self.activity)  

        plt.suptitle(title)

        return fig

    def plot_forcemoments(self, num):
        """ A function to plot all the forces/moments. """

        fig = plt.figure(num)
        gs = gridspec.GridSpec(2, 3)
        titles = dict(zip(range(6), ["f-x", "f-y", "f-z", "m-x", "m-y", "m-z"]))

        i = 0
        for j in range(2):
            for k in range(3):
                ax = plt.subplot(gs[j, k])
                ax.plot(self.time, self.forcemoments[i])
                ax.set_xlabel("Time (s)")
                ax.set_title(titles[i])
                i += 1

        title = "Ramp {r} force-moment data for {sub}'s {s} {p}{a}".format(r=self.rampnum,\
                sub=self.name, s=self.side, p=self.part, a=self.activity)  

        plt.suptitle(title)

        return fig
