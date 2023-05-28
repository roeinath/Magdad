from numpy import std, mean
from matplotlib.pyplot import hist, show, xlabel, ylabel, title, plot, scatter, legend, savefig, clf, gca
from os import mkdir, path
import os
from web_features.tech_miun_temp.estimator_evaluation.helper_functions import delete_not_relevants, open_file_and_save_graph
# draw the average grade of talpions (dashed line), and scatter the grades given by specific evaluator
def scatter_solution_grades_of_maarih_around_the_general_mean(solution_grades, maarihim_names, average_grades, solution_rows_of_talpions, output_path):
    solution_grades_mean = mean(solution_grades)
    for name, grade in zip(maarihim_names, average_grades):
        grades = solution_rows_of_talpions.groupby(["מעריך"]).get_group(name)["מסכם"].array.to_numpy()
        x_values = []
        y_values = []
        for i, item in enumerate(grades):
            x_values.append(i+0.5)
            y_values.append(item)
        plot(x_values, y_values, 'rx', label="your evaluations")
        plot([0, len(grades)], [solution_grades_mean, solution_grades_mean], linestyle="dashed", label="general average")
        title(str(name + " : פיזור הערכות ביחס לממוצע")[::-1])
        # ignore x-axis values
        frame = gca()
        frame.axes.get_xaxis().set_visible(False)
        legend(loc="upper left")
        open_file_and_save_graph(name, output_path, 'grades_scattering')
        clf()
# create histogram of given grades (How many evaluators give this grade ?)
# draw the average grade of talpions and the average grade which given by specific evaluator
def create_histograms_of_grades(solution_grades, maarihim_names, average_grades, output_path):
    solution_grades_mean = mean(solution_grades)
    for name, grade in zip(maarihim_names, average_grades):
        hist(average_grades, bins="auto", histtype="stepfilled")
        xlabel("average grade")
        ylabel("# evaluators")
        title(name[::-1])
        plot([grade, grade], [0, 20], linestyle="dashed", label='your average')
        plot([solution_grades_mean, solution_grades_mean], [0, 20], c="r", linestyle="dashed", label="general average")
        legend(loc="upper left")
        open_file_and_save_graph(name, output_path, 'histogram')
        clf()
# rank each evaluator by the distance of the average grade which he gives, from the average grade of talpions
# the distance measured by factors of std
# 1 - lowest, 6 - highest
def rank_grades_by_std_and_mean(solution_grades, maarihim_names, average_grades, output_path):
    solution_grades_std = std(solution_grades)
    solution_grades_mean = mean(solution_grades)
    with open(os.path.join(output_path,"graded_estimators.txt"),"w+",encoding="utf-8") as f:
        for name, grade in zip(maarihim_names, average_grades):
            if solution_grades_std / 3 > grade - solution_grades_mean > 0:
                f.write(f"{name} : 4\n")
            if 2 * solution_grades_std / 3 > grade - solution_grades_mean > solution_grades_std / 3:
                f.write(f"{name} : 5\n")
            if grade - solution_grades_mean > 2 * solution_grades_std / 3:
                f.write(f"{name} : 6\n")
            if -solution_grades_std / 3 < grade - solution_grades_mean < 0:
                f.write(f"{name} : 3\n")
            if -2 * solution_grades_std / 3 < grade - solution_grades_mean < -solution_grades_std / 3:
                f.write(f"{name} : 2\n")
            if grade - solution_grades_mean < -2 * solution_grades_std / 3:
                f.write(f"{name} : 1\n")

def create_graph_of_academic_average_as_function_of_miun_grade(x_values, y_values, output_path):
    x_values, y_values = delete_not_relevants(x_values, y_values)
    scatter(x_values, y_values)
    xlabel("ציון מסכם במיון"[::-1])
    ylabel("ממוצע אקדמי בהכשרה"[::-1])
    savefig(os.path.join(output_path, f'ממוצע אקדמי בהכשרה כתלות בציון מסכם במיון.png'))
    clf()
