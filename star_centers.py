import yt_tools
import visualizations_base as vb

with open("centers.txt", "w") as out_file:
    line_fmt = "{:<7}\t{:<15}\t{:<15}\t{:<15}\n"
    out_file.write(line_fmt.format("# a", "x [pc]", "y [pc]", "z [pc]"))
    for ds in vb.ds_ts:
        a = ds.scale_factor
        print("Star centering for a={}".format(a))

        halo_file = yt_tools.find_correct_halo_file(vb.halos_dir, ds)
        hc = yt_tools.make_halo_catalog(halo_file, ds)
        largest_halo = yt_tools.find_largest_halo(hc)
        center = yt_tools.get_halo_center(largest_halo)
        radius = largest_halo.data_object.radius
        j_radius = 0.2 * radius

        gal = yt_tools.galaxy.Galaxy(ds, center, radius=radius, 
                                     j_radius=j_radius)
        gal.centering(accuracy=10)
        
        x, y, z = gal.center.in_units("pc").value
        out_file.write(line_fmt.format(a, x, y, z))
