#import os

import subprocess
#import numpy as np
import pytest
#import xarray as xr
#from roocs_utils.exceptions import InvalidParameterValue
#from roocs_utils.exceptions import MissingParameterValue
#from roocs_utils.parameter import area_parameter
#from roocs_utils.parameter import collection_parameter
#from roocs_utils.parameter import time_parameter
#from roocs_utils.parameter.param_utils import level_interval
#from roocs_utils.parameter.param_utils import level_series
#from roocs_utils.parameter.param_utils import time_components
#from roocs_utils.parameter.param_utils import time_interval
#from roocs_utils.parameter.param_utils import time_series
#from roocs_utils.utils.file_utils import FileMapper
#
#from daops import CONFIG
from daops.ops.subset import subset
from tests._common import CMIP5_DAY
#from tests._common import CMIP5_TAS_FPATH
#from tests._common import CMIP6_DAY
#from tests._common import CMIP6_MONTH
#from tests._common import MINI_ESGF_MASTER_DIR
#

month_names = 'jan feb mar apr may jun jul aug sep oct nov dec'.split()

def tc_str(months=None, days=None, use_names=False):
    tcs = []
    if months:
        if use_names:
            tcs.append(('months', [month_names[n-1] for n in months]))
        else:
            tcs.append(('months', months))
    if days:
        tcs.append(('days', days))
    return '|'.join(f"{key}:{','.join(str(val) for val in vals)}" for key, vals in tcs)


@pytest.mark.online
def test_cli_by_time_interval_and_components_month_day(tmpdir, load_esgf_test_data):
    ys, ye = 2007, 2010
    months = [3, 4, 5]
    days = [5, 6]
    
    ti = f"{ys}-12-01T00:00:00,{ye}-11-30T23:59:59"

    tc1 = tc_str(months=months, use_names=True)
    tc2 = tc_str(months=months, days=days)
    
    for tc in (tc1, tc2):

        cmd = f'daops subset --time {ti} --time-components {tc} --output-dir {tmpdir} {CMIP5_DAY}'
        print(cmd)
        
        
        import pdb
        pdb.set_trace()

        ds = xr.open_dataset(result.file_uris[0], use_cftime=True)

        assert set(ds.time.dt.month.values) == set(months)
        assert set(ds.time.dt.day.values) == set(days)
        assert len(ds.time.values) == (ye - ys) * len(months) * len(days)
        ds.close()
