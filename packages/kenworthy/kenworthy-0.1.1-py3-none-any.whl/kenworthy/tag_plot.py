def tag_plot(axis):
# Written by M. Kenworthy (2015) - kenworthy@strw.leidenuniv.nl
    """tag_plot - adds a filename and timestamp to a plot
       axis - the Axes object you want to add the timestamp to.

       Example:
       >>> fig = plt.figure(figsize=(8,6))
       >>> ax1 = fig.add_subplot(111)
       >>> plt.plot(np.random.random(10))
       >>> tag_plot(ax1)
    """
    import sys, os, datetime

    pathname = os.path.dirname(sys.argv[0])

    tagline = os.path.abspath(pathname) + '/' + \
        sys.argv[0] + ' on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    axis.text(0.99, 0.01, tagline, ha='right', va='bottom', \
        transform=axis.transAxes, color='black', fontsize=14)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib import interactive

    # make a demonstration figure with axes ax1
    fig = plt.figure(figsize=(8,6))
    ax1 = fig.add_subplot(111)
    plt.plot(np.random.random(10))

    # add a timetag to the plot in ax1
    tag_plot(ax1)
    plt.draw()
    plt.show()


