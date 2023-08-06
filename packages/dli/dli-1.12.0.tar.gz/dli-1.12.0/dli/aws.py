#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import logging
import operator
import re
from collections import defaultdict
from datetime import timezone, datetime
from typing import Optional, List, Dict, Tuple

from botocore.credentials import RefreshableCredentials
from botocore.session import get_session

from boto3 import Session
from dateutil.parser import isoparse

trace_logger = logging.getLogger('trace_logger')


class SplitString:
    """Field that serializes to a title case string and deserializes
    to a lower case string.
    """
    _re_match = re.compile(
        r'^([\sa-zA-z0-9_-]+)'
        '(<=|<|=|>|>=|!=)((?!<=|<|=|>|>=|!=)'
        r'[\sa-zA-z0-9_-]+)$'
    )

    def __init__(self, val):
        matches = SplitString._re_match.match(val)
        self.valid = True
        if not matches or len(matches.groups()) != 3:
            self.valid = False
            raise ValueError(
                f"Requested partition is invalid: {val}. Partition arguments "
                f"must be alphanumeric separated by an operator, and must "
                f"not be wrapped in special characters like single or double "
                f"quotations."
            )
        else:
            self.partition, self.operator, self.value = matches.groups()

    def as_dict(self):
        if self.valid:
            return {
                'partition': str(self.partition),
                'operator': str(self.operator),
                'value': str(self.value)
            }

        return None


def create_refreshing_session(
    dli_client_session, **kwargs
):
    """
    :param dli_client_session: We must not be closing over the original
    variable in a multi-threaded env as the state can become shared.
    :param kwargs:
    :return:
    """

    def refresh():
        auth_key = dli_client_session.auth_key
        expiry_time = dli_client_session.token_expires_on.replace(
            tzinfo=timezone.utc
        ).isoformat()

        return dict(
            access_key=auth_key,
            secret_key='noop',
            token='noop',
            expiry_time=expiry_time,
        )

    _refresh_meta = refresh()

    session_credentials = RefreshableCredentials.create_from_metadata(
        metadata=_refresh_meta,
        refresh_using=refresh,
        method='noop'
    )

    session = get_session()
    handler = kwargs.pop("event_hooks", None)
    if handler is not None:
        session.register(f'before-send.s3', handler)

    session._credentials = session_credentials
    return Session(
        botocore_session=session,
        **kwargs
    )


def _get_partitions_in_filepath(filepath: str) -> List[List[str]]:
    splits = filepath.split("/")
    return [x.split("=") for x in splits if "=" in x]


def _operator_lookup(op):
    return {
        '<': operator.lt,
        '>': operator.gt,
        '=': operator.eq,
        '<=': operator.le,
        '>=': operator.ge,
        '!=': operator.ne
    }[op]


def eval_logical(oper, field, val):
    return _operator_lookup(oper)(field, val)


def match_partitions(
    file_path: str,
    partitions: Optional[List[str]],
):
    """
    Return True if the path contains the partition(s) provided.

    :param file_path:
    :param partitions:
    :return:
    """
    # Convert from a list of string to a dictionary of partition, operator &
    # value
    query_partitions = [
        potential.as_dict() for potential in
        [
            SplitString(x)
            for x in partitions
        ] if potential.valid
    ]

    return _meets_partition_params(file_path, query_partitions)


def _meets_partition_params(
    file_path: str,
    query_partitions: Optional[List[Dict[str, str]]],
):
    """
    Return True if the path contains the partition(s) provided.

    :param file_path:
    :param query_partitions:
    :return:
    """

    # Copied from Consumption

    if query_partitions is None:
        return True

    # Sanitse the user input.
    for x in query_partitions:
        x['partition'] = x['partition'].strip()

    # Convert Lists of List to Dictionary using dictionary comprehension.
    found_partitions = {
        x[0]: x[1] for x in _get_partitions_in_filepath(file_path)
    }

    filtered = [
        x for x in query_partitions
        if x['partition'] in found_partitions
    ]

    # Example:
    # found_p = dict[(k,v), (k1,v1)] = k:v, k1:v1
    # query_p = [{'partition':'date', 'operator':'<', 'value':'20190102'}]

    for filterable in filtered:
        field = filterable['partition'].strip()
        compare_val = found_partitions[field]
        op = filterable['operator'].strip()
        filter_value = filterable['value'].strip()

        if field.startswith('as_of_'):
            try:
                filter_value_date = isoparse(filter_value)
            except ValueError as e:
                # This means a user has given an invalid date i.e. not in
                # the correct ISO 8601 format for Python datetime.
                raise ValueError(
                    'Was unable to parse the filter value you provided for '
                    'the `as_of_date` into a Python datetime: '
                    f"'{filter_value}', file_path: {file_path}'"
                ) from e

            try:
                compare_val = isoparse(compare_val)
            except ValueError:
                # Can not meet partition params as it not a date
                trace_logger.warning(
                    f'{file_path} is not a valid date.',
                    extra={
                        'file_path': file_path,
                        'filterable': filterable
                    },
                    exc_info=True
                )

                return False

            filter_value = filter_value_date

        match = eval_logical(
            op,
            field=compare_val,
            val=filter_value
        )

        if not match:
            # Short circuit as soon as we fail to match a filter.
            trace_logger.debug(
                f"Excluding file with path '{file_path}' because it "
                f"contains the partitions '{found_partitions}' and the "
                f"user is filtering with '{field}{op}{filter_value}' "
                f"which for this path is {compare_val}'."
            )
            return False

    not_filtered = [
        x for x in query_partitions
        if not x['partition'] in found_partitions
    ]

    if not_filtered:
        # trace_logger.warning(
        #     f"These query partitions '{not_filtered}' were not found as "
        #     f"keys in the S3 path '{file_path}', so we are going to "
        #     'let this file through the filter but either the user has '
        #     'supplied an partition that does not exist or one of the S3 '
        #     'paths does not follow the partition pattern of the first S3 '
        #     'path in this instance.'
        # )
        return False

    return True


def filter_by_load_type_full(
    paths: List[Tuple[str, int]],
    load_type: Optional[str],
) -> List[Tuple[str, int]]:
    """
    This filtering logic only applies to Structured datasets,

    For a Structured dataset, we expect the first common prefix on S3
    to be an `as_of` representing when the data was published.

    If the dataset's load type is "Full Load"
    then return only data from the most recent `as_of` common prefix.
    Else (if the dataset's load type is "Incremental Load" or None),
    then we return data from all as_of common prefixes.

    :param paths: List of tuple of path to data for this dataset on S3 and
        the size on S3.
    :param load_type: Either None, "Incremental Load" or "Full Load"
    :return:  List of tuple of path to data for this dataset on S3 and
        the size on S3.
    """

    trace_logger.debug(
        f"load_type from Catalogue: '{load_type}'",
        extra={
            'load_type': load_type,
        }
    )

    if load_type == 'Full Load':
        as_of_to_paths: dict = defaultdict(list)
        as_of_key: Optional[str] = None
        as_of_warning_shown = False
        for path in paths:
            partitions = {
                k.lower(): v for k, v in dict(
                    _get_partitions_in_filepath(path[0])
                ).items()
            }

            # Partition cannot be filtered out if does not have an
            # `as_of_`. Get the first instance of a key that begins
            # with `as_of_`.
            as_of_key = next(
                (k for k, v in partitions.items()
                 if k.startswith('as_of_')),
                None
            )

            if not as_of_key:
                # Only show the message the first time, otherwise it will
                # spam the logs.
                if not as_of_warning_shown:
                    trace_logger.warning(
                        'as_of_ not in partitions but load type is full, '
                        'so not filtering out this file but will consider it '
                        'in as having the oldest as_of_ possible.',
                        extra={
                            'load_type': load_type,
                            'path': path[0],
                        }
                    )
                    as_of_warning_shown = True

                as_of_to_paths[
                    datetime.min
                ].append(path)
            else:
                # For a `load_type` = `Full Load` dataset, we only want
                # to return the data in the most recent `as_of_`
                # directory. We accumulate a dict of `as_of_` to
                # path, then at the end we know what the latest
                # `as_of_` is and only return those paths.
                as_of_to_paths[
                    isoparse(partitions[as_of_key])
                ].append(path)

        # Return only the paths that belong to the most recent
        # `as_of_`.
        if as_of_to_paths:
            most_recent_as_of = sorted(
                as_of_to_paths.keys()
            )[-1]
            number_of_paths = len(
                as_of_to_paths[most_recent_as_of]
            )
            trace_logger.debug(
                'Load type is full, so returning most recent '
                f"as_of_ key '{as_of_key}': value '{most_recent_as_of}', "
                f"number of paths: '{number_of_paths}'",
            )
            return as_of_to_paths[most_recent_as_of]
        else:
            # Edge case - the `load_type` is `Full Load` but
            # there are zero as_of_ keys, so return and empty list. The
            # code calling this filter will have to return a user
            # friendly error message about there being no files in the
            # dataset.
            # Alternatively, the cache might not be up to date causing
            # the most recent as_of_ to not be in the list.
            trace_logger.warning(
                'Zero as_of_ keys in the partitions but load type is '
                'full. We may have returned some paths that did not '
                'have an as_of_ key in their path. Alternatively, '
                'we may need to wait for the cache to update.',
                extra={
                    'load_type': load_type,
                }
            )
            return []
    else:
        return paths
