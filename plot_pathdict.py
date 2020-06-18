import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedFormatter, FixedLocator,FormatStrFormatter
from gempy.plot import helpers
import matplotlib.colors as mcolors
import matplotlib.path


def plot_pathdict(pathdict, cdict, extent, ax=None, surflist=['CARBO', 'TRIAS', 'LIAS', 'fault_left', 'fault_right']):
    if ax == None:
        fig, ax = plt.subplots()
    for formation in surflist:
        for path in pathdict.get(formation):
            #print(type(path))
            if path !=[]:
                #print(type(path))
                if type(path) == matplotlib.path.Path:
                    patch = patches.PathPatch(path, fill=False, lw=1, edgecolor=cdict.get(formation, 'k'))
                    ax.add_patch(patch)
                elif type(path) == list:
                    for subpath in path:
                        assert type(subpath == matplotlib.path.Path)
                        patch = patches.PathPatch(subpath, fill=False, lw=1, edgecolor=cdict.get(formation, 'k'))
                    #print('weird')
                        ax.add_patch(patch)
            
            
def prettify_splot(plot, ax, n, labels, pos_list):    
# adjust this
    sname = ['s1','s2','s3','s4'][n]

    a = plot.make_topography_overlay_4_sections(n)
    bound=np.append(a[:-4],np.array([a[:-4][-1],[13000,-3000],[0,-3000],a[:-4][0]])).reshape(-1,2)
    ax[n].fill(a[:,0], a[:,1], 'w', zorder=2, edgecolor='w', linewidth=0.5)
    ax[n].plot(bound[:,0],bound[:,1],'k', zorder=100, linewidth=1.2)
    ax[n].xaxis.set_major_locator(FixedLocator(nbins=len(labels), locs=pos_list))
    ax[n].xaxis.set_major_formatter(FixedFormatter((labels)))
    ax[n].spines['top'].set_visible(False)
    ax[n].spines['left'].set_bounds(900, -3000)
    ax[n].spines['right'].set_bounds(900, -3000)
    
    
def plot_probabilities(plot, block, shape, T = False, extent=None):
    fig, ax = plt.subplots(int(np.ceil(block.shape[0]/2)), 2, figsize=(16, 8))
    ax = ax.flatten()
    print(int(np.ceil(block.shape[0]/2)))
    print(block.shape)
    for i in range(block.shape[0]):
        allcolors = list(plot._color_lot.values())[plot.model.faults.n_faults:]
        formnames = list(plot._color_lot.keys())[plot.model.faults.n_faults:]
        c2 = allcolors[i]
        title = formnames[i]
        cmap = mcolors.LinearSegmentedColormap.from_list('c',['#FFFFFF',c2])
        if T:
            plotblock = block[i].reshape(shape).T
        else:
            plotblock = block[i].reshape(shape)
        im = ax[i].imshow(plotblock, origin='lower', cmap=cmap,
                    extent = extent)
        ax[i].set_title(title)
        helpers.add_colorbar(im, label='probability')