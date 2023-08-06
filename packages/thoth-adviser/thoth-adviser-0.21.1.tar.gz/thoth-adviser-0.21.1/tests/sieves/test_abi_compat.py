#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2020 Kevin Postlethwait
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

"""Test filtering out Python Packages based on required and available ABI symbols."""

import flexmock

from thoth.adviser.context import Context
from thoth.adviser.enums import RecommendationType
from thoth.adviser.pipeline_builder import PipelineBuilderContext
from thoth.adviser.sieves import AbiCompatibilitySieve
from thoth.python import PackageVersion
from thoth.python import Source
from thoth.storages import GraphDatabase

from ..base import AdviserUnitTestCase

_SYSTEM_SYMBOLS = ["GLIBC_2.0", "GLIBC_2.1", "GLIBC_2.2", "GLIBC_2.3", "GLIBC_2.4", "GLIBC_2.5", "GCC_3.4", "X_2.21"]
_REQUIRED_SYMBOLS_A = ["GLIBC_2.9"]
_REQUIRED_SYMBOLS_B = ["GLIBC_2.4"]


class TestAbiCompatSieve(AdviserUnitTestCase):
    """Test filtering out packages based on symbols required."""

    UNIT_TESTED = AbiCompatibilitySieve

    def test_verify_multiple_should_include(self, builder_context: PipelineBuilderContext) -> None:
        """Verify multiple should_include calls do not loop endlessly."""
        builder_context.recommendation_type = RecommendationType.LATEST
        builder_context.project.runtime_environment.should_receive("is_fully_specified").with_args().and_return(True)
        self.verify_multiple_should_include(builder_context)

    def test_abi_compat_symbols_present(self) -> None:
        """Test if required symbols are correctly identified."""
        source = Source("https://pypi.org/simple")
        package_version = PackageVersion(name="tensorflow", version="==1.9.0", index=source, develop=False)
        flexmock(GraphDatabase)
        GraphDatabase.should_receive("get_analyzed_image_symbols_all").and_return(_SYSTEM_SYMBOLS).once()
        GraphDatabase.should_receive("get_python_package_required_symbols").and_return(_REQUIRED_SYMBOLS_B).once()

        context = flexmock(
            graph=GraphDatabase(),
            project=flexmock(
                runtime_environment=flexmock(
                    operating_system=flexmock(name="rhel", version="8.0"),
                    cuda_version="4.6",
                    python_version="3.6",
                )
            ),
        )
        with AbiCompatibilitySieve.assigned_context(context):
            sieve = AbiCompatibilitySieve()
            sieve.pre_run()
            assert list(sieve.run((p for p in [package_version]))) == [package_version]

    def test_abi_compat_symbols_not_present(self) -> None:
        """Test if required symbols being missing is correctly identified."""
        source = Source("https://pypi.org/simple")
        package_version = PackageVersion(name="tensorflow", version="==1.9.0", index=source, develop=False)
        flexmock(GraphDatabase)
        GraphDatabase.should_receive("get_analyzed_image_symbols_all").and_return(_SYSTEM_SYMBOLS).once()
        GraphDatabase.should_receive("get_python_package_required_symbols").and_return(_REQUIRED_SYMBOLS_A).once()

        context = flexmock(
            graph=GraphDatabase,
            project=flexmock(
                runtime_environment=flexmock(
                    operating_system=flexmock(name="rhel", version="8.0"),
                    cuda_version="4.6",
                    python_version="3.6",
                )
            ),
        )
        with AbiCompatibilitySieve.assigned_context(context):
            sieve = AbiCompatibilitySieve()
            sieve.pre_run()
            assert list(sieve.run((p for p in [package_version]))) == []

    def test_super_pre_run(self, context: Context) -> None:
        """Make sure the pre-run method of the base is called."""
        context.graph.should_receive("get_analyzed_image_symbols_all").with_args(
            os_name=context.project.runtime_environment.operating_system.name,
            os_version=context.project.runtime_environment.operating_system.version,
            cuda_version=context.project.runtime_environment.cuda_version,
            python_version=context.project.runtime_environment.python_version,
        ).and_return(set()).once()
        unit = self.UNIT_TESTED()
        assert unit.unit_run is False
        with unit.assigned_context(context):
            unit.pre_run()
        assert unit.unit_run is False
