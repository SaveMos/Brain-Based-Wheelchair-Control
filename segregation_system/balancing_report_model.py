"""
Author: Saverio Mosti
Creation Date: 2024-12-06
"""

import os
import matplotlib.pyplot as plt
from segregation_system.segregation_system_configuration import SegregationSystemConfiguration
from segregation_system.balancing_report import BalancingReport

class BalancingReportModel:
    """
    A model that generates a histogram from a BalancingReport object,
    adds a tolerance line, and saves the plot to a file.

    Attributes:
        balancing_report (BalancingReport): The report to generate the histogram from.
        segregation_config (SegregationSystemConfiguration): The configuration to get the tolerance value.

    Author: Saverio Mosti

    Creation Date: 2024-12-06
    """

    def __init__(self, balancing_report: BalancingReport, segregation_config: SegregationSystemConfiguration):
        """
        Initializes the BalancingReportModel with the provided balancing report and configuration.

        Args:
            balancing_report (BalancingReport): The balancing report object containing move, turn_left, and turn_right values.
            segregation_config (SegregationSystemConfiguration): The segregation system configuration to access tolerance.
        """
        self.balancing_report = balancing_report
        self.segregation_config = segregation_config

    def generateBalancingReport(self):
        """
        Generates and saves a histogram for the balancing report, with a tolerance line above the median bar.
        The histogram is saved as 'BalancingReport.png' in a 'plots' directory.
        """
        # Extract the data from the balancing report
        data = [self.balancing_report.move, self.balancing_report.turn_left, self.balancing_report.turn_right]
        labels = ['Move', 'Turn Left', 'Turn Right']

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Create the histogram
        ax.bar(labels, data, color=['blue', 'green', 'red'])

        # Calculate the median value
        median_value = sorted(data)[1]

        # Get the tolerance value from the configuration
        tolerance = self.segregation_config.tolerance_interval

        # Add the tolerance line at the median value + tolerance
        ax.axhline(median_value + tolerance, color='purple', linestyle='--', label=f'Tolerance: {tolerance}')

        # Add labels and title
        ax.set_xlabel('Actions')
        ax.set_ylabel('Frequency')
        ax.set_title('Balancing Report Histogram')

        # Add a legend
        ax.legend()

        # Create the 'plots' directory if it does not exist
        os.makedirs('plots', exist_ok=True)

        # Save the plot as an image
        plt.savefig('plots/BalancingReport.png')

        # Show the plot (optional)
        plt.show()
