from typing import Dict
from math import ceil
import hypothesis.strategies as hst
import numpy as np
from numpy.testing import assert_array_equal
import pytest
from hypothesis import given, settings
from string import ascii_uppercase

from qcodes.dataset.measurements import Measurement
from qcodes.instrument.parameter import expand_setpoints_helper
from qcodes.dataset.descriptions.detect_shapes import detect_shape_of_measurement


@pytest.mark.parametrize("bg_writing", [True, False])
@pytest.mark.parametrize("setpoints_type", ['text', 'numeric'])
@settings(deadline=None, max_examples=10)
@given(n_points=hst.integers(min_value=1, max_value=11))
def test_cache_1d(experiment, DAC, DMM, n_points, bg_writing,
                  channel_array_instrument, setpoints_type):

    setpoints_param, setpoints_values = _prepare_setpoints_1d(
        DAC, channel_array_instrument,
        n_points, setpoints_type
    )

    meas = Measurement()

    meas.register_parameter(setpoints_param)

    meas_parameters = (DMM.v1,
                       channel_array_instrument.A.dummy_multi_parameter,
                       channel_array_instrument.A.dummy_scalar_multi_parameter,
                       channel_array_instrument.A.dummy_2d_multi_parameter,
                       channel_array_instrument.A.dummy_2d_multi_parameter_2,
                       channel_array_instrument.A.dummy_array_parameter,
                       channel_array_instrument.A.dummy_complex_array_parameter,
                       channel_array_instrument.A.dummy_complex,
                       channel_array_instrument.A.dummy_parameter_with_setpoints,
                       channel_array_instrument.A.dummy_parameter_with_setpoints_complex,
                       )
    channel_array_instrument.A.dummy_start(0)
    channel_array_instrument.A.dummy_stop(10)
    channel_array_instrument.A.dummy_n_points(10)
    for param in meas_parameters:
        meas.register_parameter(param, setpoints=(setpoints_param,))

    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        _assert_parameter_data_is_identical(dataset.get_parameter_data(), dataset.cache.data())
        for i, v in enumerate(setpoints_values):
            setpoints_param.set(v)

            meas_vals = [(param, param.get()) for param in meas_parameters[:-2]]
            meas_vals += expand_setpoints_helper(meas_parameters[-2])
            meas_vals += expand_setpoints_helper(meas_parameters[-1])

            datasaver.add_result((setpoints_param, v),
                                 *meas_vals)
            datasaver.flush_data_to_database(block=True)
            data = dataset.cache.data()
            _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                                data)
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())
    assert dataset.cache._loaded_from_completed_ds is True
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())


@pytest.mark.parametrize("bg_writing", [True, False])
@pytest.mark.parametrize("setpoints_type", ['text', 'numeric'])
@settings(deadline=None, max_examples=10)
@given(n_points=hst.integers(min_value=1, max_value=101))
def test_cache_1d_every_other_point(experiment, DAC, DMM, n_points, bg_writing,
                                    channel_array_instrument, setpoints_type):

    setpoints_param, setpoints_values = _prepare_setpoints_1d(DAC, channel_array_instrument,
                                                                                   n_points, setpoints_type)

    meas = Measurement()

    meas.register_parameter(setpoints_param)

    meas_parameters = (DMM.v1,
                       channel_array_instrument.A.temperature,
                       channel_array_instrument.B.temperature
                       )
    for param in meas_parameters:
        meas.register_parameter(param, setpoints=(setpoints_param,))

    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        _assert_parameter_data_is_identical(dataset.get_parameter_data(), dataset.cache.data())
        for i, v in enumerate(setpoints_values):
            setpoints_param.set(v)

            meas_vals = [(param, param.get()) for param in meas_parameters]

            if i % 2 == 0:
                datasaver.add_result((setpoints_param, v),
                                     *meas_vals)
            else:
                datasaver.add_result((setpoints_param, v),
                                     *meas_vals[0:2])
            datasaver.flush_data_to_database(block=True)
            data = dataset.cache.data()
            assert len(data['dummy_channel_inst_ChanA_temperature']['dummy_channel_inst_ChanA_temperature']) == i + 1
            assert len(data['dummy_channel_inst_ChanB_temperature']['dummy_channel_inst_ChanB_temperature']) == i//2 + 1
            _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                                data)
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())
    assert dataset.cache._loaded_from_completed_ds is True
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())


def _prepare_setpoints_1d(DAC, channel_array_instrument, n_points, setpoints_type):
    if setpoints_type == 'numeric':
        setpoints_param = DAC.ch1
        setpoints_values = np.linspace(-1, 1, n_points)
    else:
        setpoints_param = channel_array_instrument.A.dummy_text
        setpoints_values = [l*(i+1) for i, l in
                            enumerate(ascii_uppercase*(n_points//26+1))][0:n_points]
    return setpoints_param, setpoints_values


@pytest.mark.parametrize("bg_writing", [True, False])
@settings(deadline=None, max_examples=10)
@given(n_points_outer=hst.integers(min_value=1, max_value=11),
       n_points_inner=hst.integers(min_value=1, max_value=11))
def test_cache_2d(experiment, DAC, DMM, n_points_outer,
                      n_points_inner, bg_writing, channel_array_instrument):
    meas = Measurement()

    meas.register_parameter(DAC.ch1)
    meas.register_parameter(DAC.ch2)

    meas_parameters = (DMM.v1,
                       channel_array_instrument.A.dummy_multi_parameter,
                       channel_array_instrument.A.dummy_scalar_multi_parameter,
                       channel_array_instrument.A.dummy_2d_multi_parameter,
                       channel_array_instrument.A.dummy_2d_multi_parameter_2,
                       channel_array_instrument.A.dummy_array_parameter,
                       channel_array_instrument.A.dummy_complex_array_parameter,
                       channel_array_instrument.A.dummy_complex,
                       channel_array_instrument.A.dummy_parameter_with_setpoints,
                       channel_array_instrument.A.dummy_parameter_with_setpoints_complex,
                       )
    channel_array_instrument.A.dummy_start(0)
    channel_array_instrument.A.dummy_stop(10)
    channel_array_instrument.A.dummy_n_points(10)
    for param in meas_parameters:
        meas.register_parameter(param, setpoints=(DAC.ch1, DAC.ch2))
    n_rows_written = 0
    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        _assert_parameter_data_is_identical(dataset.get_parameter_data(), dataset.cache.data())
        for v1 in np.linspace(-1, 1, n_points_outer):
            for v2 in np.linspace(-1, 1, n_points_inner):
                DAC.ch1.set(v1)
                DAC.ch2.set(v2)
                meas_vals = [(param, param.get()) for param in meas_parameters[:-2]]
                meas_vals += expand_setpoints_helper(meas_parameters[-2])
                meas_vals += expand_setpoints_helper(meas_parameters[-1])

                datasaver.add_result((DAC.ch1, v1),
                                     (DAC.ch2, v2),
                                     *meas_vals)
                datasaver.flush_data_to_database(block=True)
                n_rows_written += 1
                data = dataset.cache.data()
                _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                                    data)
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())


@pytest.mark.parametrize("bg_writing", [True, False])
@pytest.mark.parametrize("storage_type", ['numeric', 'array', None])
@settings(deadline=None, max_examples=10)
@given(n_points_outer=hst.integers(min_value=1, max_value=11),
       n_points_inner=hst.integers(min_value=1, max_value=11))
def test_cache_2d_num_with_multiple_storage_types(experiment, DAC, DMM, n_points_outer,
                      n_points_inner, bg_writing, storage_type):
    meas = Measurement()

    meas.register_parameter(DAC.ch1, paramtype=storage_type)
    meas.register_parameter(DAC.ch2, paramtype=storage_type)
    meas.register_parameter(DMM.v1, setpoints=(DAC.ch1, DAC.ch2), paramtype=storage_type)
    array_used = _array_param_used_in_tree(meas)
    n_rows_written = 0
    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        _assert_parameter_data_is_identical(dataset.get_parameter_data(), dataset.cache.data())
        for v1 in np.linspace(-1, 1, n_points_outer):
            for v2 in np.linspace(-1, 1, n_points_inner):
                DAC.ch1.set(v1)
                DAC.ch2.set(v2)
                datasaver.add_result((DAC.ch1, v1),
                                     (DAC.ch2, v2),
                                     (DMM.v1, DMM.v1.get()))
                datasaver.flush_data_to_database(block=True)
                n_rows_written += 1
                data = dataset.cache.data()
                if array_used:
                    shape = (n_rows_written, 1)
                else:
                    shape = (n_rows_written,)
                assert data[DMM.v1.full_name][DMM.v1.full_name].shape == shape
                assert data[DMM.v1.full_name][DAC.ch1.full_name].shape == shape
                _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                                    data)
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())


@pytest.mark.parametrize("bg_writing", [True, False])
@pytest.mark.parametrize("storage_type", ['numeric', 'array', None])
@settings(deadline=None, max_examples=10)
@given(n_points=hst.integers(min_value=1, max_value=21))
def test_cache_1d_array_in_1d(experiment, DAC, channel_array_instrument, n_points, bg_writing, storage_type):
    param = channel_array_instrument.A.dummy_array_parameter
    meas = Measurement()
    meas.register_parameter(DAC.ch1, paramtype=storage_type)
    meas.register_parameter(param, setpoints=(DAC.ch1,), paramtype=storage_type)
    array_used = _array_param_used_in_tree(meas)

    setpoint_name = "_".join((param.instrument.full_name, param.setpoint_names[0]))

    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        for i, v1 in enumerate(np.linspace(-1, 1, n_points)):
            datasaver.add_result((DAC.ch1, v1),
                                 (param, param.get()))
            datasaver.flush_data_to_database(block=True)
            data = dataset.cache.data()
            n_rows_written = i+1
            if array_used:
                shape = (n_rows_written, param.shape[0])
            else:
                shape = (n_rows_written * param.shape[0],)
            if storage_type != 'array':
                # with explicit array types the shape is incorrect
                # https://github.com/QCoDeS/Qcodes/issues/2105
                assert data[param.full_name][DAC.ch1.full_name].shape == shape
            assert data[param.full_name][setpoint_name].shape == shape
            assert data[param.full_name][param.full_name].shape == shape
            _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                                data)
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())


@pytest.mark.parametrize("bg_writing", [True, False])
@pytest.mark.parametrize("storage_type", ['numeric', 'array', None])
@settings(deadline=None, max_examples=10)
@given(n_points=hst.integers(min_value=1, max_value=21))
def test_cache_multiparam_in_1d(experiment, DAC, channel_array_instrument, n_points, bg_writing, storage_type):
    param = channel_array_instrument.A.dummy_2d_multi_parameter
    meas = Measurement()
    meas.register_parameter(DAC.ch1, paramtype=storage_type)
    meas.register_parameter(param, setpoints=(DAC.ch1,), paramtype=storage_type)
    array_used = _array_param_used_in_tree(meas)

    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        for i, v1 in enumerate(np.linspace(-1, 1, n_points)):
            datasaver.add_result((DAC.ch1, v1),
                                 (param, param.get()))
            datasaver.flush_data_to_database(block=True)
            data = dataset.cache.data()
            n_rows_written = i+1
            for j, subparam in enumerate(param.full_names):
                if array_used:
                    expected_shape = (n_rows_written,) + param.shapes[j]
                else:
                    expected_shape = n_rows_written * np.prod(param.shapes[j])
                assert data[subparam][subparam].shape == expected_shape
                if storage_type != 'array':
                    # with explicit array types the shape is incorrect
                    # https://github.com/QCoDeS/Qcodes/issues/2105
                    assert data[subparam][DAC.ch1.full_name].shape == expected_shape
                for setpoint_name in param.setpoint_full_names[j]:
                    assert data[subparam][setpoint_name].shape == expected_shape
            _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                                data)
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())


@pytest.mark.parametrize("bg_writing", [True, False])
@pytest.mark.parametrize("storage_type", ['array', None])
@pytest.mark.parametrize("outer_param_type", ['numeric', 'text'])
@settings(deadline=None, max_examples=10)
@given(n_points=hst.integers(min_value=1, max_value=21))
def test_cache_complex_array_param_in_1d(experiment, DAC, channel_array_instrument, n_points, bg_writing, storage_type, outer_param_type):
    param = channel_array_instrument.A.dummy_complex_array_parameter
    meas = Measurement()
    if outer_param_type == 'numeric':
        outer_param = DAC.ch1
        outer_setpoints = np.linspace(-1, 1, n_points)
        outer_storage_type = storage_type
    else:
        outer_param = channel_array_instrument.A.dummy_text
        outer_setpoints = ['A', 'B', 'C', 'D']
        outer_storage_type = 'text'
    meas.register_parameter(outer_param, paramtype=outer_storage_type)
    meas.register_parameter(param, setpoints=(outer_param,), paramtype=storage_type)
    array_used = _array_param_used_in_tree(meas)
    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        for i, v1 in enumerate(outer_setpoints):
            datasaver.add_result((outer_param, v1),
                                 (param, param.get()))
            datasaver.flush_data_to_database(block=True)
            data = dataset.cache.data()
            n_rows_written = i+1

            if array_used:
                expected_shape = (n_rows_written,) + param.shape
            else:
                expected_shape = n_rows_written * np.prod(param.shape)
            assert data[param.full_name][param.full_name].shape == expected_shape
            if storage_type != 'array':
                # with explicit array types the shape is incorrect
                # https://github.com/QCoDeS/Qcodes/issues/2105
                assert data[param.full_name][outer_param.full_name].shape == expected_shape
            for setpoint_name in param.setpoint_full_names:
                assert data[param.full_name][setpoint_name].shape == expected_shape
            _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                                data)
    _assert_parameter_data_is_identical(dataset.get_parameter_data(),
                                        dataset.cache.data())


@pytest.mark.parametrize("bg_writing", [True, False])
@pytest.mark.parametrize("setpoints_type", ['text', 'numeric'])
@settings(deadline=None, max_examples=10)
@given(n_points=hst.integers(min_value=1, max_value=11))
def test_cache_1d_shape(experiment, DAC, DMM, n_points, bg_writing,
                  channel_array_instrument, setpoints_type):

    setpoints_param, setpoints_values = _prepare_setpoints_1d(
        DAC, channel_array_instrument,
        n_points, setpoints_type
    )

    meas = Measurement()

    meas.register_parameter(setpoints_param)

    meas_parameters = (DMM.v1,
                       channel_array_instrument.A.dummy_multi_parameter,
                       channel_array_instrument.A.dummy_scalar_multi_parameter,
                       channel_array_instrument.A.dummy_2d_multi_parameter,
                       channel_array_instrument.A.dummy_2d_multi_parameter_2,
                       channel_array_instrument.A.dummy_array_parameter,
                       channel_array_instrument.A.dummy_complex_array_parameter,
                       channel_array_instrument.A.dummy_complex,
                       channel_array_instrument.A.dummy_parameter_with_setpoints,
                       channel_array_instrument.A.dummy_parameter_with_setpoints_complex,
                       )
    pws_n_points = 10
    channel_array_instrument.A.dummy_start(0)
    channel_array_instrument.A.dummy_stop(10)
    channel_array_instrument.A.dummy_n_points(pws_n_points)

    expected_shapes = {
        'dummy_dmm_v1': (n_points, ),
        'dummy_channel_inst_ChanA_multi_setpoint_param_this': (n_points, 5),
        'dummy_channel_inst_ChanA_multi_setpoint_param_that': (n_points, 5),
        'dummy_channel_inst_ChanA_thisparam': (n_points, ),
        'dummy_channel_inst_ChanA_thatparam': (n_points, ),
        'dummy_channel_inst_ChanA_this': (n_points, 5, 3),
        'dummy_channel_inst_ChanA_that': (n_points, 5, 3),
        'dummy_channel_inst_ChanA_this_5_3': (n_points, 5, 3),
        'dummy_channel_inst_ChanA_this_2_7': (n_points, 2, 7),
        'dummy_channel_inst_ChanA_dummy_array_parameter': (n_points, 5),
        'dummy_channel_inst_ChanA_dummy_complex_array_parameter': (n_points, 5),
        'dummy_channel_inst_ChanA_dummy_complex': (n_points, ),
        'dummy_channel_inst_ChanA_dummy_parameter_with_setpoints': (n_points, pws_n_points),
        'dummy_channel_inst_ChanA_dummy_parameter_with_setpoints_complex': (n_points, pws_n_points)
    }

    for param in meas_parameters:
        meas.register_parameter(param, setpoints=(setpoints_param,))
    meas.set_shapes(detect_shape_of_measurement(
        meas_parameters,
        (n_points,))
    )
    n_points_measured = 0
    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        _assert_parameter_data_is_identical(dataset.get_parameter_data(), dataset.cache.data())
        for i, v in enumerate(setpoints_values):
            n_points_measured += 1
            setpoints_param.set(v)

            meas_vals = [(param, param.get()) for param in meas_parameters[:-2]]
            meas_vals += expand_setpoints_helper(meas_parameters[-2])
            meas_vals += expand_setpoints_helper(meas_parameters[-1])

            datasaver.add_result((setpoints_param, v),
                                 *meas_vals)
            datasaver.flush_data_to_database(block=True)
            cache_data_trees = dataset.cache.data()
            param_data_trees = dataset.get_parameter_data()
            _assert_partial_cache_is_as_expected(
                cache_data_trees,
                expected_shapes,
                n_points_measured,
                param_data_trees,
                cache_correct=True
            )
    cache_data_trees = dataset.cache.data()
    param_data_trees = dataset.get_parameter_data()

    _assert_completed_cache_is_as_expected(cache_data_trees,
                                           param_data_trees,
                                           flatten=False)


@pytest.mark.parametrize("bg_writing", [True, False])
@pytest.mark.parametrize("cache_size", ["too_large",
                                        "correct",
                                        "too_small"])
@settings(deadline=None, max_examples=10)
@given(n_points_outer=hst.integers(min_value=1, max_value=11),
       n_points_inner=hst.integers(min_value=1, max_value=11),
       pws_n_points=hst.integers(min_value=1, max_value=11))
def test_cache_2d_shape(experiment,
                        DAC,
                        DMM,
                        n_points_outer,
                        n_points_inner,
                        pws_n_points,
                        bg_writing,
                        channel_array_instrument,
                        cache_size):
    meas = Measurement()

    meas.register_parameter(DAC.ch1)
    meas.register_parameter(DAC.ch2)

    meas_parameters = (DMM.v1,
                       channel_array_instrument.A.dummy_multi_parameter,
                       channel_array_instrument.A.dummy_scalar_multi_parameter,
                       channel_array_instrument.A.dummy_2d_multi_parameter,
                       channel_array_instrument.A.dummy_2d_multi_parameter_2,
                       channel_array_instrument.A.dummy_array_parameter,
                       channel_array_instrument.A.dummy_complex_array_parameter,
                       channel_array_instrument.A.dummy_complex,
                       channel_array_instrument.A.dummy_parameter_with_setpoints,
                       channel_array_instrument.A.dummy_parameter_with_setpoints_complex,
                       )

    channel_array_instrument.A.dummy_start(0)
    channel_array_instrument.A.dummy_stop(10)
    channel_array_instrument.A.dummy_n_points(pws_n_points)
    for param in meas_parameters:
        meas.register_parameter(param, setpoints=(DAC.ch1, DAC.ch2))

    if cache_size == "too_small":
        meas.set_shapes(detect_shape_of_measurement(
            meas_parameters,
            (int(ceil(n_points_outer/2)), n_points_inner))
        )
    elif cache_size == "too_large":
        meas.set_shapes(detect_shape_of_measurement(
            meas_parameters,
            (n_points_outer*2, n_points_inner))
        )
    else:
        meas.set_shapes(detect_shape_of_measurement(
            meas_parameters,
            (n_points_outer, n_points_inner))
        )

    expected_shapes = {
        'dummy_dmm_v1': (n_points_outer, n_points_inner),
        'dummy_channel_inst_ChanA_multi_setpoint_param_this': (n_points_outer, n_points_inner, 5),
        'dummy_channel_inst_ChanA_multi_setpoint_param_that': (n_points_outer, n_points_inner, 5),
        'dummy_channel_inst_ChanA_thisparam': (n_points_outer, n_points_inner),
        'dummy_channel_inst_ChanA_thatparam': (n_points_outer, n_points_inner),
        'dummy_channel_inst_ChanA_this': (n_points_outer, n_points_inner, 5, 3),
        'dummy_channel_inst_ChanA_that': (n_points_outer, n_points_inner, 5, 3),
        'dummy_channel_inst_ChanA_this_5_3': (n_points_outer, n_points_inner, 5, 3),
        'dummy_channel_inst_ChanA_this_2_7': (n_points_outer, n_points_inner, 2, 7),
        'dummy_channel_inst_ChanA_dummy_array_parameter': (n_points_outer, n_points_inner, 5),
        'dummy_channel_inst_ChanA_dummy_complex_array_parameter': (n_points_outer, n_points_inner, 5),
        'dummy_channel_inst_ChanA_dummy_complex': (n_points_outer, n_points_inner),
        'dummy_channel_inst_ChanA_dummy_parameter_with_setpoints': (n_points_outer, n_points_inner, pws_n_points),
        'dummy_channel_inst_ChanA_dummy_parameter_with_setpoints_complex': (n_points_outer, n_points_inner, pws_n_points)
    }

    if cache_size == "correct":
        assert meas._shapes == expected_shapes

    with meas.run(write_in_background=bg_writing) as datasaver:
        dataset = datasaver.dataset
        # Check that parameter data and cache data are indential for empty datasets
        _assert_parameter_data_is_identical(dataset.get_parameter_data(), dataset.cache.data())
        n_points_measured = 0
        for v1 in np.linspace(-1, 1, n_points_outer):
            for v2 in np.linspace(-1, 1, n_points_inner):
                n_points_measured += 1
                DAC.ch1.set(v1)
                DAC.ch2.set(v2)
                meas_vals = [(param, param.get()) for param in meas_parameters]

                datasaver.add_result((DAC.ch1, v1),
                                     (DAC.ch2, v2),
                                     *meas_vals)
                datasaver.flush_data_to_database(block=True)
                param_data_trees = dataset.get_parameter_data()
                cache_data_trees = dataset.cache.data()

                _assert_partial_cache_is_as_expected(
                    cache_data_trees,
                    expected_shapes,
                    n_points_measured,
                    param_data_trees,
                    cache_size == "correct"
                )
    cache_data_trees = dataset.cache.data()
    param_data_trees = dataset.get_parameter_data()
    _assert_completed_cache_is_as_expected(cache_data_trees,
                                           param_data_trees,
                                           flatten=cache_size == "too_small",
                                           clip=cache_size == "too_large")


def _assert_completed_cache_is_as_expected(
        cache_data_trees,
        param_data_trees,
        flatten=False,
        clip=False):
    for outer_key, cache_data_tree in cache_data_trees.items():
        for inner_key, cache_data in cache_data_tree.items():
            if flatten:
                assert_array_equal(
                    cache_data.flatten(),
                    param_data_trees[outer_key][inner_key].flatten()
                )
            elif clip:
                size = param_data_trees[outer_key][inner_key].size
                assert_array_equal(
                    cache_data.ravel()[:size],
                    param_data_trees[outer_key][inner_key].ravel()
                )
            else:
                assert_array_equal(
                    cache_data,
                    param_data_trees[outer_key][inner_key]
                )


def _assert_partial_cache_is_as_expected(
        cache_data_trees,
        expected_shapes,
        n_points_measured,
        param_data_trees,
        cache_correct=True
):
    assert sorted(cache_data_trees.keys()) == sorted(expected_shapes.keys())
    for outer_key, cache_data_tree in cache_data_trees.items():
        exshape = expected_shapes[outer_key]
        if len(exshape) > 2:
            array_shape = np.prod(exshape[2:])
        else:
            array_shape = 1

        for inner_key, cache_data in cache_data_tree.items():
            if cache_correct:
                assert cache_data.shape == exshape
            assert_array_equal(
                cache_data.ravel()[:n_points_measured * array_shape],
                param_data_trees[outer_key][inner_key].ravel()[:n_points_measured * array_shape]
            )


def _assert_parameter_data_is_identical(expected: Dict[str, Dict[str, np.ndarray]],
                                        actual: Dict[str, Dict[str, np.ndarray]]):
    assert expected.keys() == actual.keys()

    for outer_key in expected.keys():
        expected_inner = expected[outer_key]
        actual_inner = actual[outer_key]
        assert expected_inner.keys() == actual_inner.keys()
        for inner_key in expected_inner.keys():
            np.testing.assert_array_equal(expected_inner[inner_key],
                                          actual_inner[inner_key])


def _array_param_used_in_tree(measurement: Measurement) -> bool:
    found_array = False
    for paramspecbase in measurement.parameters.values():
        if paramspecbase.type == 'array':
            found_array = True
    return found_array
