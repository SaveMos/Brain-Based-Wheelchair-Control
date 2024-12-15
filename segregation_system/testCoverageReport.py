import random

from prepared_session import PreparedSession
from segregation_system.coverage_report_model import CoverageReportModel
from segregation_system.coverage_report_view import CoverageReportView


def generate_random_prepared_session():
    """
    Generates a PreparedSession object with random Feature objects and labels,
    ensuring the features follow a non-uniform distribution.
    """
    session_id = random.randint(1, 100)

    # Generate features using a non-uniform distribution
    features = [min(max(random.normalvariate(0.5, 0.2), 0), 1) for _ in range(6)]  # Normal distribution centered on 0.5

    # Labels could be random choices from a set of labels
    label = random.choice(["Turn Left", "Turn Right", "Move"])  # Random labels for each session

    return PreparedSession(session_id, features, label)


def main():
    """
    Main function to generate the CoverageReportModel with random PreparedSessions
    and generate the radar plot.
    """
     #Generate 100 random prepared sessions
    prepared_sessions = [generate_random_prepared_session() for _ in range(50)]

    # Create the CoverageReportModel with the prepared sessions
    coverage_report = CoverageReportModel(prepared_sessions)
    coverage_report.generateCoverageReport()

    print("Radar bubble plot for CoverageReport generated and saved as 'plots/CoverageReport.png'.")
    cov = CoverageReportView()
    cov.open_coverage_report()

if __name__ == "__main__":
    main()
