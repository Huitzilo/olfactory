# Olfactory
-----------
## Introduction
TBD

The following feature selection methods are available:

* Backward Elimination
* Forward Selection
* Integer Optimization through the Gurobi Solver

The following data-sets are included:

* Hallem, 2006
* DoOR
* dorsal DoOR (subset of DoOR)

## Installation
* If you intend to use Gurobi to solve the optimization problem, you need to download and install Gurobi first (http://gurobi.com).
    * this requires a license (which is free for academical use)
    * check if your paths are set properly, for example for Linux (for more information check: [http://www.gurobi.com/](http://www.gurobi.com/))

          export GUROBI_HOME=/opt/gurobi560/linux64
          export PATH=$PATH:/opt/gurobi560/linux64/bin
          export LD_LIBRARY_PATH=$GUROBI_HOME/lib`

* Switch to your virtualenv. Make sure, you have python27 installed.

* Install the required packages (via pip or easy_install):
    * Flask==0.10.1
    * matplotlib==1.3.1
    * numpy==1.8.0
    * scipy==0.13.1

* Checkout the repository: https://github.com/marcusschroeder/olfactory

* Go to the repo and run: `python test.py`

## General Setup
### virtualenv + Gurobi
If you have downloaded and installed Gurobi, it may be necessary to copy gurobipy from the system site-package to the site-package of the virtualenv to have access to Gurobi without gurobi.sh.

`cp -a /usr/local/lib/python2.7/dist-packages/gurobipy/ /home/<your_dir>/.virtualenvs/<your_env>/lib/python2.7/site-packages/`

Now, switch to your virtualenv and check if the following works without errors:

`python -c "import gurobipy"`

### virtualenv + Gurobi + PyCharm
To get PyCharm to work with virtualenv and Gurobi you have to manually add theLD_LIBRARY_PATH parameter to the run configuration:

            LD_LIBRARY_PATH=/opt/gurobi560/linux64/lib`

Now, you should be able to run Gurobi code from within PyCharm.

## Example: Backward Elimination on dorsal DoOR data-set
In short, odorant receptors (ORs) are connected to glomeruli in the Antenna Lobe (AL) - the olfactory brain - of _Drosophila_.
Some glomeruli are located on the outer surface of AL, the so called dorsal area, which allows one to use optical methods to measure their activity.
The DoOR data-set is a heterogenous data-set, e.g. it combines the results from various studies into one model. The dorsal DoOR data-set is a subset that contains only the responses from dorsal ORs.
For a more detailed explanation check my thesis ---

In this example, I explain how to identify the best odorants based on this dorsal DoOR data-set.

__First__, access the data-set:

        from door.data import DoOR
        door = DoOR()
        data, ors, odorants = door.get_dorsal_data()  # returns response matrix, OR names, odorant names

__Second__, perform backward elimination:

        import featureselection
        feature_list, backward_result = featureselection.backward_elimination(data)

`feature_list` is a sorted list of indices, where the most important odorant can be found at the end.
`backward_result` is a list containing the scores when using the different number of odorants. The higher to score is, the better. With increasing number of odorants, the score increases as well.

__Third__, lets say, you are interested in the six most important features and the score:

        features = 6
        sub_list = feature_list[:-features - 1:-1]

        print "Score:", backward_result[-features - 1]
        >>> Score: 0.076566239434
        print odorants[sub_list]
        >>> ['trans-vaccenic acid' 'Isoamyl acetate' 'Pyrrolidine' 'o-Cresol' 'Ethyl (R)-3-hydroxybutyrate' 'p-Kresol']

The results can then be plotted via:

        import toolbox
        title = 'Backward Elimination of DoOr with %i features' % (features)
        path = "../figures/door/be/door_be_min_" + str(features) + ".png"   # or any path you like
        toolbox.plot_fingerprints(title, odorants[sub_list], data[:, sub_list], ors, path, "DoOR units")

A complete example can be found in `door/be.py` or `hallem/be.py`.