import sys
import pytest
import inspect
import importlib

from unittest.mock import Mock

# Mock all external modules
sys.modules['features_common.proxyio'] = Mock()
sys.modules['features_common.helpers'] = Mock()
sys.modules['src.rules_utils.mt_receiver_qr_low_27_whitelist'] = Mock()



def test_something():
    data =  {
        "data": {
            "context": []
        }
    }
    rules = list()
    for m in inspect.getmembers(importlib.import_module("src.rule"), inspect.isclass):
        if m[1].__module__ == 'src.rule' and m[0] != "RuleResult":
            rules.append(m[1])

    # Este es el modo de usar las rules después:
    # log = cls('mlbmt')
    # log(data, None, None, None)
    assert rules == []
