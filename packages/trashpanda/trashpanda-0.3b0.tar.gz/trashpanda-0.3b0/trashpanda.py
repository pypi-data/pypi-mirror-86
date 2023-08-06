#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from typing import (
    Optional,
    List,
    Any,
    Union,
    overload,
    Iterable,
)

# create LOGGER with this namespace's name
import numpy
import pandas
from pandas import DataFrame, Series

_logger = logging.getLogger("trashpanda")
_logger.setLevel(logging.ERROR)
# create console handler and set level to debug
writes_logs_onto_console = logging.StreamHandler()
# add formatter to ch
writes_logs_onto_console.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(name)s - %(module)s - %(funcName)s "
        "- %(lineno)s - %(levelname)s - %(message)s"
    )
)


__version__ = "0.3b0"
__all__ = [
    "get_intersection",
    "add_columns_to_dataframe",
    "override_left_with_right_dataframe",
    "add_missing_indexes_to_series",
    "override_left_with_right_series",
    "add_blank_rows_to_dataframe",
    "cut_dataframe_after",
]


DEFAULT_NA = pandas.NA


@overload
def get_intersection(
    source: DataFrame, targeted_indexes: Union[List, pandas.Index]
) -> DataFrame:
    pass


@overload
def get_intersection(
    source: Series, targeted_indexes: Union[List, pandas.Index]
) -> Series:
    pass


def get_intersection(
    source: Union[DataFrame, Series], targeted_indexes: Union[List, pandas.Index]
) -> Union[DataFrame, Series]:
    """
    Intersects Series or DataFrame by requested indexes. A subsection from the
    *source* is made for the *targeted_indexes*, which must not necessaraly
    be whithin the *source*.

    Args:
        source(Union[DataFrame, Series]):
            Values from which an intersection will be retrieved.

        targeted_indexes(Index):
            The indexes which the returned Series should contain.

    Returns:
        Union[DataFrame, Series]

    Examples:
        >>> from pandas import Series, DataFrame
        >>> sample_series = Series(list(range(3)), index=list(iter("abc")), name="foo")
        >>> get_intersection(sample_series, ["b", "c", "d"])
        b    1
        c    2
        Name: foo, dtype: int64
        >>> get_intersection(sample_series, ["x", "y", "z"])
        Series([], Name: foo, dtype: int64)
        >>> sample_frame = DataFrame(
        ...     list(range(3)), index=list(iter("abc")), columns=["foo"]
        ... )
        >>> get_intersection(sample_frame, ["b", "c", "d"])
           foo
        b    1
        c    2
        >>> get_intersection(sample_frame, ["x", "y", "z"])
        Empty DataFrame
        Columns: [foo]
        Index: []

    """
    existing_indexes = source.index
    possible_indexes = existing_indexes.intersection(targeted_indexes)
    requested_series = source.loc[possible_indexes]
    return requested_series


def add_blank_rows_to_dataframe(
    source_frame: DataFrame,
    indexes_to_add: Union[Iterable, pandas.Index],
    fill_value: Optional[Any] = None,
    override: bool = False,
) -> DataFrame:
    """
    Adds blank rows into the DataFrame with `numpy.nan` by default. Double
    indexes are either overriden if argumend *override* is True or ignored.


    Args:
        source_frame(DataFrame):
            Frame in which additional 'blank' rows should be filled.

        indexes_to_add(Union[Iterable, pandas.Index]):
            The targeted indexes, which are going to be added or overriden.

        fill_value(Optional[Any]):
            Default `numpy.nan`; value which is going to be used as the
            added rows values.

        override(bool):
            States if the *indexes to add* are overriding the source or ignored.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy as np
        >>> from trashpanda import add_blank_rows_to_dataframe
        >>> sample_frame = DataFrame(
        ...     np.arange(6.0).reshape(3, 2), index=[0.1, 0.2, 0.3], columns=["a", "b"]
        ... )
        >>> prepared_frame = add_blank_rows_to_dataframe(
        ...     source_frame=sample_frame, indexes_to_add=[0.15, 0.3, 0.35]
        ... )
        >>> prepared_frame
                a    b
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> prepared_frame.interpolate(method="index", limit_area="inside")
                a    b
        0.10  0.0  1.0
        0.15  1.0  2.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.35  NaN  NaN
        >>> add_blank_rows_to_dataframe(
        ...     source_frame=sample_frame,
        ...     indexes_to_add=[0.15, 0.3, 0.35],
        ...     override=True
        ... )
                a    b
        0.10  0.0  1.0
        0.15  NaN  NaN
        0.20  2.0  3.0
        0.30  NaN  NaN
        0.35  NaN  NaN
        >>> add_blank_rows_to_dataframe(
        ...     source_frame=sample_frame,
        ...     indexes_to_add=[],
        ... )
               a    b
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0

    """
    if fill_value is None:
        fill_value = numpy.nan

    nothing_do_add_just_copy_source = len(indexes_to_add) == 0
    if nothing_do_add_just_copy_source:
        return source_frame.copy()

    column_count = len(source_frame.columns)
    index_count = len(indexes_to_add)

    double_indexes = source_frame.index.intersection(indexes_to_add)

    just_need_to_add = len(double_indexes) == 0
    if just_need_to_add:
        blank_lines = [[fill_value] * column_count] * index_count
        rows_to_add = DataFrame(
            blank_lines,
            index=indexes_to_add,
            columns=source_frame.columns.copy(),
        )
        requested_frame = pandas.concat((source_frame, rows_to_add), axis=0, sort=True)
        requested_frame.sort_index(inplace=True)
        return requested_frame

    ignore_equal_adding_row_indexes_to_source = not override
    if ignore_equal_adding_row_indexes_to_source:
        actual_indexes_to_add = pandas.Index(indexes_to_add).drop(double_indexes)
        blank_lines = [[fill_value] * column_count] * len(actual_indexes_to_add)
        rows_to_add = DataFrame(
            blank_lines,
            index=actual_indexes_to_add,
            columns=source_frame.columns.copy(),
        )
        requested_frame = pandas.concat((source_frame, rows_to_add), axis=0, sort=True)
        requested_frame.sort_index(inplace=True)
        return requested_frame

    blank_lines = [[fill_value] * column_count] * len(indexes_to_add)
    rows_to_add = DataFrame(
        blank_lines,
        index=indexes_to_add,
        columns=source_frame.columns.copy(),
    )
    different_indexes = source_frame.index.difference(double_indexes)
    requested_frame = pandas.concat(
        (source_frame.loc[different_indexes], rows_to_add), axis=0, sort=True
    )
    requested_frame.sort_index(inplace=True)
    return requested_frame


def add_columns_to_dataframe(
    frame_to_enlarge: DataFrame,
    column_names: List[str],
    fill_value: Optional[Any] = None,
) -> DataFrame:
    """
    Adds columns to a dataframe. By default the columns are filled with
    pandas.NA values if no *fill_value* is explizitly given.

    Args:
        frame_to_enlarge(DataFrame):
            pandas.DataFrame which gets additional columns.

        column_names(List[str]):
            Names of additional columns to create.

        fill_value(Optional[Any]):
            Value which will fill the newly created columns. Default pandas.NA

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy
        >>> sample_frame = DataFrame(numpy.arange(4).reshape((2,2)), columns=["a", "b"])
        >>> sample_frame
           a  b
        0  0  1
        1  2  3
        >>> add_columns_to_dataframe(sample_frame, ["c", "d"], "+")
           a  b  c  d
        0  0  1  +  +
        1  2  3  +  +
        >>> add_columns_to_dataframe(sample_frame, ["c", "d"])
           a  b     c     d
        0  0  1  <NA>  <NA>
        1  2  3  <NA>  <NA>
    """
    if fill_value is None:
        fill_value = DEFAULT_NA

    for column_name_to_add in column_names:
        frame_to_enlarge[column_name_to_add] = fill_value
    return frame_to_enlarge


def cut_dataframe_after(
    frame_to_cut: DataFrame, cutting_index: float
) -> DataFrame:
    """
    Cuts a dataframe dropping the part after the cutting index. The cutting
    index will be added to the frame, which values are being interpolated, if inside.

    Args:
        frame_to_cut(DataFrame):
            Source frame to be cut at the cutting index.

        cutting_index(float):
            Cutting index at which the source frame should be cut.

    Returns:
        DataFrame

    Examples:
        >>> import numpy
        >>> from pandas import DataFrame, Series
        >>> sample_frame = DataFrame(
        ...     numpy.arange(6.0).reshape(3, 2), index=[0.1, 0.2, 0.3]
        ... )
        >>> sample_frame
               0    1
        0.1  0.0  1.0
        0.2  2.0  3.0
        0.3  4.0  5.0
        >>> cut_dataframe_after(sample_frame, 0.14)
                0    1
        0.10  0.0  1.0
        0.14  0.8  1.8
        >>> cut_dataframe_after(sample_frame, 0.2)
               0    1
        0.1  0.0  1.0
        0.2  2.0  3.0
        >>> cut_dataframe_after(sample_frame, 0.31)
                0    1
        0.10  0.0  1.0
        0.20  2.0  3.0
        0.30  4.0  5.0
        0.31  NaN  NaN
        >>> cut_dataframe_after(sample_frame, 0.0)
        Empty DataFrame
        Columns: [0, 1]
        Index: []
    """
    if cutting_index <= frame_to_cut.index.min():
        return DataFrame(columns=frame_to_cut.columns.copy())
    if cutting_index in frame_to_cut:
        return frame_to_cut.loc[frame_to_cut.index <= cutting_index].copy()
    prepared_frame = add_blank_rows_to_dataframe(
        source_frame=frame_to_cut, indexes_to_add=[cutting_index]
    )
    interpolated_frame = prepared_frame.interpolate(method="index", axis=0, limit_area="inside")
    return interpolated_frame.loc[interpolated_frame.index <= cutting_index].copy()


def override_left_with_right_dataframe(
    left_target: DataFrame, overriding_right: DataFrame
) -> DataFrame:
    """
    Overrides overlapping items of left with right.

    Args:
        left_target(DataFrame):
            Dataframe which should be overridden.

        overriding_right(DataFrame):
            The new values as frame, which overrides the *left target*.

    Returns:
        DataFrame

    Examples:
        >>> from pandas import DataFrame
        >>> import numpy as np
        >>> left = DataFrame(np.full(3, 1), index=list(iter("abc")), columns=["v"])
        >>> left
           v
        a  1
        b  1
        c  1
        >>> right = DataFrame(np.full(2, 2), index=list(iter("ad")), columns=["v"])
        >>> right
           v
        a  2
        d  2
        >>> override_left_with_right_dataframe(left, right)
           v
        a  2
        b  1
        c  1
        d  2
        >>> double_data = [list(range(1, 3)) for i in range(3)]
        >>> left = DataFrame(double_data, index=list(iter("abc")), columns=["m", "x"])
        >>> left
           m  x
        a  1  2
        b  1  2
        c  1  2
        >>> double_data = [list(range(3, 5)) for i in range(2)]
        >>> right = DataFrame(double_data, index=list(iter("ad")), columns=["x", "m"])
        >>> right
           x  m
        a  3  4
        d  3  4
        >>> override_left_with_right_dataframe(left, right)
           m  x
        a  4  3
        b  1  2
        c  1  2
        d  4  3
        >>> right = DataFrame(double_data, index=list(iter("ad")), columns=["z", "m"])
        >>> right
           z  m
        a  3  4
        d  3  4
        >>> override_left_with_right_dataframe(left, right)
           m    x     z
        a  4  2.0     3
        b  1  2.0  <NA>
        c  1  2.0  <NA>
        d  4  NaN     3

    """
    old_frame = left_target.copy()
    columns_to_add = overriding_right.columns.difference(left_target.columns)
    if not columns_to_add.empty:
        for column_name in columns_to_add:
            old_frame[column_name] = pandas.NA
    targeted_columns = overriding_right.columns
    same_indexes = overriding_right.index.intersection(old_frame.index)
    new_indexes = overriding_right.index.difference(old_frame.index)
    old_frame.loc[same_indexes, targeted_columns] = overriding_right.loc[same_indexes]
    new_rows = overriding_right.loc[new_indexes]
    overridden_frame = pandas.concat([old_frame, new_rows], sort=True)
    return overridden_frame


def add_missing_indexes_to_series(
    target_series: Series, new_indexes: pandas.Index, fill_value: Optional[Any] = None
) -> Series:
    """
    Adds different (missing) indexes to series.

    Args:
        target_series(Series):
            Series in which missing indexes should be added.

        new_indexes(pandas.Index):
            Indexes, which should be in the *target series*.

        fill_value(Optional[Any]):
            An optional fill value for the freshly added items.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Index, Int16Dtype
        >>> import numpy as np
        >>> target = Series(
        ...     np.full(3, 1), index=list(iter("abc")), name="foo", dtype=Int16Dtype()
        ... )
        >>> target
        a    1
        b    1
        c    1
        Name: foo, dtype: Int16
        >>> new_indexes_to_add = Index(list(iter("ad")))
        >>> add_missing_indexes_to_series(target, new_indexes_to_add)
        a       1
        b       1
        c       1
        d    <NA>
        Name: foo, dtype: object
        >>> add_missing_indexes_to_series(target, new_indexes_to_add, "X")
        a    1
        b    1
        c    1
        d    X
        Name: foo, dtype: object

    """
    if fill_value is None:
        fill_value = DEFAULT_NA

    old_series = target_series.copy()
    try:
        missing_indexes = new_indexes.difference(old_series.index)
    except AttributeError:
        raise TypeError("new_indexes must be of pandas.Index type.")
    new_rows = Series([fill_value] * len(missing_indexes), index=missing_indexes)
    overridden_series = pandas.concat([old_series, new_rows], sort=True)
    overridden_series.name = old_series.name
    return overridden_series


def override_left_with_right_series(
    left_target: Series, overriding_right: Series
) -> Series:
    """
    Overrides overlapping items of left with right.

    Args:
        left_target(DataFrame):
            Series which should be overridden.

        overriding_right(DataFrame):
            The new values as Series, which overrides the *left target*.

    Returns:
        Series

    Examples:
        >>> from pandas import Series, Int16Dtype
        >>> import numpy as np
        >>> left = Series(np.full(3, 1), index=list(iter("abc")), dtype=Int16Dtype())
        >>> left
        a    1
        b    1
        c    1
        dtype: Int16
        >>> right = Series(np.full(2, 2), index=list(iter("ad")), dtype=Int16Dtype())
        >>> right
        a    2
        d    2
        dtype: Int16
        >>> override_left_with_right_series(left, right)
        a    2
        b    1
        c    1
        d    2
        dtype: Int16

    """
    old_series = left_target.copy()
    same_indexes = overriding_right.index.intersection(old_series.index)
    new_indexes = overriding_right.index.difference(old_series.index)
    old_series.loc[same_indexes] = overriding_right.loc[same_indexes]
    new_items = overriding_right.loc[new_indexes]
    overridden_series = pandas.concat([old_series, new_items], sort=True)
    return overridden_series


if __name__ == "__main__":
    import doctest

    doctest.testmod()
