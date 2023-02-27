import os
import pytest
import tempfile
import xarray as xr
from daops.ops.subset import subset
from jinja2 import Template
from tests._common import write_roocs_cfg
from roocs_utils.parameter.param_utils import time_interval


CMIP5_IDS = [
    "cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga",
    "cmip5.output1.MOHC.HadGEM2-ES.rcp85.mon.atmos.Amon.r1i1p1.latest.tas",
    "cmip5.output1.MOHC.HadGEM2-ES.historical.mon.land.Lmon.r1i1p1.latest.rh",
]


def simple_test(out_dir='/tmp/out',
                in_path='/home/roocsdev/.mini-esgf-data/master/test_data/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/land/day/r1i1p1/latest/mrsos/mrsos_day_HadGEM2-ES_rcp45_r1i1p1_20051201-20151130.nc'
                #in_path='/badc/cmip5/data/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/land/day/r1i1p1/latest/mrsos/mrsos_day_HadGEM2-ES_rcp45_r1i1p1_20051201-20151130.nc'
                ):

    os.system(f'rm -f {out_dir}/*')
    #os.system(f'ls -l {os.environ["ROOCS_CONFIG"]}')
    #os.system(f'cat {os.environ["ROOCS_CONFIG"]}')
   
    #params = {'collection': [in_path], 'output_dir': out_dir}    
    params = {'collection': ['cmip5.output1.INM.inmcm4.rcp45.mon.ocean.Omon.r1i1p1.latest.zostoga'],
              'output_dir': out_dir}    
    result = subset(**params)
    print(result.file_uris)

    out_path, = result.file_uris
    assert out_path == os.path.join(out_dir, os.path.basename(in_path))
    assert os.path.exists(out_path)
    os.system(f'ls -l {out_path}')


def simple_test2(tmpdir):

    print('running test 2')
    result = subset(
        CMIP5_IDS[0],
        time=time_interval("2085-01-16", "2120-12-16"),
        output_dir=tmpdir,
        file_namer="simple",
        apply_fixes=False,
    )
    #_check_output_nc(result)
    ds = xr.open_dataset(result.file_uris[0], use_cftime=True)
    assert ds.time.shape == (192,)

    # lev should still be in ds.dims because fix hasn't been applied
    assert "lev" in ds.dims

    
def test_foo(tmpdir, load_esgf_test_data):
    print(f'tmpdir is {tmpdir}')
    simple_test2(tmpdir)
    

def write_cfg():
    cfg_templ = """
    [project:cmip5]
    base_dir = {{ base_dir }}/test_data/badc/cmip5/data/cmip5
    """
    ROOCS_CFG = os.path.join(tempfile.gettempdir(), "roocs.ini")
    #MINI_ESGF_CACHE_DIR = Path.home() / ".mini-esgf-data"
    #MINI_ESGF_MASTER_DIR = os.path.join(MINI_ESGF_CACHE_DIR, "master")
    MINI_ESGF_MASTER_DIR = '/home/roocsdev/.mini-esgf-data/master'
    cfg = Template(cfg_templ).render(base_dir=MINI_ESGF_MASTER_DIR)
    with open(ROOCS_CFG, "w") as fp:
        fp.write(cfg)

    print(f'conf file {ROOCS_CFG} contains')
    print(cfg)
    print('--------------')
        
    # point to roocs cfg in environment
    os.environ["ROOCS_CONFIG"] = ROOCS_CFG


if __name__ == '__main__':
    write_roocs_cfg()
    #write_cfg()
    simple_test2('/tmp/direct-test/')


