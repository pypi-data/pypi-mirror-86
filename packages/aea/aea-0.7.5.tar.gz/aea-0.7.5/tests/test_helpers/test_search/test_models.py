# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
"""This module contains the tests for the helpers.search.models."""
from typing import Tuple
from unittest.mock import Mock

import pytest

from aea.exceptions import AEAEnforceError
from aea.helpers.search.models import (
    And,
    Attribute,
    AttributeInconsistencyException,
    Constraint,
    ConstraintType,
    ConstraintTypes,
    DataModel,
    Description,
    Location,
    Not,
    Or,
    Query,
    generate_data_model,
)


def test_location():
    """Test Location type."""
    loc = Location(1.1, 2.2)
    assert loc.distance(Location(1.1, 2.2)) == 0

    assert Location(1.1, 2.2) == Location(1.1, 2.2)

    assert Location(1.1, 2.2) is not None
    assert isinstance(loc.tuple, Tuple)
    assert loc.tuple == (loc.latitude, loc.longitude)
    assert str(loc) == "Location(latitude=1.1,longitude=2.2)"


def test_attribute():
    """Test data model Attribute."""
    params = dict(name="test", type_=str, is_required=True)

    assert Attribute(**params) == Attribute(**params)
    assert Attribute(**params) is not None
    assert Attribute(**params) != Attribute(name="another", type_=int, is_required=True)
    assert (
        str(Attribute(**params))
        == "Attribute(name=test,type=<class 'str'>,is_required=True)"
    )


def test_data_model():
    """Test data model definitions."""
    params = dict(name="test", type_=str, is_required=True)

    data_model = DataModel("test", [Attribute(**params)])
    data_model._check_validity()

    assert (
        str(data_model)
        == "DataModel(name=test,attributes={'test': \"Attribute(name=test,type=<class 'str'>,is_required=True)\"},description=)"
    )
    with pytest.raises(ValueError):
        data_model = DataModel("test", [Attribute(**params), Attribute(**params)])
        data_model._check_validity()

    assert DataModel("test", [Attribute(**params)]) == DataModel(
        "test", [Attribute(**params)]
    )
    assert DataModel("test", [Attribute(**params)]) != DataModel(
        "not test", [Attribute(**params)]
    )


def test_generate_data_model():
    """Test model generated from description."""
    params = dict(name="test", type_=str, is_required=True)

    data_model = DataModel("test", [Attribute(**params)])

    assert generate_data_model("test", {"test": "str"}) == data_model


def test_description():
    """Test model description."""
    values = {"test": "test"}
    Description(values=values, data_model=generate_data_model("test", values))
    desc = Description(values=values)
    assert (
        str(desc)
        == "Description(values={'test': 'test'},data_model=DataModel(name=,attributes={'test': \"Attribute(name=test,type=<class 'str'>,is_required=True)\"},description=))"
    )

    assert Description(values=values) == Description(values=values)
    assert list(Description(values=values)) == list(values.values())

    with pytest.raises(
        AttributeInconsistencyException, match=r"Missing required attribute."
    ):
        Description(
            values=values, data_model=generate_data_model("test", {"extra_key": "key"})
        )

    with pytest.raises(
        AttributeInconsistencyException,
        match=r"Have extra attribute not in data model.",
    ):
        Description(values=values, data_model=generate_data_model("test", {}))

    with pytest.raises(
        AttributeInconsistencyException, match=r".* has incorrect type:.*"
    ):
        Description(values=values, data_model=generate_data_model("test", {"test": 12}))

    with pytest.raises(
        AttributeInconsistencyException, match=r".* has unallowed type:.*"
    ):
        Description(
            values={"test": object()},
            data_model=generate_data_model("test", {"test": object()}),
        )

    desc = Description(values=values)
    mock = Mock()
    Description.encode(mock, desc)
    assert Description.decode(mock) == desc


def test_constraint_type():
    """Test ConstraintType."""
    for cons_type in [
        ConstraintTypes.EQUAL,
        ConstraintTypes.NOT_EQUAL,
        ConstraintTypes.LESS_THAN,
        ConstraintTypes.LESS_THAN_EQ,
        ConstraintTypes.GREATER_THAN,
        ConstraintTypes.GREATER_THAN_EQ,
    ]:
        constrant_type = ConstraintType(cons_type, 12)
        constrant_type.is_valid(Attribute("test", int, True))
        constrant_type.check(13)

    constrant_type = ConstraintType(ConstraintTypes.WITHIN, [1, 2])
    constrant_type.is_valid(Attribute("test", int, True))
    constrant_type.check(13)
    assert str(constrant_type) == "ConstraintType(value=[1, 2],type=within)"

    constrant_type = ConstraintType(ConstraintTypes.IN, [1, 2])
    constrant_type.is_valid(Attribute("test", int, True))
    constrant_type.check(13)

    constrant_type = ConstraintType(ConstraintTypes.NOT_IN, [1, 2])
    constrant_type.is_valid(Attribute("test", int, True))
    constrant_type.check(13)

    constrant_type = ConstraintType(ConstraintTypes.DISTANCE, [Location(1.1, 2.2), 2.2])
    constrant_type.is_valid(Attribute("test", int, True))
    constrant_type.check(Location(1.1, 2.2))

    with pytest.raises(ValueError):
        ConstraintType("something", [Location(1.1, 2.2), 2.2]).is_valid(
            Attribute("test", int, True)
        )

    with pytest.raises(AEAEnforceError):
        ConstraintType(ConstraintTypes.GREATER_THAN, str)

    assert ConstraintType(ConstraintTypes.IN, [1, 2]) == ConstraintType(
        ConstraintTypes.IN, [1, 2]
    )


def test_constraints_expressions():
    """Test constraint expressions: And, Or, Not."""
    expression = And(
        [
            ConstraintType(ConstraintTypes.EQUAL, 12),
            ConstraintType(ConstraintTypes.EQUAL, 12),
        ]
    )
    expression.check_validity()
    assert expression.check(12)
    expression.is_valid(Attribute("test", int, True))

    expression = Or(
        [
            ConstraintType(ConstraintTypes.EQUAL, 12),
            ConstraintType(ConstraintTypes.EQUAL, 13),
        ]
    )
    expression.check_validity()
    assert expression.check(12)

    expression.is_valid(Attribute("test", int, True))

    expression = Not(
        And(
            [
                ConstraintType(ConstraintTypes.EQUAL, 12),
                ConstraintType(ConstraintTypes.EQUAL, 12),
            ]
        )
    )
    expression.check_validity()
    assert expression.check(13)
    expression.is_valid(Attribute("test", int, True))


def test_constraint():
    """Test Constraint."""
    c1 = Constraint("author", ConstraintType("==", "Stephen King"))
    c2 = Constraint("author", ConstraintType("in", ["Stephen King"]))
    book_1 = Description({"author": "Stephen King", "year": 1991, "genre": "horror"})
    book_2 = Description({"author": "George Orwell", "year": 1948, "genre": "horror"})
    assert c1.check(book_1)
    assert not c1.check(book_2)

    # empty description
    assert not c1.check(Description({}))

    # bad type
    assert not c1.check(Description({"author": 12}))

    # bad type
    assert not c2.check(Description({"author": 12}))

    assert c1.is_valid(generate_data_model("test", {"author": "some author"}))

    assert not c1.is_valid(generate_data_model("test", {"not_author": "some author"}))

    assert c1 == c1
    assert c1 != c2


def test_query():
    """Test Query."""
    c1 = Constraint("author", ConstraintType("==", "Stephen King"))
    query = Query([c1])
    assert (
        str(query)
        == "Query(constraints=['Constraint(attribute_name=author,constraint_type=ConstraintType(value=Stephen King,type===))'],model=None)"
    )
    query.check_validity()
    assert query.check(
        Description({"author": "Stephen King", "year": 1991, "genre": "horror"})
    )
    assert query.is_valid(generate_data_model("test", {"author": "some author"}))

    with pytest.raises(ValueError, match=r"Constraints must be a list .*"):
        query = Query(c1)

    Query([]).check_validity()

    with pytest.raises(
        ValueError,
        match=r"Invalid input value for type 'Query': the query is not valid for the given data model.",
    ):
        Query(
            [c1], generate_data_model("test", {"notauthor": "not some author"})
        ).check_validity()

    assert Query([]) == Query([])

    mock = Mock()
    Query.encode(mock, Query([]))
    assert Query.decode(mock) == Query([])
