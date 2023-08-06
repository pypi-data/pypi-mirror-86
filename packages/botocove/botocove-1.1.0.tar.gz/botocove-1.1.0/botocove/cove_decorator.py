import asyncio
import functools
import logging
from concurrent import futures
from functools import partial
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import boto3
from boto3.session import Session
from botocore.config import Config

from botocove.cove_session import CoveSession

logger = logging.getLogger(__name__)

DEFAULT_ROLENAME = "OrganizationAccountAccessRole"

config = Config(max_pool_connections=20)

# TODO boto3 types - s/Any/mypy_boto3 types


def _get_cove_session(
    org_client: Any,
    sts_client: Any,
    account_id: str,
    rolename: str,
    org_master: bool,
) -> CoveSession:
    role_arn = f"arn:aws:iam::{account_id}:role/{rolename}"
    if org_master:
        account_details = org_client.describe_account(AccountId=account_id)["Account"]
    else:
        account_details = {"Id": account_id}
    cove_session = CoveSession(account_details)
    try:
        logger.debug(f"Attempting to assume {role_arn}")
        creds = sts_client.assume_role(RoleArn=role_arn, RoleSessionName=rolename)[
            "Credentials"
        ]
        cove_session.initialize_boto_session(
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
        )
    except Exception as e:
        cove_session.store_exception(e)

    return cove_session


def _get_org_accounts(
    org_client: Any, sts_client: Any, ignore_ids: Optional[List[str]]
) -> Set[str]:
    calling_account: Set = {sts_client.get_caller_identity()["Account"]}
    accounts_to_ignore = set(calling_account)

    if ignore_ids:
        accounts_to_ignore = set(ignore_ids) | accounts_to_ignore
    logger.info(f"{accounts_to_ignore=}")
    all_org_accounts = (
        org_client.get_paginator("list_accounts")
        .paginate()
        .build_full_result()["Accounts"]
    )

    active_accounts = {
        acc["Id"] for acc in all_org_accounts if acc["Status"] == "ACTIVE"
    }

    target_accounts = active_accounts - accounts_to_ignore
    return target_accounts


async def _get_account_sessions(
    org_client: Any,
    sts_client: Any,
    rolename: str,
    accounts: Set[str],
    org_master: bool,
) -> List[CoveSession]:
    with futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                _get_cove_session,
                org_client,
                sts_client,
                account_id,
                rolename,
                org_master,
            )
            for account_id in accounts
        ]
    sessions = await asyncio.gather(*tasks)
    return sessions


def wrap_func(
    func: Callable,
    raise_exception: bool,
    account_session: Session,
    *args: Any,
    **kwargs: Any,
) -> Dict[str, Any]:
    # Wrapper capturing exceptions and formatting results
    try:
        result = func(account_session, *args, **kwargs)
        return account_session.format_cove_result(result)
    except Exception as e:
        if raise_exception is True:
            account_session.store_exception(e)
            logger.exception(account_session.format_cove_error())
            raise
        else:
            account_session.store_exception(e)
            return account_session.format_cove_error()


async def _async_boto3_call(
    valid_sessions: List[CoveSession],
    raise_exception: bool,
    func: Callable,
    *args: Any,
    **kwargs: Any,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    with futures.ThreadPoolExecutor() as executor:
        loop = asyncio.get_running_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                partial(
                    wrap_func, func, raise_exception, account_session, *args, **kwargs
                ),
            )
            for account_session in valid_sessions
        ]

    completed = await asyncio.gather(*tasks)
    successful_results = [
        result for result in completed if not result.get("ExceptionDetails")
    ]
    exceptions = [result for result in completed if result.get("ExceptionDetails")]
    return successful_results, exceptions


def cove(
    _func: Optional[Callable] = None,
    *,
    target_ids: Optional[List[str]] = None,
    ignore_ids: Optional[List[str]] = None,
    rolename: Optional[str] = None,
    assuming_session: Optional[Session] = None,
    raise_exception: bool = False,
    org_master: bool = True,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Dict[str, Any]:
            #  Check type of ignore_ids for safety
            if ignore_ids:
                if not isinstance(ignore_ids, list):
                    raise TypeError("ignore_ids must be a list of account IDs")
                for account_id in ignore_ids:
                    if len(account_id) != 12:
                        raise TypeError(
                            "All ignore_id in list must be 12 character strings"
                        )
                    if not isinstance(account_id, str):
                        raise TypeError("All ignore_id list entries must be strings")

            # If undefined, use credentials from boto3 credential chain
            if not assuming_session:
                logger.info("No Boto3 session argument: using credential chain")
                sts_client = boto3.client("sts", config=config)
                org_client = boto3.client("organizations", config=config)
            # Use boto3 session supplied as arg
            else:
                logger.info(f"Using provided Boto3 session {assuming_session}")
                sts_client = assuming_session.client("sts")
                org_client = assuming_session.client("organizations")

            # Create a set of account ID's to run function against
            if not target_ids:
                account_ids = _get_org_accounts(org_client, sts_client, ignore_ids)
            elif ignore_ids:
                account_ids = set(target_ids) - set(ignore_ids)
            else:
                account_ids = set(target_ids)

            if not account_ids:
                raise ValueError(
                    "There are no eligible account ids to run decorated func "
                    f"{func.__name__} against"
                )
            # Role to assume in each account
            if not rolename:
                # If undefined, use default AWS organization role
                role_to_assume = DEFAULT_ROLENAME
            else:
                # Use supplied role name
                role_to_assume = rolename

            logger.info(
                f"Running func {func.__name__} against accounts passing arguments: "
                f"{role_to_assume=} {target_ids=} {ignore_ids=} {assuming_session=}"
            )
            logger.debug(f"accounts targeted are {account_ids}")

            sessions = asyncio.run(
                _get_account_sessions(
                    org_client, sts_client, role_to_assume, account_ids, org_master
                )
            )
            valid_sessions = [
                session for session in sessions if session.assume_role_success is True
            ]
            invalid_sessions = [
                session.format_cove_error()
                for session in sessions
                if session.assume_role_success is False
            ]

            if invalid_sessions:
                logger.warning("Could not assume role into these accounts:")
                for invalid_session in invalid_sessions:
                    logger.warning(invalid_session)
                invalid_ids = [failure["Id"] for failure in invalid_sessions]
                logger.warning(
                    f"\n\nInvalid session Account IDs as list: {invalid_ids}"
                )

            if not valid_sessions:
                raise ValueError("No accounts are accessible: check logs for detail")

            results, exceptions = asyncio.run(
                _async_boto3_call(
                    valid_sessions, raise_exception, func, *args, **kwargs
                )
            )
            return {
                "Results": results,
                "Exceptions": exceptions,
                "FailedAssumeRole": invalid_sessions,
            }

        return wrapper

    # Handle both bare decorator and with argument
    if _func is None:
        return decorator
    else:
        return decorator(_func)
