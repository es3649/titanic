#!/usr/bin/python3.6

# silence warnings from sklearn
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn


"""
MakeForest() takes some parameters and makes a decision tree with them

:param train_X: The training independent variables
:param train_y: The training dependent variable
:param random_state: the random starting state, for reproducibility
    corresponds directly to the eponymous parameter for RandomForestRegressor
:param max_leaves: The maximum number of leaf nodes the trees can/should have
    corresponds directly to the eponymous parameter for RandomForestRegressor

:returns: a trained RandomForestRegressor
"""
def MakeForest(train_X, train_y, random_state=0,max_leaves=512):
    from sklearn.ensemble import RandomForestRegressor
    from numpy import ravel
    dtr = RandomForestRegressor(random_state=random_state, max_leaf_nodes=max_leaves)
    return dtr.fit(train_X, ravel(train_y))

def adjust(some_list):
    from math import floor
    for i in range(0,len(some_list)):
        some_list[i] = floor(.5 + some_list[i])
    
    return some_list





"""
EvalMae() takes a model and some test parameters and gets statistics on
    it's predictions.

:param tree: is the model to predict with and evaluate
    anything with a predict() method
:param test_X: the independent variables on which to predict
:param test_y: the dependent variable to test check against
"""
def EvalMae(tree, test_X, test_y):
    from sklearn.metrics import mean_absolute_error
    preds = tree.predict(test_X)
    return mean_absolute_error(adjust(preds), test_y)


def main():
    import argparse as ap
    parser = ap.ArgumentParser(description="train and evaluate a random forest given certain params")

    # get data paths
    parser.add_argument('--train', '-t', dest='train', action='store',
                    type=str, nargs=1)
    parser.add_argument('--test', '-s', dest='test', action='store',
                    type=str, nargs=1)

    # out file?
    parser.add_argument('--out', '-o', dest='out', action='store',
                    type=str, nargs=1, default="")

    # get tree parameters
    parser.add_argument('--leaves', '-l', dest='leaves', action='store',
                    type=int, nargs='+')
    parser.add_argument('--random_state', '-r', dest='random_state', action='store',
                    type=int, nargs=1)

    # get data info
    parser.add_argument('--dependent', '-d', dest='dep', action='store',
                    type=str, nargs=1)
    parser.add_argument('--independents', '-i', dest='indeps', action='store',
                    type=str, nargs='+')

    args = parser.parse_args()


    import pandas as pd
    # get and separate the training data
    train = pd.read_csv(args.train[0])
    train_X = train[args.indeps]
    train_y = train[args.dep]

    # get and separate the test data
    test = pd.read_csv(args.test[0])
    test_X = test[args.indeps]
    test_y = test[args.dep]

    for l in args.leaves:
        t = MakeForest(train_X, train_y,
            random_state=args.random_state[0], max_leaves=l)
        print("Leaves:", l, "Error:", EvalMae(t, test_X, test_y))
        if args.out != "" and len(args.leaves) == 1:
            preds = t.predict(test_X)
            preds = adjust(preds)
            # print(preds, len(preds))
            passenger_id = test.PassengerId
            test = pd.DataFrame( { "PassengerId" : passenger_id , "Survived" : preds } )
            test = test.astype(int)
            test.to_csv(args.out[0], index=False)



if __name__ == "__main__":
    main()