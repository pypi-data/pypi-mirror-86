import pytest
import os.path
import easyvvuq as uq
from easyvvuq.constants import default_campaign_prefix, Status
from easyvvuq.db.sql import CampaignDB
from easyvvuq.data_structs import CampaignInfo, RunInfo, AppInfo
from easyvvuq.constants import Status
import pandas as pd
import numpy as np


@pytest.fixture
def app_info():
    app_info = AppInfo('test', uq.ParamsSpecification({
        "temp_init": {
            "type": "float",
            "min": 0.0,
            "max": 100.0,
            "default": 95.0},
        "kappa": {
            "type": "float",
            "min": 0.0,
            "max": 0.1,
            "default": 0.025},
        "t_env": {
            "type": "float",
            "min": 0.0,
            "max": 40.0,
            "default": 15.0},
        "out_file": {
            "type": "string",
            "default": "output.csv"}}),
        None,
        uq.encoders.GenericEncoder(
            template_fname='tests/cooling/cooling.template',
            delimiter='$',
            target_filename='cooling_in.json'),
        uq.decoders.SimpleCSV(
            target_filename='output.csv',
            output_columns=["te"]))

    return app_info


@pytest.fixture
def campaign(tmp_path, app_info):
    info = CampaignInfo(
        name='test',
        campaign_dir_prefix=default_campaign_prefix,
        easyvvuq_version=uq.__version__,
        campaign_dir=str(tmp_path))
    campaign = CampaignDB(location='sqlite:///{}/test.sqlite'.format(tmp_path),
                          new_campaign=True, name='test', info=info)
    campaign.tmp_path = str(tmp_path)
    runs = [RunInfo('run', 'test', '.', 1, {'a': 1}, 1, 1) for _ in range(1010)]
    run_names = ['Run_{}'.format(i) for i in range(1, 1011)]
    campaign.add_runs(runs)
    campaign.add_app(app_info)
    return campaign


def test_db_file_created(campaign):
    assert(os.path.isfile('{}/test.sqlite'.format(campaign.tmp_path)))


def test_get_and_set_status(campaign):
    run_names = ['Run_{}'.format(i) for i in range(1, 1011)]
    assert(all([campaign.get_run_status(name) == Status.NEW for name in run_names]))
    campaign.set_run_statuses(run_names, Status.ENCODED)
    assert(all([campaign.get_run_status(name) == Status.ENCODED for name in run_names]))


def test_get_num_runs(campaign):
    assert(campaign.get_num_runs() == 1010)


def test_app(campaign):
    with pytest.raises(RuntimeError):
        campaign.app('test_')
    app_dict = campaign.app('test')
    assert(app_dict['name'] == 'test')
    assert(isinstance(app_dict, dict))


def test_add_app(campaign, app_info):
    with pytest.raises(RuntimeError):
        campaign.add_app(app_info)


def test_campaign(campaign):
    assert('test' in campaign.campaigns())


def test_get_campaign_id(campaign):
    with pytest.raises(RuntimeError):
        campaign.get_campaign_id('test_')
    assert(campaign.get_campaign_id('test') == 1)


def test_campaign_dir(campaign):
    assert(campaign.campaign_dir('test') == campaign.tmp_path)


def test_version_check(campaign):
    info = CampaignInfo(
        name='test2',
        campaign_dir_prefix=default_campaign_prefix,
        easyvvuq_version="some.other.version",
        campaign_dir=str(campaign.tmp_path))
    with pytest.raises(RuntimeError):
        campaign2 = CampaignDB(location='sqlite:///{}/test.sqlite'.format(campaign.tmp_path),
                               new_campaign=True, name='test2', info=info)
    info = CampaignInfo(
        name='test3',
        campaign_dir_prefix=default_campaign_prefix,
        easyvvuq_version=uq.__version__,
        campaign_dir=str(campaign.tmp_path))
    campaign3 = CampaignDB(location='sqlite:///{}/test.sqlite'.format(campaign.tmp_path),
                           new_campaign=True, name='test3', info=info)


def test_collation(campaign):
    results = [(run[0], {'b': i, 'c': [i + 1, i + 2]}) for i, run in enumerate(campaign.runs())]
    campaign.store_results('test', results)
    campaign.set_run_statuses([run[0] for run in campaign.runs()], Status.COLLATED)
    result = campaign.get_results('test')
    assert(isinstance(result, pd.DataFrame))
    assert(list(result.columns) == [('run_id', 0), ('a', 0), ('b', 0), ('c', 0), ('c', 1)])
    assert(list(result.iloc[100].values) == [101, 1, 100, 101, 102])
    assert(result.count()[0] == 1010)
