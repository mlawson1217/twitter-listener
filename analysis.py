import pandas as pd

def load_csv(file: str):
    df = pd.read_csv(file, encoding='utf8', delimiter=',')
    return df



if __name__ == "__main__":
    print(load_csv('tweet_output.csv'))
