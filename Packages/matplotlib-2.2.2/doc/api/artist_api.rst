.. _artist-api:

===================
 ``artist`` Module
===================

.. inheritance-diagram:: matplotlib.axes._axes.Axes matplotlib.axes._base._AxesBase matplotlib.axis.Axis matplotlib.axis.Tick matplotlib.axis.XAxis matplotlib.axis.XTick matplotlib.axis.YAxis matplotlib.axis.YTick matplotlib.collections.AsteriskPolygonCollection matplotlib.collections.BrokenBarHCollection matplotlib.collections.CircleCollection matplotlib.collections.Collection matplotlib.collections.EllipseCollection matplotlib.collections.EventCollection matplotlib.collections.LineCollection matplotlib.collections.PatchCollection matplotlib.collections.PathCollection matplotlib.collections.PolyCollection matplotlib.collections.QuadMesh matplotlib.collections.RegularPolyCollection matplotlib.collections.StarPolygonCollection matplotlib.collections.TriMesh matplotlib.collections._CollectionWithSizes matplotlib.contour.ClabelText matplotlib.figure.Figure matplotlib.image.AxesImage matplotlib.image.BboxImage matplotlib.image.FigureImage matplotlib.image.NonUniformImage matplotlib.image.PcolorImage matplotlib.image._ImageBase matplotlib.legend.Legend matplotlib.lines.Line2D matplotlib.offsetbox.AnchoredOffsetbox matplotlib.offsetbox.AnchoredText matplotlib.offsetbox.AnnotationBbox matplotlib.offsetbox.AuxTransformBox matplotlib.offsetbox.DrawingArea matplotlib.offsetbox.HPacker matplotlib.offsetbox.OffsetBox matplotlib.offsetbox.OffsetImage matplotlib.offsetbox.PackerBase matplotlib.offsetbox.PaddedBox matplotlib.offsetbox.TextArea matplotlib.offsetbox.VPacker matplotlib.patches.Arc matplotlib.patches.Arrow matplotlib.patches.Circle matplotlib.patches.CirclePolygon matplotlib.patches.ConnectionPatch matplotlib.patches.Ellipse matplotlib.patches.FancyArrow matplotlib.patches.FancyArrowPatch matplotlib.patches.FancyBboxPatch matplotlib.patches.Patch matplotlib.patches.PathPatch matplotlib.patches.Polygon matplotlib.patches.Rectangle matplotlib.patches.RegularPolygon matplotlib.patches.Shadow matplotlib.patches.Wedge matplotlib.patches.YAArrow matplotlib.projections.geo.AitoffAxes matplotlib.projections.geo.GeoAxes matplotlib.projections.geo.HammerAxes matplotlib.projections.geo.LambertAxes matplotlib.projections.geo.MollweideAxes matplotlib.projections.polar.PolarAxes matplotlib.quiver.Barbs matplotlib.quiver.Quiver matplotlib.quiver.QuiverKey matplotlib.spines.Spine matplotlib.table.Cell matplotlib.table.CustomCell matplotlib.table.Table matplotlib.text.Annotation matplotlib.text.Text matplotlib.text.TextWithDash
   :parts: 1
   :private-bases:



.. automodule:: matplotlib.artist
   :no-members:
   :no-undoc-members:


``Artist`` class
================

.. autoclass:: Artist
   :no-members:
   :no-undoc-members:

Interactive
-----------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.add_callback
   Artist.format_cursor_data
   Artist.get_contains
   Artist.get_cursor_data
   Artist.get_picker
   Artist.mouseover
   Artist.pchanged
   Artist.pick
   Artist.pickable
   Artist.remove_callback
   Artist.set_contains
   Artist.set_picker
   Artist.contains

Margins and Autoscaling
-----------------------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.sticky_edges

Clipping
--------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.get_clip_box
   Artist.get_clip_on
   Artist.get_clip_path
   Artist.set_clip_box
   Artist.set_clip_on
   Artist.set_clip_path

Bulk Properties
---------------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.update
   Artist.update_from
   Artist.properties
   Artist.set

Drawing
-------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.draw
   Artist.get_animated
   Artist.set_animated

   Artist.get_agg_filter

   Artist.get_alpha
   Artist.get_snap
   Artist.get_visible
   Artist.get_zorder
   Artist.set_agg_filter
   Artist.set_alpha

   Artist.set_sketch_params
   Artist.set_snap
   Artist.get_rasterized
   Artist.get_sketch_params
   Artist.set_path_effects
   Artist.set_rasterized
   Artist.zorder
   Artist.set_visible
   Artist.set_zorder
   Artist.get_window_extent
   Artist.get_path_effects
   Artist.get_transformed_clip_path_and_affine

Figure and Axes
---------------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.remove

   Artist.axes

   Artist.set_figure
   Artist.get_figure

Children
--------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.get_children
   Artist.findobj

Transform
---------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.set_transform
   Artist.get_transform
   Artist.is_transform_set

Units
-----

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.convert_xunits
   Artist.convert_yunits
   Artist.have_units

Metadata
--------

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.get_gid
   Artist.get_label
   Artist.set_gid
   Artist.set_label
   Artist.get_url
   Artist.set_url
   Artist.aname

Stale
-----

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   Artist.stale

Functions
=========

.. autosummary::
   :toctree: _as_gen
   :nosignatures:

   allow_rasterization
   get
   getp
   setp
   kwdoc
   ArtistInspector
