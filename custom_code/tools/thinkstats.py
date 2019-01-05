"""This file is code copied from ..code

Ideally this will not be necessary as I work through the book.
For now I will occasionally copy code to get started a bit faster 
and keep the motivation high.
"""

import re

import numpy as np
import pandas

TYPE_MAP = dict(byte=int, int=int, long=int, float=float, double=float)
STATA_DCT_REGEX = r'_column\((?P<start>\w+)\)\s+(?P<type>\w+)\s+(?P<name>\w+)\s+\S(?P<fstring>\w+)+\s+"(?P<description>[\w+\s\w+]*)"*'
PREG_COLUMN_LIST = [
    "caseid",
    "prglngth",
    "outcome",
    "pregordr",
    "birthord",
    "birthwgt_lb",
    "birthwgt_oz",
    "totalwgt_lb",
    "agepreg",
    "finalwgt",
]
STATA_DCT_FILENAME = "2002FemPreg.dct"
STATA_DATA_FILENAME = "2002FemPreg.dat.gz"


def trim_df_to_columns(df, columns=PREG_COLUMN_LIST):
    if not columns:
        return df
    return df[columns]


def parse_type_info(type_info):
    """Translate type info from stata dict to python.
    """

    if "str" in type_info:
        return str
    else:
        return TYPE_MAP[type_info]


def read_stata_dct(dct_file):
    """Read stata dictionary file.

    Read info describing the stata data file.
    """

    with open(dct_file, "r") as f:
        var_info = []
        for line in f:
            match = re.search(STATA_DCT_REGEX, line)
            if match:
                column_info = (
                    int(match.group("start")),
                    parse_type_info(match.group("type")),
                    str(match.group("name")).lower(),
                    "%" + str(match.group("fstring")),
                    str(match.group("description")).lower(),
                )
                var_info.append(column_info)

        columns = ["start", "type", "name", "fstring", "desc"]
        variables = pandas.DataFrame(var_info, columns=columns)

        # fill in the end column by shifting the start column
        variables["end"] = variables.start.shift(-1)
        variables.loc[len(variables) - 1, "end"] = 0

        dct = FixedWidthVariables(variables, index_base=1)
        return dct


class FixedWidthVariables:
    """Represents a set of variables in a fixed width file."""

    def __init__(self, variables, index_base=0):
        """Initializes.

        variables: DataFrame
        index_base: are the indices 0 or 1 based?

        Attributes:
        colspecs: list of (start, end) index tuples
        names: list of string variable names
        """
        self.variables = variables

        # note: by default, subtract 1 from colspecs
        self.colspecs = variables[["start", "end"]] - index_base

        # convert colspecs to a list of pair of int
        self.colspecs = self.colspecs.astype(np.int).values.tolist()
        self.names = variables["name"]

    def read_fixed_width(self, filename, **options):
        """Reads a fixed width ASCII file.

        filename: string filename

        returns: DataFrame
        """
        df = pandas.read_fwf(
            filename, colspecs=self.colspecs, names=self.names, **options
        )
        return df


def read_fem_preg(
    dct_file="data/2002FemPreg.dct",
    dat_file="data/2002FemPreg.dat.gz",
    compression="gzip",
    clean=True,
):
    """Reads the NSFG pregnancy data.

    dct_file: string file name
    dat_file: string file name

    returns: DataFrame
    """
    dct = read_stata_dct(dct_file)
    df = dct.read_fixed_width(dat_file, compression=compression)

    if clean:
        clean_fem_preg(df)

    return df


def clean_fem_preg(df):
    """Recodes variables from the pregnancy frame.

    df: DataFrame
    """
    # mother's age is encoded in centiyears; convert to years
    df.agepreg /= 100.0

    # birthwgt_lb contains at least one bogus value (51 lbs)
    # replace with NaN
    df.loc[df.birthwgt_lb > 20, "birthwgt_lb"] = np.nan

    # replace 'not ascertained', 'refused', 'don't know' with NaN
    na_vals = [97, 98, 99]
    df.birthwgt_lb.replace(na_vals, np.nan, inplace=True)
    df.birthwgt_oz.replace(na_vals, np.nan, inplace=True)
    df.hpagelb.replace(na_vals, np.nan, inplace=True)

    df.babysex.replace([7, 9], np.nan, inplace=True)
    df.nbrnaliv.replace([9], np.nan, inplace=True)

    # birthweight is stored in two columns, lbs and oz.
    # convert to a single column in lb
    # NOTE: creating a new column requires dictionary syntax,
    # not attribute assignment (like df.totalwgt_lb)
    df["totalwgt_lb"] = df.birthwgt_lb + df.birthwgt_oz / 16.0

    # due to a bug in ReadStataDct, the last variable gets clipped;
    # so for now set it to NaN
    df.cmintvw = np.nan


def read_female_respondents_data(
    dct_file="data/2002FemResp.dct",
    dat_file="data/2002FemResp.dat.gz",
    nrows=None,
    compression="gzip",
    clean=True,
):
    """Reads the NSFG respondent data.

    dct_file: string file name
    dat_file: string file name

    returns: DataFrame
    """
    dct = read_stata_dct(dct_file)
    df = dct.read_fixed_width(dat_file, compression=compression, nrows=nrows)

    if clean:
        clean_female_respondents_df(df)

    return df


def clean_female_respondents_df(df):
    """Recodes variables from the respondent frame.

    df: DataFrame
    """
    pass


def get_trimmed_and_cleaned_dataframe(data_path="data", columns=None):
    df_total = read_fem_preg(
        dct_file=data_path + "/" + STATA_DCT_FILENAME,
        dat_file=data_path + "/" + STATA_DATA_FILENAME,
    )
    return trim_df_to_columns(df_total, columns)


def get_live_fatal_first_other_births(df):
    live = df[df["outcome"] == 1]
    fatal = df[df["outcome"] != 1]
    first = live[live["birthord"] == 1]
    other = live[live["birthord"] != 1]
    return live, fatal, first, other
