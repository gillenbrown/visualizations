import sys
config_file = sys.path[1]

import visualizations_base as vb

params = vb.read_config(config_file)

for ds in vb.ds_ts:
    a = ds.scale_factor
    print("Making star plots for a={}".format(a))

    stars_plot = vb.make_base_plot(ds=ds, field=params["field"],
                                   width=params["width"], depth=params["depth"],
                                   cm=params["cm_obj"])
    stars_plot.save("plots/{}_a_{:.3f}.png".format(params["name"], a))

with open(".finished_{}.txt".format(params["name"]), "w") as temp_file:
    temp_file.write("This file is for the makefile and has no other use.")