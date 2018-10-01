import matplotlib
matplotlib.use("Agg")  # for use on SSH

import yt
yt.funcs.mylog.setLevel(50)
from matplotlib import animation
from yt.analysis_modules.halo_analysis.api import HaloCatalog
import yt_tools
from matplotlib import cm
from matplotlib import colors

import betterplotlib as bpl
bpl.presentation_style()

ds_ts = yt.load("/u/home/hliastro/code/ART/data_local/NBm/NBm_200SFE_tidal_writeout/OUT/continuous_a*.art")
halos_dir = "/u/home/gillenb/code/halo_trees/tidal_writeout/rockstar_halos/"

stars_cm = cm.copper
gas_cm = cm.viridis

stars_cm.set_bad(stars_cm(0))
gas_cm.set_bad(gas_cm(0))

def find_projection_axis(ds, halo):
    center = yt_tools.get_halo_center(halo)
    
    half_virial_sphere = ds.sphere(center=center,
                                   radius=0.2*halo.data_object.radius)
    x = half_virial_sphere[('STAR', 'particle_position_relative_x')]
    y = half_virial_sphere[('STAR', 'particle_position_relative_y')]
    z = half_virial_sphere[('STAR', 'particle_position_relative_z')]
    m = half_virial_sphere[('STAR', 'MASS')]
    
    axis_ratios_object = yt_tools.AxisRatios(x, y, z, m)
    
    perpendicular_vector = axis_ratios_object.c_vec
    north_vector = axis_ratios_object.a_vec
    if perpendicular_vector is None:
        perpendicular_vector = [1, 0, 0]
    if north_vector is None:
        north_vector = [0, 1, 0]
    return perpendicular_vector, north_vector

def plot_basics(ds):
    halo_file = yt_tools.find_correct_halo_file(halos_dir, ds)
    hc = yt_tools.make_halo_catalog(halo_file, ds)
    largest_halo = yt_tools.find_largest_halo(hc)
    data_object = largest_halo.data_object
    center = yt_tools.get_halo_center(largest_halo)
    
    perp_vector, north_vector = find_projection_axis(ds, largest_halo)
    
    return perp_vector, north_vector, center

def make_base_plot_gas(ds):
    normal, north, center = plot_basics(ds)
    
    field = "density"
    width = (50, "kpc")
    depth = (10, "kpc")

    plot = yt.OffAxisProjectionPlot(ds, fields=field, center=center, 
                                    normal=normal, north_vector=north,
                                    width=width, depth=depth)
    plot.set_cmap(field, gas_cm)
    plot.set_zlim(field, 0.1, 10**3)
    plot.annotate_timestamp(corner='upper_left', redshift=True, draw_inset_box=True)
    plot.set_unit(field, "msun/pc**2")
    return plot

def make_base_plot_stars(ds):
    normal, north, center = plot_basics(ds)
    
    field = ('deposit', 'STAR_density')
    width = (50, "kpc")
    depth = (10, "kpc")

    plot = yt.OffAxisProjectionPlot(ds, fields=field, center=center, 
                                    normal=normal, north_vector=north,
                                    width=width, depth=depth)
    plot.set_cmap(field, stars_cm)
    plot.set_zlim(field, 0.1, 10**3)
    plot.annotate_timestamp(corner='upper_left', redshift=True, draw_inset_box=True)
    plot.set_unit(field, "msun/pc**2")
    return plot

for ds in ds_ts:
    gas_plot = make_base_plot_gas(ds)
    stars_plot = make_base_plot_stars(ds)
    
    a = ds.scale_factor
    print("Making plots for a={}".format(a))
    
    gas_plot.save("plots/gas_a_{:.3f}.png".format(a))
    stars_plot.save("plots/stars_a_{:.3f}.png".format(a))

with open(".finished.txt", "w") as temp_file:
    temp_file.write("This file is for the makefile and has no other use.")
