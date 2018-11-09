import yt_tools
import sys
config_file = sys.argv[1]

import visualizations_base as vb

params = vb.read_config(config_file)

for ds in vb.ds_ts:
    yt_tools.add_species_fields(ds)
    a = ds.scale_factor
    print("Making star plots for a={}".format(a))
    plot = vb.make_base_plot(ds=ds, field=params["field"],
                             width=params["width"], depth=params["depth"],
                             cm=params["cm_obj"])
    # ffmpeg needs the image to have an even number of pixels in both directions
    # to make the plot viewable by quicktime. I'll check the dimensions I 
    # expect the plot to have.
    figwidth  = plot.plots[params["field"]].figure.get_figwidth()
    figheight = plot.plots[params["field"]].figure.get_figheight()
    if np.isclose(figheight, 10.85) and np.isclose(figheight, 9.2):
        # if these dimensions are correct, we know that a dpi of 200 will work,
        # but 400 will be even better.
        plot.save("plots/{}_a_{:.3f}.png".format(params["name"], a),
                        mpl_kwargs={"dpi":400})
    else:
        raise RuntimeError("Plot is wrong size")
    

with open(".finished_{}.txt".format(params["name"]), "w") as temp_file:
    temp_file.write("This file is for the makefile and has no other use.")
