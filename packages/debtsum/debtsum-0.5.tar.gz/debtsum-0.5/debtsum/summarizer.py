import pandas as pd

class Summarizer:

    def __init__(self, filename):
        self.filename = filename

    def summarize(self):
        df = pd.read_csv(self.filename, header=None)
        sum_df = df.groupby([0, 1]).sum().reset_index()
        return sum_df