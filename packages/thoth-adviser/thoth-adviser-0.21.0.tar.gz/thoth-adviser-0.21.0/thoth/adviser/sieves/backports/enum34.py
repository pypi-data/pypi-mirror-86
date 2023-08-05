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

"""A sieve to remove backport of enum34 intended for older Python versions."""

import logging
from typing import Any
from typing import Dict
from typing import Generator
from typing import Optional
from typing import TYPE_CHECKING

import attr
from thoth.common import get_justification_link as jl
from thoth.python import PackageVersion

from ...exceptions import SkipPackage
from ...sieve import Sieve

if TYPE_CHECKING:
    from ...pipeline_builder import PipelineBuilderContext

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class Enum34BackportSieve(Sieve):
    """Remove backport of enum34, available in the standard library starting Python 3.4.

    https://pypi.org/project/enum34/
    https://docs.python.org/3/library/enum.html
    """

    CONFIGURATION_DEFAULT = {"package_name": "enum34"}
    _MESSAGE = (
        f"Dependency 'enum34' removed: emum34 is available in Python "
        f"standard library starting Python 3.4 - see {jl('backports')}"
    )

    _logged = attr.ib(default=False, type=bool, init=False)

    def pre_run(self) -> None:
        """Initialize self before running."""
        self._logged = False
        super().pre_run()

    @classmethod
    def should_include(cls, builder_context: "PipelineBuilderContext") -> Optional[Dict[str, Any]]:
        """Include for Python 3.5 and above for adviser and dependency monkey runs."""
        if builder_context.is_included(cls) or builder_context.project.runtime_environment.python_version is None:
            return None

        if builder_context.project.runtime_environment.get_python_version_tuple() >= (3, 4):
            return {}

        return None

    def run(self, package_versions: Generator[PackageVersion, None, None]) -> Generator[PackageVersion, None, None]:
        """Remove dependency enum34 for newer Python versions."""
        if not self._logged:
            self.context.stack_info.append({"type": "WARNING", "message": self._MESSAGE})
            _LOGGER.warning(self._MESSAGE)
            self._logged = True

        raise SkipPackage
