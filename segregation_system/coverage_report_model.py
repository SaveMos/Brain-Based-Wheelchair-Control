"""
Author: Saverio Mosti
Creation Date: 2024-12-06
"""

import os
import matplotlib.pyplot as plt
import numpy as np


class CoverageReportModel:
    """
    This class generates a radar bubble plot (polar plot) based on an array of PreparedSession objects.
    It saves the plot in a 'plots' directory as 'CoverageReport.png'.

    Author: Saverio Mosti
    Creation Date: 2024-12-06
    """

    def __init__(self, prepared_sessions):
        """
        Initializes the CoverageReportModel with the provided prepared sessions.

        :param prepared_sessions: List of PreparedSession objects.
        """
        self.prepared_sessions = prepared_sessions
        self.features_names = [
            "PSD Delta Band", "Activity + Scatter", "PSD Beta Band", "PSD Tetha Band",
            "Environment + Scatter", "PSD Alpha Band"
        ]

    import numpy as np
    import matplotlib.pyplot as plt
    import os

    def generateCoverageReport(self):
        """
        Creates a radar bubble plot for the provided prepared sessions.
        """
        # Number of features (6 in this case)
        num_features = len(self.features_names)

        # Create an array of angles for each feature (equally spaced in a circle)
        angles = np.linspace(0, 2 * np.pi, num_features, endpoint=False).tolist()

        # Add the first angle to the end to close the circle
        angles += angles[:1]

        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Create a density grid for storing how many points are in each region
        density = np.zeros((num_features, 10))  # 10 bins for the radial dimension

        # Loop through each PreparedSession to plot the data
        for session in self.prepared_sessions:
            feature_values = session.features + [session.features[0]]  # To close the radar plot

            # Plot the individual points (bubbles) for each feature in each session
            for i, value in enumerate(session.features):
                angle = angles[i]  # Calculate the angle for the feature
                radius = value  # The radius will be the feature value

                # Calculate the radial bin for density
                radial_bin = int(np.clip(radius * 10, 0, 9))  # 10 bins (0-1 range)
                density[i, radial_bin] += 1  # Increment the density at this angle and radial bin

        # Normalize the density to get bubble sizes
        max_density = np.max(density)
        density = density / max_density  # Normalize to a range from 0 to 1

        # Loop again to plot bubbles with density-based sizes
        for session in self.prepared_sessions:
            for i, value in enumerate(session.features):
                angle = angles[i]
                radius = value
                # Calculate bubble size based on density
                radial_bin = int(np.clip(radius * 10, 0, 9))
                bubble_size = density[i, radial_bin] * 1000  # Scale the bubble size

                ax.scatter(angle, radius, s=bubble_size, color='lightblue', alpha=0.6)  # Plot the bubble


        # Add concentric rings with labels
        ax.set_rmax(1)  # Set the maximum radius (1 is the default)
        ax.set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Set radial ticks
        ax.set_rlabel_position(40)  # Position the radial labels on the outermost ring
        ax.tick_params(labelsize=8)  # Set the size of the radial labels

        # Enable angular ticks and set their positions at the appropriate angles
        ax.set_xticks(angles[:-1])  # Enable angular ticks at the feature angles
        ax.set_xticklabels(self.features_names, fontsize=8, color='black', weight='bold')  # Labels for the features

        # Add title
        ax.set_title("Coverage Report", size=16, color='black', y=1.1)

        # Save the plot to the "plots" directory as 'CoverageReport.png'
        if not os.path.exists('plots'):
            os.makedirs('plots')

        plt.savefig('plots/CoverageReport.png', bbox_inches='tight')
        plt.show()



