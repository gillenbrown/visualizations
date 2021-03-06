import yt
yt.funcs.mylog.setLevel(50)
import yt_tools
import numpy as np
import matplotlib
matplotlib.use("Agg")  # for use on SSH
import matplotlib.pyplot as plt

ds_ts = yt.load("/u/home/hliastro/code/ART/data_local/NBm/NBm_200SFE_tidal_writeout/OUT/continuous_a*.art")
halos_dir = "/u/home/gillenb/code/halo_trees/tidal_writeout/rockstar_halos/"

def parse_lengths(ds, length_tuple):
    """Put a length into the appropriate dataset units.

    :param length_tuple: A two item tuple where the first item is a float 
                         holding the value of the length, and the second
                         is a string with the unit."""
    return ds.quan(length_tuple[0], length_tuple[1])

def read_config(name):
    with open("./params/{}.txt".format(name), "r") as in_file:
        params = dict()
        for line in in_file:
            split = line.split("=")
            if len(split) != 2:
                print(name, line)
                raise ValueError("Config file {} must have the format: \n"
                                 "parameter = value.".format(name))
            params[split[0].strip()] = split[1].strip()

    # Make sure the use didn't leave anything out or have extra parameters.
    needed_params = ["field", "cmap", "width", "depth"]
    if len(params) != len(needed_params):
        err_str = "Config file {} must have the needed items: \n"
        err_str += "{}, " * (len(needed_params) - 1)
        err_str += "{}."
        raise ValueError(err_str.format(name, *needed_params))
    for p in needed_params:
        if p not in params:
            print(p, params)
            raise ValueError("{} needed in config file {}".format(p, name))

    # use the name of the file for the name, then parse other params
    params["name"] = name
    params["field"] = tuple([s.strip() for s in params["field"].split(",")])
    params["width"] = params["width"].split()
    params["depth"] = params["depth"].split()
    params["width"][0] = float(params["width"][0])
    params["depth"][0] = float(params["depth"][0])

    cmap = plt.get_cmap(params["cmap"])
    cmap.set_bad(cmap(0))
    params["cm_obj"] = cmap
    
    return params

def read_star_centers():
    centers_dict = dict()
    with open("centers.txt", "r") as in_file:
        for line in in_file:
            if line.startswith("#"):
                continue
            a, x, y, z = line.split()
            center = [float(x), float(y), float(z)] * yt.units.pc
            centers_dict[a] = center

    return centers_dict

def find_projection_axis(ds, halo, center):
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
    a = str(ds.scale_factor)
    center = read_star_centers()[a]  # not the most elegant
    if np.isnan(center[0]):
        center = yt_tools.get_halo_center(largest_halo)

    perp_vector, north_vector = find_projection_axis(ds, largest_halo, center)
    
    return perp_vector, north_vector, center

def make_base_plot(ds, field, width, depth, cm):
    width = parse_lengths(ds, width)
    depth = parse_lengths(ds, depth)
    normal, north, center = plot_basics(ds)
    # Make a smaller data object to hopefully speed up computation. We make
    # it bigger than the projection region to ensure nothing is missed.
    ds_select = ds.disk(center=center, normal=normal, radius=2*width,
                        height=2*depth)

    plot = yt.OffAxisProjectionPlot(ds, fields=field, center=center,
                                    normal=normal, north_vector=north,
                                    width=width, depth=depth,
                                    data_source=ds_select)
    plot.set_cmap(field, cm)
    plot.set_zlim(field, 0.1, 10 ** 3)
    plot.annotate_timestamp(corner='upper_left', redshift=True,
                            draw_inset_box=True)
    plot.set_unit(field, "msun/pc**2")
    return plot
