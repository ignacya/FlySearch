import json

from matplotlib import pyplot as plt

from analysis.criterion_plotter import CriterionPlotter
from analysis.run_analyser import RunAnalyser
from analysis.utils import load_all_runs_from_a_dir


def print_results(path):
    runs = load_all_runs_from_a_dir(path)
    plotter = CriterionPlotter(runs)
    runs_unaggregated = plotter.aggregate_runs_per_function(
        lambda x: "unaggregated" if "anomaly" not in str(x.object_type).lower() else "anomaly")
    fig, ax = plt.subplots(nrows=1)
    stats = plotter.plot_accuracy_in_aggregated_runs(
        runs_unaggregated,
        ax,
        success_criterion=lambda run: RunAnalyser(run).success_criterion_satisfied(threshold=10, check_claimed=True)
    )
    print(json.dumps(stats, indent=4))
