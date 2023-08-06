from abroca.utils import *
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import sklearn.metrics as metrics
from scipy import interpolate
from scipy import integrate
import matplotlib.pyplot as plt
from sklearn import preprocessing
import sys


def compute_abroca(
    df,
    pred_col,
    label_col,
    protected_attr_col,
    compare_type="overall",
    majority_protected_attr_val=None,
    n_grid=10000,
    plot_slices=False,
    lb=0,
    ub=1,
    limit=1000
):
    # Compute the value of the abroca statistic.
    """
    df - dataframe containing colnames matching pred_col, label_col and protected_attr_col
    pred_col - name of column containing predicted probabilities (string)
    label_col - name of column containing true labels (should be 0,1 only) (string)
    protected_attr_col - name of column containing protected attribute (string)
    compare_type - comparison group being overall, multiple (compare one majority with all classes) or binary
    majority_protected_attr_val(optional) - name of 'majority' group with respect to protected attribute (string)
    n_grid (optional) - number of grid points to use in approximation (numeric) (default of 10000 is more than adequate for most cases)
    plot_slices (optional) - if TRUE, ROC slice plots are generated and saved to file_name (boolean)
    lb (optional) - Lower limit of integration (use -numpy.inf for -infinity) Default is 0
    ub (optional) - Upper limit of integration (use -numpy.inf for -infinity) Default is 1
    limit (optional) - An upper bound on the number of subintervals used in the adaptive algorithm.Default is 1000
    Returns Abroca value
    """
    if df[pred_col].between(0, 1, inclusive=True).any():
        pass
    else:
        print("predictions must be in range [0,1]")
        sys.exit()
    if len(df[label_col].value_counts()) == 2:
        pass
    else:
        print("The label column should be binary")
        sys.exit()
    prot_attr_values = df[protected_attr_col].value_counts().index.values
    fpr_tpr_dict = {}
    slice = {}
    if compare_type == "binary":
        # compute roc within each group of pa_values
        for pa_value in prot_attr_values:
            if pa_value != majority_protected_attr_val:
                minority_protected_attr_val = pa_value
            pa_df = df[df[protected_attr_col] == pa_value]
            fpr_tpr_dict[pa_value] = compute_roc(pa_df[pred_col], pa_df[label_col])

        # compare minority to majority class; accumulate absolute difference btw ROC curves to slicing statistic
        majority_roc_x, majority_roc_y = interpolate_roc_fun(
            fpr_tpr_dict[majority_protected_attr_val][0],
            fpr_tpr_dict[majority_protected_attr_val][1],
            n_grid
        )
        minority_roc_x, minority_roc_y = interpolate_roc_fun(
            fpr_tpr_dict[minority_protected_attr_val][0],
            fpr_tpr_dict[minority_protected_attr_val][1],
            n_grid
        )

        # use function approximation to compute slice statistic via piecewise linear function
        if list(majority_roc_x) == list(minority_roc_x):
            f1 = interpolate.interp1d(
                x=majority_roc_x, y=(majority_roc_y - minority_roc_y)
            )
            f2 = lambda x, acc: abs(f1(x))
            a, _ = integrate.quad(f2, lb, ub, limit)
            slice[pa_value] = a
        else:
            print("Majority and minority FPR are different")
            sys.exit()

        if plot_slices == True:
            slice_plot(
                majority_roc_x,
                minority_roc_x,
                majority_roc_y,
                minority_roc_y,
                majority_group_name="baseline",
                minority_group_name="comparison",
                fout="slice_"
                + majority_protected_attr_val
                + "_"
                + minority_protected_attr_val
                + ".png"
            )

    elif compare_type == "multiple":
        # compute values for majority attribute
        df_major = df[df[protected_attr_col] == majority_protected_attr_val]
        major_auc = compute_auc(df_major[pred_col], df_major[label_col])
        fpr_tpr_dict[majority_protected_attr_val] = compute_roc(
            df_major[pred_col], df_major[label_col]
        )
        majority_roc_x, majority_roc_y = interpolate_roc_fun(
            fpr_tpr_dict[majority_protected_attr_val][0],
            fpr_tpr_dict[majority_protected_attr_val][1],
            n_grid
        )
        for pa_value in prot_attr_values:
            pa_df = df[df[protected_attr_col] == majority_protected_attr_val]
            if pa_value != majority_protected_attr_val:
                minority_protected_attr_val = pa_value
                pa_df = pa_df.append(
                    df[df[protected_attr_col] == minority_protected_attr_val]
                )
                minor_auc = compute_auc(pa_df[pred_col], pa_df[label_col])
                if major_auc > minor_auc:
                    fpr_tpr_dict[pa_value] = compute_roc(
                        pa_df[pred_col], pa_df[label_col]
                    )
                    minority_roc_x, minority_roc_y = interpolate_roc_fun(
                        fpr_tpr_dict[minority_protected_attr_val][0],
                        fpr_tpr_dict[minority_protected_attr_val][1],
                        n_grid
                    )
                    if list(majority_roc_x) == list(minority_roc_x):
                        f1 = interpolate.interp1d(
                            x=majority_roc_x, y=(majority_roc_y - minority_roc_y)
                        )
                        f2 = lambda x, acc: abs(f1(x))
                        a, _ = integrate.quad(f2, lb, ub, limit)
                        slice[pa_value] = a

                    else:
                        print("Majority and minority FPR are different")
                        sys.exit()

                    if plot_slices == True:
                        slice_plot(
                            majority_roc_x,
                            minority_roc_x,
                            majority_roc_y,
                            minority_roc_y,
                            majority_group_name=majority_protected_attr_val,
                            minority_group_name=minority_protected_attr_val,
                            fout="slice_"
                            + majority_protected_attr_val
                            + "_"
                            + minority_protected_attr_val
                            + ".png"
                        )
                    else:
                        print("{} auc is greater than majority auc".format(pa_value))
    elif compare_type == "overall":
        fpr_tpr_dict["overall"] = compute_roc(df[pred_col], df[label_col])
        overall_roc_x, overall_roc_y = interpolate_roc_fun(
            fpr_tpr_dict["overall"][0], fpr_tpr_dict["overall"][1], n_grid
        )
        overall_auc = compute_auc(df[pred_col], df[label_col])
        for pa_value in prot_attr_values:
            minority_protected_attr_val = pa_value
            pa_df = df[df[protected_attr_col] == minority_protected_attr_val]
            minority_auc = compute_auc(pa_df[pred_col], pa_df[label_col])
            if overall_auc > minority_auc:
                fpr_tpr_dict[pa_value] = compute_roc(pa_df[pred_col], pa_df[label_col])
                minority_roc_x, minority_roc_y = interpolate_roc_fun(
                    fpr_tpr_dict[minority_protected_attr_val][0],
                    fpr_tpr_dict[minority_protected_attr_val][1],
                    n_grid
                )
                if list(overall_roc_x) == list(minority_roc_x):
                    f1 = interpolate.interp1d(
                        x=overall_roc_x, y=(overall_roc_y - minority_roc_y)
                    )
                    f2 = lambda x, acc: abs(f1(x))
                    a, _ = integrate.quad(f2, lb, ub, limit)
                    slice[pa_value] = a

                else:
                    print("Majority and minority FPR are different")
                    sys.exit()

                if plot_slices == True:
                    slice_plot(
                        overall_roc_x,
                        minority_roc_x,
                        overall_roc_y,
                        minority_roc_y,
                        majority_group_name="overall",
                        minority_group_name=minority_protected_attr_val,
                        fout="slice_overall_" + minority_protected_attr_val + ".png"
                    )
            else:
                print("{} auc is greater than overall auc".format(pa_value))
    return slice