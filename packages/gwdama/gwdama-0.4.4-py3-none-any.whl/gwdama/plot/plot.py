"""
This submodule contains some function to produce nice plots 'out of the box'
"""

import matplotlib.pyplot as plt

def make_hist(data, xlabel='Value', figsize=(10,6), title=None, **kwargs):
    """
    Function to prepare plots.
    """
    
    default_kwgs = {
        'color':'#78909c',
        'bins':'auto',
        'alpha': .6,
        'rwidth': 0.9,
        'density': True
        }
        
    for k, v in default_kwgs.items():
        kwargs[k] = kwargs.get(k, v)
    
    fig, ax = plt.subplots(figsize=figsize)
    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = ax.hist(x=data, **kwargs)
    ax.grid(alpha=0.4)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    if kwargs['density']:
        ax.set_ylabel('Density')
    else:
        ax.set_ylabel('Occurrence')

    return fig

def reshow(fig):
    """This function creates a dummy figure and uses its manager to
    display ``fig``. This is useful whaen you want to show again a
    pyplot Figure object that has been closed.
    """
    plt.close(fig)
    dummy = plt.figure()
    new_manager = dummy.canvas.manager
    new_manager.canvas.figure = fig
    fig.set_canvas(new_manager.canvas)
