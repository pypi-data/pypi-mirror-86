#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2020 Fridolin Pokorny
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

"""A wrap that notifies a bug in summary output spotted on TensorFlow 2.3."""

from typing import Any
from typing import Dict
from typing import Optional
from typing import TYPE_CHECKING

from thoth.common import get_justification_link as jl

from ...state import State
from ...wrap import Wrap

if TYPE_CHECKING:
    from ..pipeline_builder import PipelineBuilderContext


class TensorFlow23DictSummary(Wrap):
    """A wrap that notifies a bug in summary output spotted on TensorFlow 2.3.

    https://github.com/tensorflow/tensorflow/issues/42679
    """

    CONFIGURATION_DEFAULT = {"package_name": "tensorflow"}
    _JUSTIFICATION = [
        {
            "type": "WARNING",
            "message": "TensorFlow in version 2.3 can produce misleading output summary",
            "link": jl("tf_42679"),
        }
    ]

    @classmethod
    def should_include(cls, builder_context: "PipelineBuilderContext") -> Optional[Dict[str, Any]]:
        """Include this wrap in adviser."""
        if not builder_context.is_adviser_pipeline():
            return None

        units_included = builder_context.get_included_wraps(cls)
        if len(units_included) == 4:
            return None
        elif len(units_included) == 0:
            return {"package_name": "tensorflow"}
        elif len(units_included) == 1:
            return {"package_name": "tensorflow-cpu"}
        elif len(units_included) == 2:
            return {"package_name": "tensorflow-gpu"}
        elif len(units_included) == 3:
            return {"package_name": "intel-tensorflow"}

        return None

    def run(self, state: State) -> None:
        """Notify about a bug in summary output spotted on TensorFlow 2.3."""
        tensorflow_any = (
            state.resolved_dependencies.get("tensorflow")
            or state.resolved_dependencies.get("tensorflow-cpu")
            or state.resolved_dependencies.get("tensorflow-gpu")
            or state.resolved_dependencies.get("intel-tensorflow")
        )

        if tensorflow_any is None:
            return None

        if tensorflow_any[1] == "2.3" or tensorflow_any[1].startswith("2.3."):
            state.add_justification(self._JUSTIFICATION)
