1.0.2 (2020-11-24)
------------------

- Fix compatibility with latest developer version of vispy. [#363]

1.0.1 (2020-10-02)
------------------

- Fix 'flip limits' button in 3D scatter plot. [#361]

- Fix the visual appearance of vectors. [#362]

1.0.0 (2020-09-17)
------------------

- Drop support for Python < 3.6. [#351, #353]

- No longer bundle vispy, and instead depend on the
  latest stable release. [#351]

- Add initial support for vectors and error bars.
  [#358]

0.12.2 (2019-06-24)
-------------------

- Fixed __version__ variable which was set to 'undefined'. [#344]

- Fixed configuration for tox testing tool. [#344]

0.12.1 (2019-06-23)
-------------------

- Fixed missing package data.

0.12 (2019-06-23)
-----------------

- Make it possible to view datasets that are linked but not on the same
  pixel grid together. Now also requires datasets to always be linked
  in order to be shown in the same viewer. [#335, #337]

- Fix compatibility with the latest developer version of glue. [#339, #342]

- Fix bug with hidden layers in the 3D scatter viewer becoming visible after
  saving and loading session file. [#340]

0.11 (2018-11-14)
-----------------

- Fixed the home button in the toolbar to reset limits in addition to the
  viewing angle. [#327]

- Fix a bug that caused crashes when not all scatter points were inside the
  3D scatter viewer box (due e.g. to panning and/or zooming) and color-coding
  of points was used. [#326]

- Fix a bug that caused an error when adding a dataset with an incompatible
  subset to a new 3D scatter viewer. [#323]

- Improve how we deal with reaching the limit of the number of free slots
  in the volume viewer. [#321]

- Make it so that selection tools are de-selected after use, to be
  consistent with the core glue behavior. [#320]

- Fixed a bug that caused layers to sometimes non-deterministically be
  shown/hidden and/or not disappear correctly. [#314]

- Implement the 'data' and 'outline' modes for volume rendering of subsets
  directly in the OpenGL shader. [#310]

- Make volume rendering be adaptive in terms of resolution - the buffer used
  for the rendering is a fixed size and the data in the buffer is updated as
  the user zooms in/out and pans around. [#312]

0.10 (2018-04-27)
-----------------

- Use new 3D and flood fill subset state classes from glue to make storing
  subsets much more efficient. [#301]

- Work around an issue on certain graphics cards which causes volume
  renderings to not appear correctly but instead of have stripe artifacts. [#303]

- Improve performance for volume rendering for arrays larger than 2048
  along one or more dimensions. [#303]

- Improve performance when closing a session that has large volume
  visualizations. [#307]

- Improve performance when clipping the data outside the box. [#307]

- Fixed a bug that caused layers to be shown/hidden out of sync with
  checkboxes. [#307]

- Fixed a bug that caused circular references to viewers to cause issues
  after the viewers were closed. [#307]

0.9.2 (2018-03-08)
------------------

- Fix bug that caused a crash when adding a volume to a viewer that
  already had a viewer and scatter layer. [#291]

0.9.1 (2018-01-09)
------------------

- Fix compatibility of 3D viewers with PyQt5 on Linux. [#287]

0.9 (2017-10-25)
----------------

- Improve performance for volume rendering. [#274]

- Fix layer artist icon when using colormaps. [#283]

- Fix bug that occurred when downsampling cubes with more than 2048 elements
  in one or more dimensions. [#277]

0.8 (2017-08-22)
----------------

- Update viewer code to use non-Qt-specific combo helpers. [#266]

- Fix compatibility of floodfill selection with recent Numpy versions. [#257, #267]

- Avoid errors when lower and upper limits in viewer options are equal. [#268]

- Fix bug that caused the color of scatter plots to not always update. [#265]

- Fix color and size encoding when using the data clip option. [#261]

- Added a home button that resets the view. [#254]

0.7.2 (2017-03-16)
------------------

- Fixed bug that caused session files saved after removing subsets
  to no longer be loadable. [#253]

- Fixed bug that caused record icon to appear multiple times when
  successively creating 3D viewers. [#252]

- Fixed bug with volume rendering on Windows with Python 2.7, due to
  Numpy .shape returning long integers. [#245]

- Fixed bug that caused the flipping of size and cmap limits in the
  3D viewers to not work properly. [#251]

0.7.1 (unreleased)
------------------

- Fixed bugs with 3D selections following refactoring. [#243]

- Fixed the case where vmin == vmax for size or color. [#243]

0.7 (2017-02-15)
----------------

- When multiple datasets are visible in a 3D view, selections now apply to
  all of them (except for point and point and drag selections, for which the
  selection applies to the currently selected layer). [#208]

- The selection tools have been refactored to use the new toolbar/tool
  infrastructure in glue. [#208]

- Update all layers in 3D viewers if numerical values change in any datasaet. [#236]

- Refactored the viewers to simplify the code and make development easier. [#238]

- Improve the default level selection for the isosurface viewer. [#238]

0.6 (2016-11-03)
----------------

- Fixed a bug that caused subsets to not be added to viewers when adding a
  dataset with already existing subsets. [#218]

- Fixed compatibility with Qt5. [#212]

- Fixed a bug that caused session files created previously to not be
  openable. [#213, #214]

- Fixed a bug that caused 3D selections to not work properly. [#219]

0.5 (2016-10-10)
----------------

- Fixed a bug that caused alpha scaling to not work correctly when mapping
  scatter marker colors to an attribute. [#201]

- Watch for ``NumericalDataChangedMessage`` messages. [#183, #184]

- Fixed a bug that caused color-coding and size-scaling of points in 3D viewer
  to not work for negative values. [#182, #185]

- Add support for overplotting scatter markers on top of volumes. [#200]

- Add support for n-dimensional components in 3D scatter plot viewer. [#158]

- Factor of ~10 improvement in performance when selecting data in the scatter
  or volume viewers. [#165]

- Make selection frame wider. [#161]

- Small fix of the camera initial settings & rotate speed . [#154]

- Advanced point-mode selection for scatter points. [#160]

- Experimental point-mode selection for volume viewer. [#159]

- Fix button to record animations when the user cancels the file save dialog.
  [#186]

- Fix Qt imports to use QtPy for new versions of glue. [#173, #178, #186]

- Add an option to clip any data outside the specified limits. [#203]

- Add a checkbox to force the aspect ratio to be native instead of
  making all axes the same length. [#205]

0.4 (2016-05-24)
----------------

- Bundle the latest developer version of VisPy. [#143, #144]

- Add a checkbox to toggle between near and far-field view. [#140]

- Support the options in Glue v0.8 for foreground and background colors in viewers. [#149]

- Fix a bug that caused subsets selected in the 3D viewers to be applied to
  datasets for which they aren't relevant. [#151]

0.3 (2016-05-04)
----------------

- Add selection toolbar and icons for 3D viewers. [#88, #92]

- Workaround OpenGL issue that caused cubes with size > 2048 along any
  dimension to not display. [#100]

- Implemented 3D selection. [#103]

- Fix issue with _update_data on base VisPy viewer. [#106]

- Make sure an error is raised if data is not 3-dimensional and shape doesn’t
  agree with existing data in volume viewer. [#112]

- Fix a bug that caused exceptions when clearing/removing layer artists. [#117]

- Optimize the layout of options for the layer style editors to save space. [#120]

- Added the ability to save static images of the 3D viewers. [#125]

- Add toolbar icon to continuously rotate the view. [#128][#137]

- Raise an explicit error if PyOpenGL is not installed. [#129]

- Implement support for saving 3D viewers in session files. [#130]

- Fix bug that caused all layers in the 3D scatter viewer to disappear when
  one layer was removed. [#131]

- Make sure the 3D viewer is updated if the zorder is set manually. [#132]

- Added ``BACKGROUND_COLOR`` and ``FOREGROUND_COLOR`` settings at root of package. [#134]

- Make sure combo boxes don't expand if component names are long. [#135]

- Travis: add back testing against stable glue [#136]

- Save animation with imageio. [#139]

- Add toggle for perspective view. [#140]

- Bundle latest developer version of Vispy. [#143] [#144]



0.2 (2015-03-11)
----------------

- Significant work has gone into making the scatter and volume viewers
  functional. Subsets can be highlighted in either viewer.

0.1 (2015-10-19)
----------------

- Initial release, includes simple volume viewer.
