#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2019, 2020 Fridolin Pokorny
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

"""Boot units implemented in adviser."""

from .fully_specified_environment import FullySpecifiedEnvironment
from .platform import PlatformBoot
from .pipfile_hash import PipfileHashBoot
from .python_version import PythonVersionBoot
from .rhel_version import RHELVersionBoot
from .solved_software_environment import SolvedSoftwareEnvironmentBoot
from .ubi import UbiBoot

# from ._debug import MemTraceBoot


# Relative ordering of units is relevant, as the order specifies order
# in which the asked to be registered - any dependencies between them
# can be mentioned here.
__all__ = [
    # "MemTraceBoot",
    "PipfileHashBoot",  # Should be placed before any changes to the input.
    "UbiBoot",
    "PythonVersionBoot",
    "SolvedSoftwareEnvironmentBoot",
    "RHELVersionBoot",
    "PlatformBoot",
    "FullySpecifiedEnvironment",
    "SolvedSoftwareEnvironmentBoot",
]
