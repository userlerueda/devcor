#!/usr/bin/env python

"""
Author: Nick Russo
Purpose: A test case file for the Database class (Model in MVC).
Used to illustrate Test Driven Development (TDD) and DevOps CI/CD.
"""

import pytest
import requests
from requests.packages import urllib3


@pytest.fixture(name="my_kwargs")
def fixture_my_kwargs():
    """
    Test fixture setup to disable SLL self-signed certificate warnings.
    """
    urllib3.disable_warnings()
    return {
        "url": "https://localhost:5000",
        "verify": False,
        "headers": {"Accept": "text/html"},
    }


def test_get_good_page(my_kwargs):
    """
    Simulate a user navigating to the website with an HTTP GET.
    """
    resp = requests.get(**my_kwargs)
    assert resp.status_code == 200
    assert "Enter account ID" in resp.text


def test_get_bad_page(my_kwargs):
    """
    Simulate a user navigating to an invalid URL with an HTTP GET.
    """
    my_kwargs["url"] = "https://localhost:5000/bad.html"
    resp = requests.get(**my_kwargs)
    assert resp.status_code == 404
    assert "Not Found" in resp.text


def test_post_good_acct(my_kwargs):
    """
    Simulate a user entering a valid account number and clicking "Submit".
    """
    _post_acct(my_kwargs, {"acctid": "ACCT100", "acctbal": "40.00 USD"})
    _post_acct(my_kwargs, {"acctid": "ACCT200", "acctbal": "-10.00 USD"})
    _post_acct(my_kwargs, {"acctid": "ACCT300", "acctbal": "0.00 USD"})


def test_post_bad_acct(my_kwargs):
    """
    Simulate a user entering an invalid account number and clicking "Submit".
    """
    _post_acct(my_kwargs, {"acctid": "luis"})


def _post_acct(my_kwargs, acct):
    """
    Helper function to perform a post request. Takes in the keyword arguments
    (basic site data) and the account data to check.
    """

    my_kwargs["headers"].update({"Content-Type": "application/x-www-form-urlencoded"})
    resp = requests.post(**my_kwargs, data=f"acctid={acct['acctid']}")
    assert resp.status_code == 200

    balance = acct.get("acctbal")
    print(resp.text)
    if balance:
        assert f"Account balance: {balance}" in resp.text
    else:
        assert "Unknown account number" in resp.text
