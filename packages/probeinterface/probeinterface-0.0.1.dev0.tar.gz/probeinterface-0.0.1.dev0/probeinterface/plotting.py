"""
A very first draft of plotting.
Only for debugging purpose at the moment.
"""

# matplotlib is a weak dep
try:
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except ImportError:
    HAVE_MPL = False


def plot_probe(probe, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    
    ax.set_aspect('equal')
    x, y = probe.electrode_positions.T
    ax.scatter(x, y, s=5, marker='o', )

def plot_probe_bunch(probebunch, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    
    ax.set_aspect('equal')
    
    
    
    
    
    
    