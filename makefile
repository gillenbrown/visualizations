gas_vis = movies/gas.mp4
stars_vis = movies/stars.mp4
target_names = $(gas_vis) $(stars_vis)
python_file = visualizations.py
plots_flag_file = .finished.txt

all: $(target_names)

$(gas_vis): $(plots_flag_file)
	ffmpeg -framerate 2 -pattern_type glob -i 'plots/gas_a_0.*.png' -r 30 $(gas_vis)

$(stars_vis): $(plots_flag_file)
	ffmpeg -framerate 2 -pattern_type glob -i 'plots/stars_a_0.*.png' -r 30 $(stars_vis)
	
$(plots_flag_file): $(python_file)
	python $(python_file)