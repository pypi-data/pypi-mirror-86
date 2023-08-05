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

"""Implementation of sieves used in adviser pipeline."""

from .abi_compat import AbiCompatibilitySieve
from .backports import Enum34BackportSieve
from .backports import Functools32BackportSieve
from .backports import ImportlibMetadataBackportSieve
from .backports import ImportlibResourcesBackportSieve
from .backports import MockBackportSieve
from .filter_index import FilterIndexSieve
from .index_enabled import PackageIndexSieve
from .locked import CutLockedSieve
from .pandas import PandasPy36Sieve
from .prereleases import CutPreReleasesSieve
from .setuptools import Py36SetuptoolsSieve
from .solved import SolvedSieve
from .tensorflow import TensorFlowAPISieve
from .tensorflow import TensorFlowCUDASieve
from .tensorflow import TensorFlowPython39Sieve
from .version_constraint import VersionConstraintSieve


# Relative ordering of units is relevant, as the order specifies order
# in which the asked to be registered - any dependencies between them
# can be mentioned here.
__all__ = [
    "CutPreReleasesSieve",
    "CutLockedSieve",
    "PackageIndexSieve",
    "SolvedSieve",
    "VersionConstraintSieve",
    "AbiCompatibilitySieve",
    "FilterIndexSieve",
    "Enum34BackportSieve",
    "Functools32BackportSieve",
    "ImportlibMetadataBackportSieve",
    "ImportlibResourcesBackportSieve",
    "MockBackportSieve",
    "Py36SetuptoolsSieve",
    "TensorFlowAPISieve",
    "TensorFlowCUDASieve",
    "TensorFlowPython39Sieve",
    "PandasPy36Sieve",
]
