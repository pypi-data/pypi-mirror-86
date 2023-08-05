#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2019 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Test implementation of random walk in the dependency graph."""

from typing import Callable

import flexmock
from hypothesis import given
from hypothesis.strategies import integers

import random

from thoth.adviser.beam import Beam
from thoth.adviser.predictors import RandomWalk
from thoth.adviser.state import State

from ..base import AdviserTestCase


class TestRandomWalk(AdviserTestCase):
    """Tests related to random walk in the dependency graph."""

    @given(
        integers(min_value=1, max_value=256),
    )
    def test_run(self, state_factory: Callable[[], State], state_count: int) -> None:
        """Test running the random walk method."""
        state = state_factory()
        beam = Beam()
        for _ in range(state_count):
            cloned_state = state.clone()
            cloned_state.score = random.random()
            cloned_state.iteration = state.iteration + 1
            beam.add_state(cloned_state)

        predictor = RandomWalk()
        context = flexmock(accepted_final_states_count=33, beam=beam)

        with predictor.assigned_context(context):
            next_state, package_tuple = predictor.run()
            assert next_state in beam.iter_states()
            assert package_tuple is not None
            assert package_tuple[0] in next_state.unresolved_dependencies
            assert package_tuple in next_state.unresolved_dependencies[package_tuple[0]].values()

    def test_pre_run(self) -> None:
        """Test pre-run initialization."""
        context = flexmock(limit=99)

        predictor = RandomWalk()
        assert predictor._history == []
        predictor._history = [(0.99, 33), (0.42, 42)]

        with predictor.assigned_context(context):
            predictor.pre_run()
            assert predictor._history == [], "Predictor's history not discarded"
