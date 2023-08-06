# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/master/LICENSE

from __future__ import absolute_import

import sys

import pytest
import numpy

import awkward1

def test_concatenate_number():
    assert awkward1.to_list(awkward1.concatenate([
        awkward1.Array([[1, 2, 3], [], [4, 5]]), 999], axis=1)) == [
            [1, 2, 3, 999], [999], [4, 5, 999]]
    assert awkward1.to_list(awkward1.concatenate([
        awkward1.Array([[[1.1], [2.2, 3.3]], [[]], [[4.4], [5.5]]]), 999], axis=2)) == [
            [[1.1, 999.0], [2.2, 3.3, 999.0]], [[999.0]], [[4.4, 999.0], [5.5, 999.0]]]
    assert str(awkward1.type(awkward1.concatenate([
        awkward1.Array([[1, 2, 3], [], [4, 5]]),
        awkward1.Array([[123], [223], [323]])], axis=1))) == "3 * var * int64"
    assert awkward1.to_list(awkward1.concatenate([
        awkward1.Array([[1, 2, 3], [], [4, 5]]),
        awkward1.Array([[123], [223], [323]])], axis=1)) == [
                [1, 2, 3, 123], [223], [4, 5, 323]]

    one = awkward1.Array([[1, 2, 3], [], [4, 5]])
    two = awkward1.Array([123, 223, 323])
    assert awkward1.to_list(awkward1.concatenate([one, two], axis=1)) == [
            [1, 2, 3, 123], [223], [4, 5, 323]]

def test_list_offset_array_concatenate():
    content_one = awkward1.layout.NumpyArray(numpy.array([0.0, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]))
    content_two = awkward1.layout.NumpyArray(numpy.array([999.999, 0.11, 0.22, 0.33, 0.44, 0.55, 0.66, 0.77, 0.88, 0.99]))
    offsets_one = awkward1.layout.Index64(numpy.array([0, 3, 3, 5, 6, 10], dtype=numpy.int64))
    offsets_two = awkward1.layout.Index64(numpy.array([1, 3, 4, 4, 6, 9, 9, 10], dtype=numpy.int64))
    offsets_three = awkward1.layout.Index64(numpy.array([0, 3, 3, 5], dtype=numpy.int64))
    offsets_four = awkward1.layout.Index64(numpy.array([1, 3, 4, 4, 6, 7, 7], dtype=numpy.int64))

    one = awkward1.layout.ListOffsetArray64(offsets_one, content_one)
    padded_one = one.rpad(7, 0)
    assert awkward1.to_list(padded_one) == [[0.0, 1.1, 2.2], [], [3.3, 4.4], [5.5], [6.6, 7.7, 8.8, 9.9], None, None]

    two = awkward1.layout.ListOffsetArray64(offsets_two, content_two)
    three = awkward1.layout.ListOffsetArray64(offsets_three, one)
    four = awkward1.layout.ListOffsetArray64(offsets_four, two)

    assert awkward1.to_list(awkward1.concatenate([one, two], 0)) == [
        [0.0, 1.1, 2.2], [], [3.3, 4.4], [5.5], [6.6, 7.7, 8.8, 9.9],
        [0.11, 0.22], [0.33], [], [0.44, 0.55], [0.66, 0.77, 0.88], [], [0.99]]

    assert awkward1.to_list(awkward1.concatenate([padded_one, two], 1)) == [
        [0.0, 1.1, 2.2, 0.11, 0.22],
        [0.33],
        [3.3, 4.4],
        [5.5, 0.44, 0.55],
        [6.6, 7.7, 8.8, 9.9, 0.66, 0.77, 0.88],
        [],
        [0.99]]

    with pytest.raises(ValueError) as err:
        assert awkward1.to_list(awkward1.concatenate([one, two], 2))

    assert awkward1.to_list(awkward1.concatenate([three, four], 0)) == [
        [[0.0, 1.1, 2.2], [], [3.3, 4.4]],
         [],
        [[5.5], [6.6, 7.7, 8.8, 9.9]],
        [[0.33], []],
        [[0.44, 0.55]],
         [],
        [[0.66, 0.77, 0.88], []],
        [[0.99]],
         []]

    padded = three.rpad(6, 0)
    assert awkward1.to_list(awkward1.concatenate([padded, four], 1)) == [
        [[0.0, 1.1, 2.2], [], [3.3, 4.4], [0.33], []],
        [[0.44, 0.55]],
        [[5.5], [6.6, 7.7, 8.8, 9.9]],
        [[0.66, 0.77, 0.88], []],
        [[0.99]],
        []]

    assert awkward1.to_list(awkward1.concatenate([four, four], 2)) == [
        [[0.33, 0.33], []],
        [[0.44, 0.55, 0.44, 0.55]],
         [],
        [[0.66, 0.77, 0.88, 0.66, 0.77, 0.88], []],
        [[0.99, 0.99]],
         []]

def test_list_array_concatenate():
    one = awkward1.Array([[1, 2, 3], [], [4, 5]]).layout
    two = awkward1.Array([[1.1, 2.2], [3.3, 4.4], [5.5]]).layout

    one = awkward1.layout.ListArray64(one.starts, one.stops, one.content)
    two = awkward1.layout.ListArray64(two.starts, two.stops, two.content)
    assert awkward1.to_list(awkward1.concatenate([one, two], 0)) == [[1, 2, 3], [], [4, 5], [1.1, 2.2], [3.3, 4.4], [5.5]]
    assert awkward1.to_list(awkward1.concatenate([one, two], 1)) == [[1, 2, 3, 1.1, 2.2], [3.3, 4.4], [4, 5, 5.5]]

def test_records_concatenate():
    one = awkward1.Array([{"x": 1, "y": [1]}, {"x": 2, "y": [1, 2]}, {"x": 3, "y": [1, 2, 3]}]).layout
    two = awkward1.Array([{"y": [], "x": 4}, {"y": [3, 2, 1], "x": 5}]).layout

    assert awkward1.to_list(awkward1.concatenate([one, two], 0)) == [{"x": 1, "y": [1]}, {"x": 2, "y": [1, 2]}, {"x": 3, "y": [1, 2, 3]},
                                                   {"y": [], "x": 4}, {"y": [3, 2, 1], "x": 5}]
    with pytest.raises(ValueError) as err:
        awkward1.to_list(awkward1.concatenate([one, two], 1))

    with pytest.raises(ValueError) as err:
        awkward1.to_list(awkward1.concatenate([one, two], 2))

def test_indexed_array_concatenate():
    one = awkward1.Array([[1, 2, 3], [None, 4], None, [None, 5]]).layout
    two = awkward1.Array([6, 7, 8]).layout
    three = awkward1.Array([[6.6], [7.7, 8.8]]).layout
    four = awkward1.Array([[6.6], [7.7, 8.8], None, [9.9]]).layout

    assert awkward1.to_list(awkward1.concatenate([one, two], 0)) == [[1, 2, 3], [None, 4], None, [None, 5], 6, 7, 8]

    with pytest.raises(ValueError) as err:
        awkward1.to_list(awkward1.concatenate([one, three], 1))

    assert awkward1.to_list(awkward1.concatenate([one, four], 1)) == [[1, 2, 3, 6.6], [None, 4, 7.7, 8.8], [], [None, 5, 9.9]]

def test_bytemasked_concatenate():
    one = awkward1.Array([1, 2, 3, 4, 5, 6]).mask[[True, True, False, True, False, True]].layout
    two = awkward1.Array([7, 99, 999, 8, 9]).mask[[True, False, False, True, True]].layout

    assert awkward1.to_list(awkward1.concatenate([one, two], 0)) == [1, 2, None, 4, None, 6, 7, None, None, 8, 9]

    with pytest.raises(ValueError) as err:
        awkward1.to_list(awkward1.concatenate([one, two], 1))

def test_listoffsetarray_concatenate():
    content_one = awkward1.layout.NumpyArray(numpy.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))
    offsets_one = awkward1.layout.Index64(numpy.array([0, 3, 3, 5, 9]))
    one = awkward1.layout.ListOffsetArray64(offsets_one, content_one)

    assert awkward1.to_list(one) == [[1, 2, 3], [], [4, 5], [6, 7, 8, 9]]

    content_two = awkward1.layout.NumpyArray(numpy.array([100, 200, 300, 400, 500]))
    offsets_two = awkward1.layout.Index64(numpy.array([0, 2, 4, 4, 5]))
    two = awkward1.layout.ListOffsetArray64(offsets_two, content_two)

    assert awkward1.to_list(two) == [[100, 200], [300, 400], [], [500]]
    assert awkward1.to_list(awkward1.concatenate([one, two], 0)) == [[1, 2, 3], [], [4, 5], [6, 7, 8, 9], [100, 200], [300, 400], [], [500]]
    assert awkward1.to_list(awkward1.concatenate([one, two], 1)) == [[1, 2, 3, 100, 200], [300, 400], [4, 5], [6, 7, 8, 9, 500]]

def test_numpyarray_concatenate_axis0():
    emptyarray = awkward1.layout.EmptyArray()

    np1 = numpy.arange(2*7*5, dtype=numpy.float64).reshape(2, 7, 5)
    np2 = numpy.arange(3*7*5, dtype=numpy.int64).reshape(3, 7, 5)
    ak1 = awkward1.layout.NumpyArray(np1)
    ak2 = awkward1.layout.NumpyArray(np2)

    assert awkward1.to_list(awkward1.concatenate([np1, np2, np1, np2], 0)) == awkward1.to_list(numpy.concatenate([np1, np2, np1, np2], 0))
    assert awkward1.to_list(awkward1.concatenate([ak1, ak2], 0)) == awkward1.to_list(numpy.concatenate([ak1, ak2], 0))
    assert awkward1.to_list(numpy.concatenate([ak1, ak2], 0)) == awkward1.to_list(awkward1.concatenate([np1, np2], 0))

def test_numpyarray_concatenate():

    np1 = numpy.arange(2*7*5, dtype=numpy.float64).reshape(2, 7, 5)
    np2 = numpy.arange(2*7*5, dtype=numpy.int64).reshape(2, 7, 5)
    ak1 = awkward1.layout.NumpyArray(np1)
    ak2 = awkward1.layout.NumpyArray(np2)

    assert awkward1.to_list(numpy.concatenate([np1, np2], 1)) == awkward1.to_list(awkward1.concatenate([ak1, ak2], 1))
    assert awkward1.to_list(numpy.concatenate([np2, np1], 1)) == awkward1.to_list(awkward1.concatenate([ak2, ak1], 1))
    assert awkward1.to_list(numpy.concatenate([np1, np2], 2)) == awkward1.to_list(awkward1.concatenate([ak1, ak2], 2))
    assert awkward1.to_list(numpy.concatenate([np2, np1], 2)) == awkward1.to_list(awkward1.concatenate([ak2, ak1], 2))
    assert awkward1.to_list(numpy.concatenate([np2, np1], -1)) == awkward1.to_list(awkward1.concatenate([ak2, ak1], -1))

def test_numbers_and_records_concatenate():
    awkward1.deprecations_as_errors = True

    numbers = [
            awkward1.Array([
                [1.1, 2.2, 3.3],
                [],
                [4.4, 5.5],
                [6.6, 7.7, 8.8, 9.9],
            ]),
            awkward1.Array([
                [10, 20],
                [30],
                [],
                [40, 50, 60],
            ]),
            awkward1.Array(numpy.array([
                [101, 102, 103],
                [201, 202, 203],
                [301, 302, 303],
                [401, 402, 403],
            ])),
        ]

    records = [
        awkward1.Array([
            [{"x": 0.0, "y": []}, {"x": 1.1, "y": [1]}],
            [],
            [{"x": 2.2, "y": [1, 2]}],
            [{"x": 3.3, "y": [1, 2, 3]}, {"x": 4.4, "y": [1, 2, 3, 4]}],
        ]),
        awkward1.Array([
            [{"x": 0.0, "y": []}],
            [{"x": 1.1, "y": [1]}, {"x": 2.2, "y": [1, 2]}],
            [],
            [{"x": 3.3, "y": [1, 2, 3]}],
        ]),
    ]

    assert awkward1.to_list(awkward1.concatenate([numbers[0], records[0]], 1)) == [
        [1.1, 2.2, 3.3, {"x": 0.0, "y": []}, {"x": 1.1, "y": [1]}],
        [],
        [4.4, 5.5, {"x": 2.2, "y": [1, 2]}],
        [6.6, 7.7, 8.8, 9.9, {"x": 3.3, "y": [1, 2, 3]}, {"x": 4.4, "y": [1, 2, 3, 4]}],
    ]

    assert awkward1.to_list(awkward1.concatenate([numbers[0], numbers[1]], axis=1)) == [
        [1.1, 2.2, 3.3, 10, 20],
        [30],
        [4.4, 5.5],
        [6.6, 7.7, 8.8, 9.9, 40, 50, 60],
    ]

    assert awkward1.to_list(awkward1.concatenate(numbers, axis=1)) == [
        [1.1, 2.2, 3.3, 10, 20, 101, 102, 103],
        [30, 201, 202, 203],
        [4.4, 5.5, 301, 302, 303],
        [6.6, 7.7, 8.8, 9.9, 40, 50, 60, 401, 402, 403]]

    assert awkward1.to_list(awkward1.concatenate(records, axis=1)) == [
        [{'x': 0.0, 'y': []}, {'x': 1.1, 'y': [1]}, {'x': 0.0, 'y': []}],
        [{'x': 1.1, 'y': [1]}, {'x': 2.2, 'y': [1, 2]}],
        [{'x': 2.2, 'y': [1, 2]}],
        [{'x': 3.3, 'y': [1, 2, 3]},
         {'x': 4.4, 'y': [1, 2, 3, 4]},
         {'x': 3.3, 'y': [1, 2, 3]}]]

    with pytest.raises(ValueError) as err:
        awkward1.to_list(awkward1.concatenate([numbers, records], axis=1))
    assert str(err.value).startswith("scalar Record can only be sliced by field name (string); try \"0\"")

def test_broadcast_and_apply_levels():
    arrays = [
    awkward1.Array([[[0.0, 1.1, 2.2], []], [[3.3, 4.4]], [[5.5], [6.6, 7.7, 8.8, 9.9]]]),
    awkward1.Array([[[10, 20], [30]], [[40]], [[50, 60, 70], [80, 90]]]),
    ]
    # nothing is required to have the same length
    assert awkward1.concatenate(arrays, axis=0).tolist() == [
        [[0.0, 1.1, 2.2], []],
        [[3.3, 4.4]],
        [[5.5], [6.6, 7.7, 8.8, 9.9]],
        [[10, 20], [30]],
        [[40]],
        [[50, 60, 70], [80, 90]],
    ]
    # the outermost arrays are required to have the same length, but nothing deeper than that
    assert awkward1.concatenate(arrays, axis=1).tolist() == [
        [[0.0, 1.1, 2.2], [], [10, 20], [30]],
        [[3.3, 4.4], [40]],
        [[5.5], [6.6, 7.7, 8.8, 9.9], [50, 60, 70], [80, 90]],
    ]
    # the outermost arrays and the first level are required to have the same length, but nothing deeper
    assert awkward1.concatenate(arrays, axis=2).tolist() == [
        [[0.0, 1.1, 2.2, 10, 20], [30]],
        [[3.3, 4.4, 40]],
        [[5.5, 50, 60, 70], [6.6, 7.7, 8.8, 9.9, 80, 90]],
    ]

def test_negative_axis_concatenate():
    arrays = [
    awkward1.Array([[[0.0, 1.1, 2.2], []], [[3.3, 4.4]], [[5.5], [6.6, 7.7, 8.8, 9.9]]]),
    awkward1.Array([[[10, 20], [30]], [[40]], [[50, 60, 70], [80, 90]]]),
    ]

    assert awkward1.concatenate(arrays, axis=-1).tolist() == [
        [[0.0, 1.1, 2.2, 10, 20], [30]],
        [[3.3, 4.4, 40]],
        [[5.5, 50, 60, 70], [6.6, 7.7, 8.8, 9.9, 80, 90]],
    ]

    assert awkward1.concatenate(arrays, axis=-2).tolist() == [
        [[0.0, 1.1, 2.2], [], [10, 20], [30]],
        [[3.3, 4.4], [40]],
        [[5.5], [6.6, 7.7, 8.8, 9.9], [50, 60, 70], [80, 90]],
    ]

    assert awkward1.concatenate(arrays, axis=-3).tolist() == [
        [[0.0, 1.1, 2.2], []],
        [[3.3, 4.4]],
        [[5.5], [6.6, 7.7, 8.8, 9.9]],
        [[10, 20], [30]],
        [[40]],
        [[50, 60, 70], [80, 90]],
    ]

def test_even_more():
    dim1 = awkward1.Array([1.1, 2.2, 3.3, 4.4, 5.5])
    dim1a = awkward1.Array([[1.1], [2.2], [3.3], [4.4], [5.5]])
    dim1b = awkward1.Array(numpy.array([[1.1], [2.2], [3.3], [4.4], [5.5]]))
    dim2 = awkward1.Array([[0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9]])
    dim3 = awkward1.Array([[[0, 1, 2], []], [[3, 4]], [], [[5], [6, 7, 8, 9]], []])

    assert awkward1.concatenate([dim1, 999]).tolist() == [1.1, 2.2, 3.3, 4.4, 5.5, 999]
    assert awkward1.concatenate([999, dim1]).tolist() == [999, 1.1, 2.2, 3.3, 4.4, 5.5]

    assert awkward1.concatenate([dim1, dim2]).tolist() == [1.1, 2.2, 3.3, 4.4, 5.5, [0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9]]
    assert awkward1.concatenate([dim2, dim1]).tolist() == [[0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9], 1.1, 2.2, 3.3, 4.4, 5.5]

    with pytest.raises(ValueError):
        awkward1.concatenate([dim1, 999], axis=1)

    assert awkward1.concatenate([dim2, 999], axis=1).tolist() == [[0, 1, 2, 999], [999], [3, 4, 999], [5, 999], [6, 7, 8, 9, 999]]

    assert awkward1.concatenate([999, dim2], axis=1).tolist() == [[999, 0, 1, 2], [999], [999, 3, 4], [999, 5], [999, 6, 7, 8, 9]]

    assert awkward1.concatenate([dim1, dim2], axis=1).tolist() == [[1.1, 0, 1, 2], [2.2], [3.3, 3, 4], [4.4, 5], [5.5, 6, 7, 8, 9]]
    assert awkward1.concatenate([dim2, dim1], axis=1).tolist() == [[0, 1, 2, 1.1], [2.2], [3, 4, 3.3], [5, 4.4], [6, 7, 8, 9, 5.5]]
    assert awkward1.concatenate([dim1a, dim2], axis=1).tolist() == [[1.1, 0, 1, 2], [2.2], [3.3, 3, 4], [4.4, 5], [5.5, 6, 7, 8, 9]]
    assert awkward1.concatenate([dim2, dim1a], axis=1).tolist() == [[0, 1, 2, 1.1], [2.2], [3, 4, 3.3], [5, 4.4], [6, 7, 8, 9, 5.5]]
    assert awkward1.concatenate([dim1b, dim2], axis=1).tolist() == [[1.1, 0, 1, 2], [2.2], [3.3, 3, 4], [4.4, 5], [5.5, 6, 7, 8, 9]]
    assert awkward1.concatenate([dim2, dim1b], axis=1).tolist() == [[0, 1, 2, 1.1], [2.2], [3, 4, 3.3], [5, 4.4], [6, 7, 8, 9, 5.5]]

    assert awkward1.concatenate([123, dim1, dim2]).tolist() == [123, 1.1, 2.2, 3.3, 4.4, 5.5, [0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9]]
    assert awkward1.concatenate([123, dim2, dim1]).tolist() == [123, [0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9], 1.1, 2.2, 3.3, 4.4, 5.5]
    assert awkward1.concatenate([dim1, 123, dim2]).tolist() == [1.1, 2.2, 3.3, 4.4, 5.5, 123, [0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9]]
    assert awkward1.concatenate([dim1, dim2, 123]).tolist() == [1.1, 2.2, 3.3, 4.4, 5.5, [0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9], 123]
    assert awkward1.concatenate([dim2, 123, dim1]).tolist() == [[0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9], 123, 1.1, 2.2, 3.3, 4.4, 5.5]
    assert awkward1.concatenate([dim2, dim1, 123]).tolist() == [[0, 1, 2], [], [3, 4], [5], [6, 7, 8, 9], 1.1, 2.2, 3.3, 4.4, 5.5, 123]

    assert awkward1.concatenate([123, dim1, dim2], axis=1).tolist() == [[123, 1.1, 0, 1, 2], [123, 2.2], [123, 3.3, 3, 4], [123, 4.4, 5], [123, 5.5, 6, 7, 8, 9]]
    assert awkward1.concatenate([123, dim2, dim1], axis=1).tolist() == [[123, 0, 1, 2, 1.1], [123, 2.2], [123, 3, 4, 3.3], [123, 5, 4.4], [123, 6, 7, 8, 9, 5.5]]
    assert awkward1.concatenate([dim1, 123, dim2], axis=1).tolist() == [[1.1, 123, 0, 1, 2], [2.2, 123], [3.3, 123, 3, 4], [4.4, 123, 5], [5.5, 123, 6, 7, 8, 9]]
    assert awkward1.concatenate([dim1, dim2, 123], axis=1).tolist() == [[1.1, 0, 1, 2, 123], [2.2, 123], [3.3, 3, 4, 123], [4.4, 5, 123], [5.5, 6, 7, 8, 9, 123]]
    assert awkward1.concatenate([dim2, 123, dim1], axis=1).tolist() == [[0, 1, 2, 123, 1.1], [123, 2.2], [3, 4, 123, 3.3], [5, 123, 4.4], [6, 7, 8, 9, 123, 5.5]]
    assert awkward1.concatenate([dim2, dim1, 123], axis=1).tolist() == [[0, 1, 2, 1.1, 123], [2.2, 123], [3, 4, 3.3, 123], [5, 4.4, 123], [6, 7, 8, 9, 5.5, 123]]

    assert awkward1.concatenate([123, dim1a, dim2], axis=1).tolist() == [[123, 1.1, 0, 1, 2], [123, 2.2], [123, 3.3, 3, 4], [123, 4.4, 5], [123, 5.5, 6, 7, 8, 9]]
    assert awkward1.concatenate([123, dim2, dim1a], axis=1).tolist() == [[123, 0, 1, 2, 1.1], [123, 2.2], [123, 3, 4, 3.3], [123, 5, 4.4], [123, 6, 7, 8, 9, 5.5]]
    assert awkward1.concatenate([dim1a, 123, dim2], axis=1).tolist() == [[1.1, 123, 0, 1, 2], [2.2, 123], [3.3, 123, 3, 4], [4.4, 123, 5], [5.5, 123, 6, 7, 8, 9]]
    assert awkward1.concatenate([dim1a, dim2, 123], axis=1).tolist() == [[1.1, 0, 1, 2, 123], [2.2, 123], [3.3, 3, 4, 123], [4.4, 5, 123], [5.5, 6, 7, 8, 9, 123]]
    assert awkward1.concatenate([dim2, 123, dim1a], axis=1).tolist() == [[0, 1, 2, 123, 1.1], [123, 2.2], [3, 4, 123, 3.3], [5, 123, 4.4], [6, 7, 8, 9, 123, 5.5]]
    assert awkward1.concatenate([dim2, dim1a, 123], axis=1).tolist() == [[0, 1, 2, 1.1, 123], [2.2, 123], [3, 4, 3.3, 123], [5, 4.4, 123], [6, 7, 8, 9, 5.5, 123]]

    assert awkward1.concatenate([123, dim1b, dim2], axis=1).tolist() == [[123, 1.1, 0, 1, 2], [123, 2.2], [123, 3.3, 3, 4], [123, 4.4, 5], [123, 5.5, 6, 7, 8, 9]]
    assert awkward1.concatenate([123, dim2, dim1b], axis=1).tolist() == [[123, 0, 1, 2, 1.1], [123, 2.2], [123, 3, 4, 3.3], [123, 5, 4.4], [123, 6, 7, 8, 9, 5.5]]
    assert awkward1.concatenate([dim1b, 123, dim2], axis=1).tolist() == [[1.1, 123, 0, 1, 2], [2.2, 123], [3.3, 123, 3, 4], [4.4, 123, 5], [5.5, 123, 6, 7, 8, 9]]
    assert awkward1.concatenate([dim1b, dim2, 123], axis=1).tolist() == [[1.1, 0, 1, 2, 123], [2.2, 123], [3.3, 3, 4, 123], [4.4, 5, 123], [5.5, 6, 7, 8, 9, 123]]
    assert awkward1.concatenate([dim2, 123, dim1b], axis=1).tolist() == [[0, 1, 2, 123, 1.1], [123, 2.2], [3, 4, 123, 3.3], [5, 123, 4.4], [6, 7, 8, 9, 123, 5.5]]
    assert awkward1.concatenate([dim2, dim1b, 123], axis=1).tolist() == [[0, 1, 2, 1.1, 123], [2.2, 123], [3, 4, 3.3, 123], [5, 4.4, 123], [6, 7, 8, 9, 5.5, 123]]

    assert awkward1.concatenate([dim3, 123]).tolist() == [[[0, 1, 2], []], [[3, 4]], [], [[5], [6, 7, 8, 9]], [], 123]
    assert awkward1.concatenate([123, dim3]).tolist() == [123, [[0, 1, 2], []], [[3, 4]], [], [[5], [6, 7, 8, 9]], []]

    assert awkward1.concatenate([dim3, 123], axis=1).tolist() == [[[0, 1, 2], [], 123], [[3, 4], 123], [123], [[5], [6, 7, 8, 9], 123], [123]]
    assert awkward1.concatenate([123, dim3], axis=1).tolist() == [[123, [0, 1, 2], []], [123, [3, 4]], [123], [123, [5], [6, 7, 8, 9]], [123]]

    assert awkward1.concatenate([dim3, dim1], axis=1).tolist() == [[[0, 1, 2], [], 1.1], [[3, 4], 2.2], [3.3], [[5], [6, 7, 8, 9], 4.4], [5.5]]
    assert awkward1.concatenate([dim1, dim3], axis=1).tolist() == [[1.1, [0, 1, 2], []], [2.2, [3, 4]], [3.3], [4.4, [5], [6, 7, 8, 9]], [5.5]]

    assert awkward1.concatenate([dim3, dim2], axis=1).tolist() == [[[0, 1, 2], [], [0, 1, 2]], [[3, 4], []], [[3, 4]], [[5], [6, 7, 8, 9], [5]], [[6, 7, 8, 9]]]
    assert awkward1.concatenate([dim2, dim3], axis=1).tolist() == [[[0, 1, 2], [0, 1, 2], []], [[], [3, 4]], [[3, 4]], [[5], [5], [6, 7, 8, 9]], [[6, 7, 8, 9]]]

    assert awkward1.concatenate([dim3, 123], axis=2).tolist() == [[[0, 1, 2, 123], [123]], [[3, 4, 123]], [], [[5, 123], [6, 7, 8, 9, 123]], []]
    assert awkward1.concatenate([123, dim3], axis=2).tolist() == [[[123, 0, 1, 2], [123]], [[123, 3, 4]], [], [[123, 5], [123, 6, 7, 8, 9]], []]

    assert awkward1.concatenate([dim3, dim3], axis=2).tolist() == [[[0, 1, 2, 0, 1, 2], []], [[3, 4, 3, 4]], [], [[5, 5], [6, 7, 8, 9, 6, 7, 8, 9]], []]

    rec1 = awkward1.Array([{"x": [1, 2], "y": [1.1]}, {"x": [], "y": [2.2, 3.3]}, {"x": [3], "y": []}, {"x": [5, 6, 7], "y": []}, {"x": [8, 9], "y": [4.4, 5.5]}])
    rec2 = awkward1.Array([{"x": [100], "y": [10, 20]}, {"x": [200], "y": []}, {"x": [300, 400], "y": [30]}, {"x": [], "y": [40, 50]}, {"x": [400, 500], "y": [60]}])

    assert awkward1.concatenate([rec1, rec2]).tolist() == [{"x": [1, 2], "y": [1.1]}, {"x": [], "y": [2.2, 3.3]}, {"x": [3], "y": []}, {"x": [5, 6, 7], "y": []}, {"x": [8, 9], "y": [4.4, 5.5]}, {"x": [100], "y": [10, 20]}, {"x": [200], "y": []}, {"x": [300, 400], "y": [30]}, {"x": [], "y": [40, 50]}, {"x": [400, 500], "y": [60]}]

    # maybe someday...
    # assert awkward1.concatenate([rec1, rec2], axis=1) == [{"x": [1, 2, 100], "y": [1.1, 10, 20]}, {"x": [200], "y": [2.2, 3.3]}, {"x": [3, 300, 400], "y": [30]}, {"x": [5, 6, 7], "y": [40, 50]}, {"x": [8, 9, 400, 500], "y": [4.4, 5.5, 60]}]
