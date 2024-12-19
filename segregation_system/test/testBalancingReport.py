"""
Author: Saverio Mosti
Creation Date: 2024-12-06
Description: Script to test the BalancingReportModel class by generating a dataset of random values
and creating a histogram plot.
"""

import random
from segregation_system.balancing_report import BalancingReport
from segregation_system.balancing_report_view import BalancingReportView
from segregation_system_configuration import SegregationSystemConfiguration
from segregation_system.balancing_report_model import BalancingReportModel


def generate_random_balancing_report():
    """
    Generates a BalancingReport object with random values for move, turn_left, and turn_right.

    Returns:
        BalancingReport: An instance with random values.
    """
    move = random.randint(0, 5)
    turn_left = random.randint(0, 5)
    turn_right = random.randint(0, 5)
    return BalancingReport(move=move, turn_left=turn_left, turn_right=turn_right)


def main():
    """
    Main function to test the BalancingReportModel.
    """
    # Generate a random BalancingReport dataset
    random_balancing_reports = [generate_random_balancing_report() for _ in range(100)]

    # Calculate aggregated values for the histogram (sum across all 100 reports)
    total_move = sum(report.move for report in random_balancing_reports)
    total_turn_left = sum(report.turn_left for report in random_balancing_reports)
    total_turn_right = sum(report.turn_right for report in random_balancing_reports)

    # Create a single aggregated BalancingReport
    aggregated_report = BalancingReport(
        move=total_move,
        turn_left=total_turn_left,
        turn_right=total_turn_right
    )

    # Define a SegregationSystemConfiguration with a tolerance value
    config = SegregationSystemConfiguration()
    config.configure_parameters()

    # Create the BalancingReportModel
    report_model = BalancingReportModel(aggregated_report, config)

    # Generate and save the histogram
    print("Generating the histogram...")
    report_model.generateBalancingReport()
    print("Histogram saved in 'plots/BalancingReport.png'.")

    report_view = BalancingReportView()
    report_view.open_balancing_report()


if __name__ == "__main__":
    main()
