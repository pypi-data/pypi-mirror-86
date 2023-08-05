Ndcube v1.4.2 (2020-11-19)
==========================

Bug Fixes
---------

- Fix bug whereby common axis was not updated appropriately when slicing an NDCubeSequence. (`#310 <https://github.com/sunpy/ndcube/pull/310>`__)


Ndcube v1.4.1 (2020-11-03)
==========================

Features
--------

- Add (cube_like)array_axis_physical_types properties to NDCubeSequence and deprecate the world_axis_physical_types properties of NDCube and NDCubeSequence. (`#309 <https://github.com/sunpy/ndcube/pull/309>`__)
- Add new properties to NDCubeSequence, array_axis_physical_types and cube_like_array_axis_physical_types, and deprecate the world_axis_physical_types properties on NDCube and NDCubeSequence. (`#309 <https://github.com/sunpy/ndcube/pull/309>`__)


Ndcube v1.4.0 (2020-11-02)
==========================

Features
--------

- Add new method, `~ndcube.NDCube.axis_world_coord_values`, to return world coords for all pixels for all axes in WCS as quantity objects. (`#283 <https://github.com/sunpy/ndcube/pull/283>`__)


Bug Fixes
---------

- Fix NDCube plotting bug when dependent axes are not first axes. (`#278 <https://github.com/sunpy/ndcube/pull/278>`__)
- Change name of NDCube.axis_world_coord_values to NDCube.axis_world_coords_values to be consistent with NDCube.axis_world_coords (`#293 <https://github.com/sunpy/ndcube/pull/293>`__)
- Move ImageAnimatorWCS class into ndcube from sunpy as it is no longer supported from sunpy 2.1 onwards. (`#306 <https://github.com/sunpy/ndcube/pull/306>`__)
- Fix bug in setting y-axis limits for 1D animations when inf or nan present in data. (`#308 <https://github.com/sunpy/ndcube/pull/308>`__)


Ndcube v1.3.2 (2020-04-20)
==========================

Bug Fixes
---------

- Generalize int type checking so it is independent of the bit-type of the OS. (`#269 <https://github.com/sunpy/ndcube/pull/269>`__)


Ndcube v1.3.1 (2020-04-17)
==========================

Bug Fixes
---------

- Fix NDCollection.aligned_dimensions so it doesnt crash when components of collection are NDCubeSequences. (`#264 <https://github.com/sunpy/ndcube/pull/264>`__)


Trivial/Internal Changes
------------------------

- Simplify and speed up implementation of NDCubeSequence slicing. (`#251 <https://github.com/sunpy/ndcube/pull/251>`__)


Ndcube v1.3.0 (2020-03-27)
==========================

Features
--------

- Add new NDCollection class for linking and manipulating partially or non-aligned NDCubes or NDCubeSequences. (`#238 <https://github.com/sunpy/ndcube/pull/238>`__)


Bug Fixes
---------

- Fixed the files included and excluded from the tarball. (`#212 <https://github.com/sunpy/ndcube/pull/212>`__)
- Fix crashing bug when an NDCube axis after the first is sliced with a numpy.int64. (`#223 <https://github.com/sunpy/ndcube/pull/223>`__)
- Raises error if NDCube is sliced with an Ellipsis. (`#224 <https://github.com/sunpy/ndcube/pull/224>`__)
- Changes behavior of NDCubeSequence slicing. Previously, a slice item of interval
  length 1 would cause an NDCube object to be returned. Now an NDCubeSequence made
  up of 1 NDCube is returned. This is consistent with how interval length 1 slice
  items slice arrays. (`#241 <https://github.com/sunpy/ndcube/pull/241>`__)


Ndcube v1.2.0 (2019-09-10)
==========================

Features
--------

- Changed all instances of "missing_axis" to "missing_axes" (`#157 <https://github.com/sunpy/ndcube/pull/157>`__)
- Added a feature to get the pixel_edges from `ndcube.NDCube.axis_world_coords` (`#174 <https://github.com/sunpy/ndcube/pull/174>`__)


Bug Fixes
---------

- `ndcube.NDCube.world_axis_physical_types` now sets the axis label to the WCS CTYPE if no corresponding IVOA name can be found. (`#164 <https://github.com/sunpy/ndcube/pull/164>`__)
- Fixed the bug of using `pixel_edges` instead of `pixel_values` in plotting (`#176 <https://github.com/sunpy/ndcube/pull/176>`__)
- Fix 2D plotting from crashing when both data and WCS are 2D. (`#182 <https://github.com/sunpy/ndcube/pull/182>`__)
- Fix the ability to pass a custom Axes to `ndcube.NDCube.plot` for a 2D cube. (`#204 <https://github.com/sunpy/ndcube/pull/204>`__)


Trivial/Internal Changes
------------------------

- Include more helpful error when invalid item type is used to slice an `~ndcube.NDCube`. (`#158 <https://github.com/sunpy/ndcube/pull/158>`__)


1.1
===

API-Breaking Changes
--------------------
- `~ndcube.NDCubeBase.crop_by_extra_coord` API has been broken and
  replaced.
  Old version:
  ``crop_by_extra_coord(min_coord_value, interval_width, coord_name)``.
  New version:
  ``crop_by_extra_coord(coord_name, min_coord_value,  max_coord_value)``.
  [#142]

New Features
------------
- Created a new `~ndcube.NDCubeBase` which has all the functionality
  of `~ncube.NDCube` except the plotting.  The old ``NDCubeBase``
  which outlined the ``NDCube`` API was renamed ``NDCubeABC``.
  `~ndcube.NDCube` has all the same functionality as before except is
  now simply inherits from `~ndcube.NDCubeBase` and
  `~ndcube.mixins.plotting.NDCubePlotMixin`. [#101]
- Moved NDCubSequence plotting to a new mixin class,
  NDCubSequencePlotMixin, making the plotting an optional extra.  All
  the non-plotting functionality now lives in the NDCubeSequenceBase
  class. [#98]
- Created a new `~ndcube.NDCubeBase.explode_along_axis` method that
  breaks an NDCube out into an NDCubeSequence along a chosen axis.  It
  is equivalent to
  `~ndcube.NDCubeSequenceBase.explode_along_axis`. [#118]
- NDCubeSequence plot mixin can now animate a cube as a 1-D line if a single
  axis number is supplied to plot_axis_indices kwarg.

API Changes
-----------
- Replaced API of what was previously ``utils.wcs.get_dependent_axes``,
  with two new functions, ``utils.wcs.get_dependent_data_axes`` and
  ``utils.wcs.get_dependent_wcs_axes``. This was inspired by a new
  implementation in ``glue-viz`` which is intended to be merged into
  ``astropy`` in the future.  This API change helped fix the
  ``NDCube.world_axis_physical_type`` bug listed below. [#80]
- Give users more control in plotting both for NDCubePlotMixin and
  NDCubeSequencePlotMixin.  In most cases the axes coordinates, axes
  units, and data unit can be supplied manually or via supplying the
  name of an extra coordinate if it is wanted to describe an
  axis. In the case of NDCube, the old API is currently still
  supported by will be removed in future versions. [#98 #103]

Bug Fixes
---------
- Allowed `~ndcube.NDCubeBase.axis_world_coords` to accept negative
  axis indices as arguments. [#106]
- Fixed bug in ``NDCube.crop_by_coords`` in case where real world
  coordinate system was rotated relative to pixel grid. [#113].
- `~ndcube.NDCubeBase.world_axis_physical_types` is now not
  case-sensitive to the CTYPE values in the WCS. [#109]
- `~ndcube.NDCubeBase.plot` now generates a 1-D line animation when
  image_axis is an integer.


1.0.1
==================

New Features
------------
- Added installation instructions to docs. [#77]

Bug Fixes
---------
- Fixed bugs in ``NDCubeSequence`` slicing and
  ``NDCubeSequence.dimensions`` in cases where sub-cubes contain
  scalar ``.data``. [#79]
- Fixed ``NDCube.world_axis_physical_types`` in cases where there is a
  ``missing`` WCS axis. [#80]
- Fixed bugs in converting between negative data and WCS axis
  numbers. [#91]
- Add installation instruction to docs. [#77]
- Fix function name called within NDCubeSequence.plot animation update
  plot. [#95]
