#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2019, 2020 Kevin Postlehtwait
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

"""Filter out stacks which have require non-existent ABI symbols."""

import logging
from typing import Any, Dict, Optional, Generator, Set, TYPE_CHECKING, Tuple

import attr
from thoth.common import get_justification_link as jl
from thoth.python import PackageVersion

from ..sieve import Sieve

if TYPE_CHECKING:
    from ..pipeline_builder import PipelineBuilderContext

_LOGGER = logging.getLogger(__name__)


@attr.s(slots=True)
class AbiCompatibilitySieve(Sieve):
    """Remove packages if the image being used doesn't have necessary ABI."""

    CONFIGURATION_DEFAULT = {"package_name": None}
    image_symbols = attr.ib(type=Set[str], factory=set, init=False)
    _messages_logged = attr.ib(type=Set[Tuple[str, str, str]], factory=set, init=False)

    _LINK = jl("abi_missing")

    @classmethod
    def should_include(cls, builder_context: "PipelineBuilderContext") -> Optional[Dict[str, Any]]:
        """Include sieve which checks for abi compatability."""
        if not builder_context.is_included(cls) and builder_context.project.runtime_environment.is_fully_specified():
            return {}

        return None

    def pre_run(self) -> None:
        """Initialize image_symbols."""
        runtime_environment = self.context.project.runtime_environment
        self.image_symbols = set(
            self.context.graph.get_analyzed_image_symbols_all(
                os_name=runtime_environment.operating_system.name,
                os_version=runtime_environment.operating_system.version,
                cuda_version=runtime_environment.cuda_version,
                python_version=runtime_environment.python_version,
            )
        )
        self._messages_logged.clear()
        _LOGGER.debug("Analyzed image has the following symbols: %r", self.image_symbols)
        super().pre_run()

    def run(self, package_versions: Generator[PackageVersion, None, None]) -> Generator[PackageVersion, None, None]:
        """If package requires non-present symbols remove it."""
        for pkg_vers in package_versions:
            package_symbols = set(
                self.context.graph.get_python_package_required_symbols(
                    package_name=pkg_vers.name,
                    package_version=pkg_vers.locked_version,
                    index_url=pkg_vers.index.url,
                )
            )

            # Shortcut if package requires no symbols
            if not package_symbols:
                yield pkg_vers
                continue

            missing_symbols = package_symbols - self.image_symbols
            if not missing_symbols:
                yield pkg_vers
            else:
                # Log removed package
                package_tuple = pkg_vers.to_tuple()
                if package_tuple not in self._messages_logged:
                    message = f"Package {package_tuple} was removed due to missing ABI symbols in the environment"
                    _LOGGER.warning("%s - see %s", message, self._LINK)
                    self._messages_logged.add(package_tuple)
                    _LOGGER.debug("The following symbols are not present: %r", str(missing_symbols))

                continue
