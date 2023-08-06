import pandas as pd
import os
import sys
from .summarizer import Summarizer
from .argparser import parser
import logging

logging.basicConfig(format='%(message)s', level=logging.INFO)

def main():

    args = parser.parse_args()
    
    if not os.path.isfile(args.File):
        logging.error('The path specified does not exist')
        sys.exit()

    result = Summarizer(args.File).summarize()
    if args.output is not None:
        result.to_csv(args.output, header=False, index=False)
        logging.info(f"Summarizations completed successfuly. Results saved in {args.output} :)")
    else:
        logging.info(result.to_string())


if __name__ == '__main__':
    main()