# %%
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from fnmatch import fnmatch
from tabulate import tabulate
from textwrap import fill
from typing import *
import atek
from pathlib import Path
from dateutil.relativedelta import relativedelta as delta
from datetime import date, datetime
import pandas as pd
import re
import toolz.curried as tz
#  import atek
import censusdata
import us


__all__ = (
    "valid_path delta ymd bom eom notebook_setup states counties "
    "state_county period period_display"
).split()


# %%k
def valid_path(path: Union[str, Path]) -> Path:
    """Returns a valid pathlib.Path object or provides smart error message
    indicating which parts are valid (exist) and which parts do not exist."""
    _path = Path(path).expanduser()
    # If expanded path or directory exists then return the expanded path
    if _path.exists():
        return _path

    # If expanded path doesn't exist, return a helpful error message by
    # calculating the good part (exists) of the path and the bad part of
    # path
    temp = _path.parent
    while True:
        if temp.exists():
            bad_part = _path.relative_to(temp)
            raise ValueError(
                f"{_path} does not exist.\n"
                f"Good part = {temp}, \n"
                f"Bad part = {bad_part}"
            )
        temp = temp.parent


# %%
def notebook_setup():
    pd.set_option("display.max_columns", 300)
    pd.set_option("display.max_colwidth", 0)
    pd.set_option("display.max_rows", 1_000)
    pd.set_option("display.min_rows", 300)
    pd.set_option("display.date_yearfirst", True)
    pd.set_option("display.float_format", lambda value: f"{value:,.2f}")
    pd.set_option("display.precision", 2)


# %%
def ymd(dt: Optional[date]=None) -> str:
    """Formats a date as yyyy-mm-dd."""
    dt = dt or date.today()
    return dt.strftime("%Y-%m-%d")


# %%
def bom(dt: Optional[date]=None, months: int=0) -> date:
    """Returns the first day of the month.
    dt -> change day to 1 -> add months."""
    dt = dt or date.today()
    return dt + delta(day=1, months=months)


# %%
def eom(dt: Optional[date]=None, months: int=0) -> date:
    """Returns the last day of the month.
    dt -> change day to 1 -> add months + 1 -> subtract a day."""
    dt = dt or date.today()
    return dt + delta(day=1, months=months+1, days=-1)


# %%k
def states() -> pd.DataFrame:
    """Returns a pandas dataframe of State FIPS codes, abbreviations, and
    state names.

    Data comes from the acs5 2015 census data.
    """
    return tz.pipe(
        censusdata.geographies(
            censusdata.censusgeo([("state", "*")]),
            "acs5",
            2015
        )
        ,lambda d: [
            {
                "State": k,
                "State_FIPS": v.params()[0][1],
                "State_ID": int(v.params()[0][1]),
            }
            for k, v in d.items()
        ]
        ,tz.map(lambda d: tz.assoc(d, "State2", us.states.lookup(d["State"]).abbr))
        ,pd.DataFrame.from_records
    )


# %%
def counties() -> pd.DataFrame:
    """Returns a pandas dataframe of County Names, Cleaned County names.

    Cleaned County Names = Words Borough, Parish, City, County, Census Area,
        Municipality, and Municipio (PR) have been removed.

    Data comes from the acs5 2015 census data.
    """
    return tz.pipe(
        censusdata.geographies(
            censusdata.censusgeo([("state", "*"), ("county", "*")]),
            "acs5",
            2015
        )
        ,lambda d: [
            {
                "County_State": k,
                "State_FIPS": v.params()[0][1],
                "County_FIPS": v.params()[1][1],
                "County_ID": int(v.params()[1][1]),
            }
            for k, v in d.items()
        ]
        ,pd.DataFrame.from_records
        ,lambda df: df
        .assign(**{
            "County_Full": lambda df: df.County_State.str.extract("(^.*)(?=,.)"),
        })
        .assign(**{
            "County": lambda df: df.County_Full.str
                .replace(" County", "")
                .replace(" and Borough", "")
                .replace(" Census Area", "")
                .replace(" Municipality", "")
                .replace(" Borough", "")
                .replace(" Parish", "")
                .replace(" City", "")
                .replace(" Municipio", ""),
            "State_County_FIPS": lambda df: df.apply(lambda row:
                row["State_FIPS"] + row["County_FIPS"],
                axis=1
            ),
            "State_County_ID": lambda df: df.State_County_FIPS.astype("int"),
        })
        .drop(columns=["County_State"])
    )


# %k%
def state_county() -> pd.DataFrame:
    """Combines results of states() and counties() into 1 pandas dataframe.
    Data comes from the acs5 2015 census data.
    """
    return tz.pipe(
        states()
        .merge(counties(), on="State_FIPS", how="left")
        .assign(**{
            "State_County": lambda df: df.apply(lambda row:
                row["State2"] + "|" + row["County"],
                axis = 1,
            ),
        })
    )


# %%
@tz.curry
def period_display(min_fmt: str, max_fmt: str,
    min_date_col: pd.Series, max_date_col: pd.Series) -> pd.Series:
    return min_date_col.dt.strftime(min_fmt) + max_date_col.dt.strftime(max_fmt)


# %%
def period(period_format: str="%Y-%m", period_name: str="", *,
    start: str="2020-01", end: Optional[str]=None,
    period_to_date: bool=False, day_freq: str="D",
    make_table: bool=False, today: str="",
    period_display_func: Optional[Callable]=None,
    ) -> pd.DataFrame:
    """Creates a period dataset. Used to create the period table.str
    period_format is applied using the strftime method.
    display_func is a func that takes the period_min_date and peiod_max_date
        and returns a formatted string representing the period_display column.
    """

    # Create calendar day series and business series
    today = pd.Timestamp.today().date() if today == "" else pd.Timestamp(today)
    end = end or today + pd.DateOffset(day=1, years=1)
    days = pd.date_range(start, end, freq=day_freq)
    period_name = period_format.replace("%", "") if period_name == "" else period_name

    period_display_func = period_display_func or period_display("%m/%d-", "%m/%d")

    return tz.pipe(
        pd.DataFrame({
            "period_date": days,
            "days": 1,
            "today": today,
            "period_name": period_name,
        })

        # Calculate columns
        .assign(**{
            "period": lambda df: df.period_date.dt.strftime(period_format),
            "day3": lambda df: df.period_date.dt.strftime("%a"),
            # If process is run on a Sat and day_freq = "B", date for Today
            # will not be present to use next closest day befor actual today
            "is_today": lambda df: np.where(
                df.query("period_date <= today")
                .period_date.max() == df.period_date, 1, 0),

            # Period to date columns
            "days_of_period": lambda df: df.groupby("period").days
                .transform("cumsum"),
            "days_in_period": lambda df: df.groupby("period").days
                .transform("sum"),
            "remaining_days_in_period": lambda df:
                df.days_in_period - df.days_of_period,
            "period_to_date": lambda df: np.where(
                df.days_of_period <= df.query("is_today == 1")
                    .days_of_period.max(), 1, 0),
        })

        # period_to_date = True, filter by is_bus_days_to_date
        ,lambda df: (df.query("period_to_date == 1") if period_to_date else df)

        # Calculate min, max, start, and end dates for each period
        ,lambda df: df.assign(**{
            "period_min_date": lambda df: df.groupby("period")
                .period_date.transform("min"),
            "period_max_date": lambda df: df.groupby("period")
                .period_date.transform("max"),
            "period_display": lambda df:
                period_display_func(df.period_min_date, df.period_max_date),
                # df.period_min_date.dt.strftime("%m/%d-")
                # + df.period_max_date.dt.strftime("%m/%d"),
            "is_period_start": lambda df: np.where(
                df.period_min_date == df.period_date, 1, 0),
            "is_period_end": lambda df: np.where(
                df.period_max_date == df.period_date, 1, 0),

            # Relative period
            "row_id": lambda df: df.period.rank(method="dense"),
            "rel_period": lambda df: df.row_id - df.query("is_today == 1")
                .row_id.max(),

        })
        .drop(columns=["row_id", "days", "period_to_date"])
    )