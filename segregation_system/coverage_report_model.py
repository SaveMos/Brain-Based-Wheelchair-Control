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

    def generateCoverageReport(self):
        """
        Creates a radar bubble plot for the provided prepared sessions.
        Save the plot to the "plots" directory as 'CoverageReport.png'.
        """
        num_features = len(self.features_names) # Get the number of features.

        # Create an array of angles for each feature (equally spaced in a circle).
        angles = np.linspace(0, 2 * np.pi, num_features, endpoint=False).tolist()

        # Add the first angle to the end to close the circle.
        angles += angles[:1]

        # Create the plot.
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Create a density grid for storing how many points are in each region.
        density = np.zeros((num_features, 10))  # 10 bins for the radial dimension.

        # Loop through each PreparedSession to plot the data.
        for session in self.prepared_sessions:
            # Plot the individual bubbles for each feature in each session.
            for i, value in enumerate(session.features):
                # In the radar plot, each feature is in a certain eagle 'i'.
                radius = value  # The radius will be the feature value.
                # radius tells in which position in the ray the bubble will be put.

                # Calculate the radial bin for density.
                # The ray is divided in 10 bins and each bin is relative to a single interval.
                # For example [0.1 , 0.2] is an interval.
                radial_bin = int(np.clip(radius * 10, 0, 9))  # 10 bins (0-1 range).
                # In this case: '0.13' => [0.1 , 0.2] interval => 2nd Bin.

                # Every time a point is in the right area we increment the number of points in that area.
                density[ i , radial_bin] += 1  # Increment the density at this angle (i) and radial bin.
                # So ( i , radial_bin ) identifies the position of the point in the radar.

        density = density / np.max(density) # Normalize the density to [0,1]

        # Loop again to plot bubbles with density-based sizes
        for session in self.prepared_sessions:
            for i, value in enumerate(session.features):
                angle = angles[i] # Angular position (phase).
                radius = value # Radial position (modulus).

                # Retrieve the bin relative to the current bubble.
                radial_bin = int(np.clip(radius * 10, 0, 9))

                bubble_size = density[i, radial_bin] * 100  # Scale the bubble size

                ax.scatter(angle, radius, s=bubble_size, color='lightblue', alpha=0.6)  # Plot the bubble

        # Add concentric rings with labels
        ax.set_rmax(1)  # Set the maximum radius (1 is the default)
        ax.set_rticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Set radial ticks
        ax.set_rlabel_position(40)  # Position the radial labels on the outermost ring
        ax.tick_params(labelsize=8)  # Set the size of the radial labels

        # Enable angular ticks and set their positions at the appropriate angles
        ax.set_xticks(angles[:-1])  # Enable angular ticks at the feature angles
        ax.set_xticklabels(self.features_names, fontsize=8, color='black', weight='bold')  # Labels for the features

        ax.set_title("Coverage Report", size=16, color='black', y=1.1) # Add the title to the plot.

        # Save the plot to the "plots" directory as 'CoverageReport.png'.
        if not os.path.exists('plots'):
            os.makedirs('plots')
        plt.savefig('plots/CoverageReport.png', bbox_inches='tight') # Save the plot into the '.png' file.



