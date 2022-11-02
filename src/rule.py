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
from features_common.proxyio import ProcessProxy
from features_common.helpers import to_date_iso8601
from .rules_utils.mt_receiver_qr_low_27_whitelist import mt_receiver_qr_low_27_whitelist_list
from functools import partial
import re

parsedt = pendulum.parse
RuleResult = namedtuple('RuleResult', ('action', 'score'))
_fix_dt = partial(re.compile(r':\d(\d{2})Z').sub, r':\1Z')


class LimitTraffic:
    def __init__(self, site):
        self.__name__ = 'LimitTraffic'

    def __call__(self, oridoc, action, scores, rules_dict):

        doc = oridoc.get('data')
        context = doc.get('context')
        if not context:
            return None
        data = doc.get('input', {}).get('data')

        # industry_id = data.get('industry_id')
        # utility_categ = data.get('utility_categ')
        flow_type = data.get('flow_type')
        config_id = data.get('config_id')

        if flow_type and flow_type != 'MT' or config_id not in ('QRC', 'MTR'):
            return RuleResult('REVIEW', None)