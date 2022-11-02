import logging
import pickle
import numpy as np
import pendulum
import urllib3
import simplejson as json
import pdb  # NOQA
from collections import namedtuple
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
# from features_common.proxyio import ProcessProxy # type: ignore
# from features_common.helpers import to_date_iso8601 # type: ignore
# from .rules_utils.mt_receiver_qr_low_27_whitelist import mt_receiver_qr_low_27_whitelist_list # type: ignore
from functools import partial
import re

from typing import Optional, Dict, Any


parsedt = pendulum.parse
RuleResult = namedtuple('RuleResult', ('action', 'score'))
_fix_dt = partial(re.compile(r':\d(\d{2})Z').sub, r':\1Z')


class LimitTraffic:
    def __init__(self, site:str):
        self.__name__ = 'LimitTraffic'

    def __call__(self, oridoc:Dict[str, Any], action:str, scores:str, rules_dict:str) -> Optional[RuleResult]:

        data = oridoc['data']
        context = data['context']
        if not context:
            return None
        
        if (_input := data.get('input', {})):
            data = _input.get('data')

        if not data:
            return RuleResult('REVIEW', None)
        # industry_id = data.get('industry_id')
        # utility_categ = data.get('utility_categ')
        flow_type = data.get('flow_type')
        config_id = data.get('config_id')

        if flow_type and flow_type != 'MT' or config_id not in ('QRC', 'MTR'):
            return RuleResult('REVIEW', None)

if __name__ == '__main__':
    rule = LimitTraffic('mlbmt')
    data = rule({"data": {"context": "nada"}}, "Hola", "None", "None")
    print(data)