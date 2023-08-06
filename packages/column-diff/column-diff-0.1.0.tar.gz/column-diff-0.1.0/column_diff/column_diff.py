#!/usr/bin/env python3

import pandas as pd
import os


def blacklist(path: str, header: bool = None, *args, **kwargs):
    df = pd.read_excel(path, header=header, *args, **kwargs)
    return df[~df.iloc[:, 1].isin(df.iloc[:, 0])].iloc[:, [1]].reset_index(drop=True)


def _derive_output_path(input_path):
    return os.path.join(
        os.path.dirname(input_path), "filtered_" + os.path.basename(input_path)
    )


def filter_file(input_path: str, output_path: str = None):
    if output_path is None:
        output_path = _derive_output_path(input_path)
    out = blacklist(input_path)
    out.to_excel(output_path, index=False, header=False)
