from argparse import ArgumentParser

parser = ArgumentParser(
    prog='debtsum', 
    usage='%(prog)s [options] path',
    description='Summarizes CSV files containing list of debts. The format sould be a file of 3 columns: the name of the borrower, the name of the creditor and the amount of debt.',
    epilog="Enjoy this program :)"

)

parser.add_argument('File', metavar='file', type=str, help='path to input file')
parser.add_argument('-o', '--output', help='enable the long listing format')