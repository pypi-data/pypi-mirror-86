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

"""A sieve for filtering packages based on constraints.

This sieve will filter out packages in specific versions *if* they occur
in the resolved stack.
"""

import logging
from typing import Any
from typing import Dict
from typing import Optional
from typing import Generator
from typing import TYPE_CHECKING

from packaging.specifiers import Specifier
from voluptuous import Required
from voluptuous import Schema

import attr
from thoth.python import PackageVersion

from ..sieve import Sieve

if TYPE_CHECKING:
    from ..pipeline_builder import PipelineBuilderContext

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class VersionConstraintSieve(Sieve):
    """Filter out packages based on version constraints if they occur in the stack."""

    CONFIGURATION_DEFAULT = {"package_name": None, "version_specifier": None}
    CONFIGURATION_SCHEMA = Schema({Required("package_name"): str, Required("version_specifier"): str})

    _specifier = attr.ib(type=Optional[Specifier], default=None, init=False)

    @classmethod
    def should_include(cls, builder_context: "PipelineBuilderContext") -> Optional[Dict[str, Any]]:
        """Include this sieve only if user explicitly asks for it."""
        return None

    def pre_run(self) -> None:
        """Parse and initialize specifier used."""
        self._specifier = Specifier(self.configuration["version_specifier"])
        super().pre_run()

    def run(self, package_versions: Generator[PackageVersion, None, None]) -> Generator[PackageVersion, None, None]:
        """Filter out packages based on build time/installation issues.."""
        if self._specifier is None:
            return

        for package_version in package_versions:
            if package_version.name == self.configuration["package_name"] and not self._specifier.contains(
                package_version.locked_version
            ):
                _LOGGER.debug(
                    "Removing package %r based on configured version specifier %r",
                    self.configuration["package_name"],
                    self.configuration["version_specifier"],
                )
                continue

            yield package_version
