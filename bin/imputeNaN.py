#!/usr/bin/python3.6

# drop the columns that have NaN and save them to the desired location
def impute(dropme, out, impute_cols):
    import pandas as pd

    datrs = pd.read_csv(dropme)
    outfile = out + dropme.split()[-1:][0]
    imputed = pd.DataFrame()
    for col in impute_cols:
        imputed[col] = datrs[col].fillna(datrs[col].mean())
    print("saving to `", outfile, "'")
    datrs.to_csv(outfile, index=False)





# this runs if this is main
def main():
    import argparse as ap

    parser = ap.ArgumentParser(description='drop some NaNs from the data')
    parser.add_argument('--files', '-f', type=str, nargs='+', dest='files', action = 'store',
                    help="files to clean up")
    parser.add_argument('--out-folder', '-o', dest='outfile_loc', action='store',
                    type=str, nargs=1)
    parser.add_argument('--columns', '-c', dest='impute_cols', type=str, nargs='+',
                    help="the columns to impute with the mean")

    args = parser.parse_args()

    for arg in args.files:
        impute(arg, args.outfile_loc[0], args.impute_cols)



        
# run main iif it's main
if __name__ == "__main__":
    main()