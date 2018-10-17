#!/usr/bin/python3.6

# drop the columns that have NaN and save them to the desired location
def dropit(dropme, out):
    import pandas as pd

    datrs = pd.read_csv(dropme)
    datrs = datrs.dropna(axis=0)
    outfile = out + dropme.split()[-1:][0]
    print("saving to `", outfile, "'")
    datrs.to_csv(outfile)





# this runs if this is main
def main():
    import argparse as ap

    parser = ap.ArgumentParser(description='drop some NaNs from the data')
    parser.add_argument('files', type=str, nargs='+',
                    help="files to clean up")
    parser.add_argument('--out-folder', '-o', dest='outfile_loc', action='store',
                    type=str, nargs=1)

    args = parser.parse_args()

    for arg in args.files:
        dropit(arg, args.outfile_loc[0])



        
# run main iif it's main
if __name__ == "__main__":
    main()