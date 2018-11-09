# I put a note in Trello describing these options, but will summarize here.
codec = libx264  # allows control over compression
#`-crf 17`: This selects the constant rate factor mode, which allows for better 
# control over the quality. See here: 
# https://slhck.info/video/2017/03/01/rate-control.html 
# The 17 is for the level of compression. This ranges from 0 to 51. 23 is 
# typical, and 17 should be indistinguishable from no compression at all.
# `-pix_fmt yuv420p`: This selects the pixel format used. I don't know exactly 
# what this does, but it does allow Quicktime to play it, while without this it 
# won't recognize the file. 
codec_flags = -crf 17 -pix_fmt yuv420p
output_filetype = mp4
framerate = 2  # input and output framerate

to_param = params/$(1).txt
to_plots_glob = plots/$(1)_a_0.*.png
to_flag = .finished_$(1).txt
to_output_filename = $(1).$(output_filetype)
to_output = movies/$(call to_output_filename,$(1))

stars_all = stars_all
stars_all_param = $(call to_param,$(stars_all))
stars_all_plots = $(call to_plots_glob,$(stars_all))
stars_all_flag = $(call to_flag,$(stars_all))
stars_all_output = $(call to_output,$(stars_all))
stars_all_output_filename = $(call to_output_filename,$(stars_all))

gas_all = gas_all
gas_all_param = $(call to_param,$(gas_all))
gas_all_plots = $(call to_plots_glob,$(gas_all))
gas_all_flag = $(call to_flag,$(gas_all))
gas_all_output = $(call to_output,$(gas_all))
gas_all_output_filename = $(call to_output_filename,$(gas_all))

gas_neutral = gas_neutral
gas_neutral_param = $(call to_param,$(gas_neutral))
gas_neutral_plots = $(call to_plots_glob,$(gas_neutral))
gas_neutral_flag = $(call to_flag,$(gas_neutral))
gas_neutral_output = $(call to_output,$(gas_neutral))
gas_neutral_output_filename = $(call to_output_filename,$(gas_neutral))

gas_molecular = gas_molecular
gas_molecular_param = $(call to_param,$(gas_molecular))
gas_molecular_plots = $(call to_plots_glob,$(gas_molecular))
gas_molecular_flag = $(call to_flag,$(gas_molecular))
gas_molecular_output = $(call to_output,$(gas_molecular))
gas_molecular_output_filename = $(call to_output_filename,$(gas_molecular))

target_names = $(stars_all_output) $(gas_all_output) $(gas_neutral_output) $(gas_molecular_output)

base_python_file = visualizations_base.py
run_python_file = make_plot.py
py_dependencies = $(base_python_file) $(run_python_file)

centers_file = centers.txt
center_python_file = star_centers.py
copy_plots_file = plot_copy.py

all: $(target_names)

# ------------------------------------------------------------------------------

# Making the visualizations

# ------------------------------------------------------------------------------
$(stars_all_output): $(stars_all_flag)
	python $(copy_plots_file) $(stars_all_output_filename)
	ffmpeg -framerate $(framerate) -pattern_type glob -i '$(stars_all_plots)' -c:v $(codec) $(codec_flags) $(stars_all_output)

$(gas_all_output): $(gas_all_flag)
	python $(copy_plots_file) $(gas_all_output_filename)
	ffmpeg -framerate $(framerate) -pattern_type glob -i '$(gas_all_plots)' -c:v $(codec) $(codec_flags) $(gas_all_output)

$(gas_neutral_output): $(gas_neutral_flag)
	python $(copy_plots_file) $(gas_neutral_output_filename)
	ffmpeg -framerate $(framerate) -pattern_type glob -i '$(gas_neutral_plots)' -c:v $(codec) $(codec_flags) $(gas_neutral_output)

$(gas_molecular_output): $(gas_molecular_flag)
	python $(copy_plots_file) $(gas_molecular_output_filename)
	ffmpeg -framerate $(framerate) -pattern_type glob -i '$(gas_molecular_plots)' -c:v $(codec) $(codec_flags) $(gas_molecular_output)

# ------------------------------------------------------------------------------

# Making the individual plots

# ------------------------------------------------------------------------------
$(stars_all_flag): $(py_dependencies) $(centers_file)
	python $(run_python_file) $(stars_all)

$(gas_all_flag): $(py_dependencies) $(centers_file)
	python $(run_python_file) $(gas_all)

$(gas_neutral_flag): $(py_dependencies) $(centers_file)
	python $(run_python_file) $(gas_neutral)

$(gas_molecular_flag): $(py_dependencies) $(centers_file)
	python $(run_python_file) $(gas_molecular)

# ------------------------------------------------------------------------------

# Doing the star centering

# ------------------------------------------------------------------------------
$(centers_file): $(center_python_file)
	python $(center_python_file)