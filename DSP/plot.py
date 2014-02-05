import matplotlib.pyplot as plt
from analysis import audio as analysis_audio

class plotter(object):

    @staticmethod
    def generate_plot_for_frequency(data, x_dataset, y_dataset, frequency):
        # Generate 2D plot for frequency of interest based on provided data
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': list,
        #                     'frame_windowed': list,
        #                     'frame_rfft': list,
        #                     'frame_magn': list}, ...]
        #
        #             x_dataset: string
        #             y_dataset: string
        #             frequency: int

        x = []
        y = []
        bin_index = analysis_audio.rfft_map_to_bin(frequency)

        for i in range(len(data)):
            x.append(data[i][x_dataset])
            y.append(data[i][y_dataset][bin_index])

        plt.plot(x, y)
        plt.show(block = False)


