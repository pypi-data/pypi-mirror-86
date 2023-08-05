.. _steps:

Step pipeline unit type
-----------------------

Another type of unit used in Thoth's adviser is called "step". You can see step
as a step performed by resolver to obtain fully pinned down software stack - a
package in a specific version is added to the resolver's internal state (see
:ref:`introduction` for theoretical background). Each step adds one package to
the resolver's state - if there are no more packages to add, a so called final
state then represents a fully pinned down software stack (as can be seen in
``Pipfile.lock``).

.. warning::

  The logic behind resolver manipulates with states. Step pipeline unit
  implementation **must NOT** adjust state attributes except for the stack
  information. Adjusting beam is also not allowed. If a step implementation
  adjusts state or beam, the behaviour is undefined.

The pipeline step is triggered after :ref:`boot <boots>`, :ref:`pseudonym
<pseudonyms>` and :ref:`sieve <sieves>` pipeline unit types and is used to
score and decide whether the given package can be added the the resolver's
internal state. In contrast to sieves, a step has a full notion of
package-versions present in not fully resolved software stack (resolver's
internal state) so steps can judge whether the given package should be added to
the state based on packages already present (see Real world examples section
bellow for examples).

.. note::

  Step pipeline units can be called even though a package that is about to be
  added to a state is already present in the state. This can happen if there
  are multiple packages that introduce such dependency. An example can be a
  pipeline step run when adding ``tensorflow`` to a state based on requirement
  ``keras``, but ``tensorflow`` is already present in the state as it was
  introduced by Seldon dependency (another example can be package ``six`` that
  can be introduced by many Python packages in the software stack).

  Note this behaviour is turned off by default. If the pipeline step requires
  such call, the step implementation should set
  ``step_instance.configuration["multi_package_resolution"]`` to ``True`` in
  derived classes implementing step logic. This is usually accomplished using
  the default configuration (if the unit should not behave differently based on
  the ``should_include`` logic). The default option can be set using
  ``Step.CONFIGURATION_DEFAULT["multi_package_resolution"] = True``

Main usage
==========

* Decide whether the given package should be added to the resolver state

  * Raising exception :class:`NotAcceptable
    <thoth.adviser.exceptions.NotAcceptable>` will prevent from adding
    package-version to the state in resolver

* Score positively or negatively presence of a package in the software stack

  * Each pipeline step can return a tuple formed out of ``float`` and a list of
    dictionaries

      * ``float`` represents score adjustment of the state

      * the list of dictionaries carries "justification" on why the given
        package-version was scored the way it was scored - this justification
        is shown to the user

* Prematurely end resolution based on the step reached

  * Raising exception :class:`EagerStopPipeline
    <thoth.adviser.exceptions.EagerStopPipeline>` will cause stopping the whole
    resolver run and causing resolver to return products computed so far

* Removing a library from a stack even though it is stated as a dependency
  (directly or transitively) by raising :class:`SkipPackage
  <thoth.adviser.exceptions.SkipPackage>` based on the resolution process.

Real world examples
===================

* Some releases of ``tensorflow`` do not work with some ``numpy`` versions -
  a ``numpy`` in a specific version can be added to a software stack that has
  ``tensorflow``  incompatible with the given ``numpy`` release (even though
  the version range specification allows it, ``tensorflow`` maintainers did
  not tested the given ``numpy`` release with issued ``tensorflow`` release)

    * A step implementing this observation can simply raise ``NotAcceptable``
      exception that will prevent from such issues in the resolved software
      stack as these two will never be resolved together

* Packages that have security vulnerabilities (CVE) can be penalized during
  the resolution so that they do not occur in the resolved software stack,
  unless there is no better candidate based on scoring in other pipeline
  steps

* Prevent adding ``scipy`` to a TensorFlow>2.1<=2.3 unless introduced
  explicitly in the stack. It is not needed (it was introduced accidentally).

Triggering unit for a specific package
======================================

To help with scaling the recommendation engine when it comes to number of
pipeline units possibly registered, it is a good practice to state to which
package the given unit corresponds. To run the pipeline unit for a specific
package, this fact should be reflected in the pipeline unit configuration by
stating ``package_name`` configuration option. An example can be a pipeline
unit specific for TensorFlow packages, which should state ``package_name:
"tensorflow"`` in the pipeline configuration.

If the pipeline unit is generic for any package, the ``package_name``
configuration has to default to ``None``.

Justifications in the recommended software stacks
=================================================

Follow the :ref:`linked documentation for providing valuable information to
users on actions performed in pipeline units implemented <justifications>`.

An example implementation
=========================

.. code-block:: python

  from typing import Any
  from typing import Dict
  from typing import List
  from typing import Optional
  from typing import Tuple

  from thoth.adviser.exceptions import NotAcceptable
  from thoth.adviser import State
  from thoth.adviser import Step
  from thoth.python import PackageVersion


  class StepExample(Step):
      """Filter out numpy causing issues in upstream TensorFlow==1.9.0."""

      # This pipeline unit is specific for "numpy".
      CONFIGURATION_DEFAULT: Dict[str, Any] = {"package_name": "numpy", "multi_package_resolution": False}

      def run(self, state: State, package_version: PackageVersion) -> Optional[Tuple[Optional[float], Optional[List[Dict[str, str]]]]]:
          """The main entry-point for step implementation demonstration."""
          if state.resolved_dependencies.get("tensorflow") != ("tensorflow", "1.9.0", "https://pypi.org/simple"):
              # Accept any other state change.
              return None

          package_version_tuple = package_version.to_tuple()
          if package_version_tuple == ("numpy", "1.17.0", "https://pypi.org/simple"):
              raise NotAcceptable(
                  f"Package {package_version_tuple!r} has known issues with upstream tensorflow in version 1.9.0 due to API incompatibility"
              )

The implementation can also provide other methods, such as :func:`Unit.pre_run
<thoth.adviser.unit.Unit.post_run>`, :func:`Unit.post_run
<thoth.adviser.unit.Unit.post_run>` or :func:`Unit.post_run_report
<thoth.adviser.unit.Unit.post_run>` and pipeline unit configuration adjustment.
See :ref:`unit documentation <unit>` for more info.
