to_param = params/$(1).mp4
to_plots_glob = plots/$(1)_a_0.*.png
to_flag = .finished_$(1).txt
to_output = movies/$(1).mp4

stars_all = stars_all
stars_all_param = $(call to_param,$(stars_all))
stars_all_plots = $(call to_plots_glob,$(stars_all))
stars_all_flag = $(call to_flag,$(stars_all))
stars_all_output = $(call to_output,$(stars_all))

gas_all = gas_all
gas_all_param = $(call to_param,$(gas_all))
gas_all_plots = $(call to_plots_glob,$(gas_all))
gas_all_flag = $(call to_flag,$(gas_all))
gas_all_output = $(call to_output,$(gas_all))

gas_neutral = gas_neutral
gas_neutral_param = $(call to_param,$(gas_neutral))
gas_neutral_plots = $(call to_plots_glob,$(gas_neutral))
gas_neutral_flag = $(call to_flag,$(gas_neutral))
gas_neutral_output = $(call to_output,$(gas_neutral))

gas_molecular = gas_molecular
gas_molecular_param = $(call to_param,$(gas_molecular))
gas_molecular_plots = $(call to_plots_glob,$(gas_molecular))
gas_molecular_flag = $(call to_flag,$(gas_molecular))
gas_molecular_output = $(call to_output,$(gas_molecular))

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
	python $(copy_plots_file) $(stars_all_output)
	ffmpeg -framerate 2 -pattern_type glob -i '$(stars_all_plots)' -r 30 $(stars_all_output)

$(gas_all_output): $(gas_all_flag)
	python $(copy_plots_file) $(gas_all_output)
	ffmpeg -framerate 2 -pattern_type glob -i '$(gas_all_plots)' -r 30 $(gas_all_output)

$(gas_neutral_output): $(gas_neutral_flag)
	python $(copy_plots_file) $(gas_neutral_output)
	ffmpeg -framerate 2 -pattern_type glob -i '$(gas_neutral_plots)' -r 30 $(gas_neutral_output)

$(gas_molecular_output): $(gas_molecular_flag)
	python $(copy_plots_file) $(gas_molecular_output)
	ffmpeg -framerate 2 -pattern_type glob -i '$(gas_molecular_plots)' -r 30 $(gas_molecular_output)

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