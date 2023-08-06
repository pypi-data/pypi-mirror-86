#!python

from itertools import groupby
import pathlib

from nmrglue import pipe
import click
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


default2d = pathlib.Path(__file__).parent / 'hsqc' / 'trosy-fb.ft2'


def contours_by_Imax(data, minI_factor=8., cl_factor=1.2, num_contours=10):
    """Calculate the contours for the plot base on the maximum intensity."""
    
    maxI = data.max()
    minI = maxI / minI_factor

    return [minI * cl_factor ** x for x in range(num_contours)]


def freq_ppm(header, data, debug=False):
    """Generate a 2d for the frequencies of the 2d spectrum in Hz."""
    # Get the spectral widths for the 2 frequency dimensions in Hz
    f1sw = header['FDF1SW']
    f2sw = header['FDF2SW']

    # Get the observed (Larmor) frequencies for each channel in MHz
    f1obs = header['FDF1OBS']
    f2obs = header['FDF2OBS']
    
    # Get the spectral widths in ppm
    f1swppm = f1sw / f1obs
    f2swppm = f2sw / f2obs
       
    # Get the spectral offset in ppm
    f1swoffppm = header['FDF1ORIG'] / f1obs
    f2swoffppm = header['FDF2ORIG'] / f2obs

    # Get the spectral ranges in ppm
    f1rangeppm = (f1swoffppm, f1swoffppm + f1swppm)
    f2rangeppm = (f2swoffppm, f2swoffppm + f2swppm)
    
    # Get the number of points in the f1 (y-axis) and f2 (x-axis)
    # dimensions
    f1npts, f2npts = data.shape
    
    # Calculate the number of ppm per point for each dimension
    f1delta = f1swppm / f1npts
    f2delta = f2swppm / f2npts

    if debug:
        print('f1sw (Hz): {}, f2sw (Hz): {}'.format(f1sw, f2sw))
        print('f1swppm (ppm): {}, f2swppm (Hz): {}'.format(f1swppm, f2swppm))
        print('f1offppm (ppm): {}, f2offppm (ppm): {}'.format(f1swoffppm, f2swoffppm))
        print('f1rangeppm (ppm): {}'.format(f1rangeppm))
        print('f2rangeppm (ppm): {}'.format(f2rangeppm))
    
    # return an numby array for the frequencies in Hz
    f1ppm = np.array([f1rangeppm[1] - float(i) * f1delta for i in range(f1npts)])
    f2ppm = np.array([f2rangeppm[1] - float(i) * f2delta for i in range(f2npts)])
    return np.meshgrid(f2ppm, f1ppm)


def format_isotope(label):
    """Format an isotope string into latex"""
    # Parse the starter numbers
    groups = [list(g) for _,g  in groupby(label, key=lambda c: c.isdigit())]

    if len(groups) > 1:
        number = ''.join(groups[0])
        rest = ''.join([''.join(g) for g in groups[1:]])
        return "$^{{{}}}${}".format(number, rest)
    else:
        return label


def print_header(header):
    """Print information on the header"""
    for key in sorted(header.keys()):
        if key.startswith('FDF3') or key.startswith('FDF4'):
            continue
        print(key, header[key])


@click.command()
@click.argument('filenames', nargs=-1, type=click.Path(exists=True))
@click.option('--dims', required=False, default=(3, 4),
              type=click.Tuple([float, float]),
              help='The figure dimensions (in inches)')
@click.option('--units', required=False, default=('ppm', 'ppm'),
              type=click.Tuple([str, str]),
              help='The units to plot the x- and y-axes (ppm)')
@click.option('--title', required=False, default=None,
              help='The title for the figure')
@click.option('--labels', required=False,
              default=('', ''), type=click.Tuple([str, str]),
              help="The labels for the x- and y-axis")
@click.option('--xlim', required=False,
              default=(None, None), type=click.Tuple([float, float]),
              help="The x-axis limits (in units) to draw the spectrum")
@click.option('--ylim', required=False,
              default=(None, None), type=click.Tuple([float, float]),
              help="The y-axis limits (in units) to draw the spectrum")
@click.option('--ticks', required=False,
              default=(1, 5), type=click.Tuple([float, float]),
              help="The major tick mark interval for the x- and y-axis")
@click.option('--contour-Icutoff', 'ctr_Icutoff', required=False,
              default=0.15, type=float,
              help='The fraction of the maximum intensity to start contours')
@click.option('--contour-levels', 'ctr_levels', required=False,
              default=20, type=int,
              help='The number of contours to draw')
@click.option('--contour-factor', 'ctr_factor', required=False,
              default=1.2, type=float,
              help='The contour multiplicative factor')
@click.option('--contour-map', 'cmap', required=False,
              default='winter', type=str,
              help='The color map to use for drawing the contours')
@click.option('--out', '-o', 'outfile',
              required=False, default=None,
              help="The output filename to save to figure image")
@click.option('--debug', '-d', required=False, default=False, type=bool,
              help="Print debug information to the terminal")
def plot2d(filenames, dims, units, title, labels, xlim, ylim, ticks,
           ctr_Icutoff, ctr_levels, ctr_factor, cmap, outfile,
           debug):
    """Plot a 2d NMR spectrum from NMRPipe format.
    """
    # Setup the figure
    fig = plt.figure(figsize=dims)

    if title is not None:
        plt.title(title)

    # Setup the input spectra
    if len(filenames) == 0:
        filenames = [str(default2d)]

    for filename in filenames:
        header, data = pipe.read(filename)

        # Format the labels
        xlabel_hdr = format_isotope(header['FDF2LABEL'])
        ylabel_hdr = format_isotope(header['FDF1LABEL'])
        
        # Format the axes
        ppm1, ppm2 = freq_ppm(header, data, debug=debug)

        if units[0] is None:
            pass
        else:
            x = ppm1
            xlabel = labels[0] or "{} Frequency (ppm)".format(xlabel_hdr)

        if units[1] is None:
            pass
        else:
            y = ppm2
            ylabel = labels[1] or "{} Frequency (ppm)".format(ylabel_hdr)

        # Set the plot
        cl = contours_by_Imax(data, minI_factor=ctr_Icutoff**-1,
                              cl_factor=ctr_factor, num_contours=ctr_levels)
        cnt = plt.contour(x, y, data, levels=cl, cmap=cmap)

        # Set plot information for the last contour
        axes = cnt.axes

        axes.invert_xaxis()
        axes.set_xlabel(xlabel)
        axes.xaxis.set_major_locator(MultipleLocator(ticks[0]))

        axes.invert_yaxis()
        axes.set_ylabel(ylabel)
        axes.yaxis.set_major_locator(MultipleLocator(ticks[1]))

        # Set the limits
        if not any(i is None for i in xlim):
            print(xlim)
            axes.set_xlim(*xlim)
        if not any(i is None for i in ylim):
            axes.set_ylim(*ylim)


    # Reposition elements
    fig.tight_layout()

    if outfile is None:
        plt.show()
    else:
        plt.savefig(outfile)


if __name__ == '__main__':
    plot2d()