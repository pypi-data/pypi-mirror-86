"""
The surface profile models are used to describe the surface profiler instruments and
associated measurements.
"""

from sqlalchemy import Column, Integer, String, ForeignKeyConstraint, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from captif_db.models.base import Table, Base


__all__ = [
    "SurfaceProfilerType",
    "SurfaceProfiler",
    "SurfaceProfilerVersion",
    "SurfaceProfilerSession",
    "SurfaceProfilerReading",
    "SurfaceProfilerTrace",
]


class SurfaceProfilerType(Table, Base):
    """
    Surface profiler type.

    :param surface_profiler_type: surface profiler type (e.g. wheel profiler) (required)

    """

    __tablename__ = "surface_profiler_type"
    __index_column__ = "surface_profiler_type"

    # Fields:
    surface_profiler_type = Column(String(50), primary_key=True)

    # Relationships:
    surface_profiler_obj = relationship("SurfaceProfiler", lazy=True)

    __table_args__ = (
        {"info": {"er_tags": ["readings", "interval", "surface_profiler"]}},
    )


class SurfaceProfiler(Table, Base):
    """
    Surface profiler instrument details.

    :param name: surface profiler instrument name (e.g. CAPTIF wheel surface profiler)
        (required)
    :param surface_profiler_type: type of surface profiler (required)

    :relationships: - surface_profiler_type_obj
                    - surface_profiler_version_obj

    """

    __tablename__ = "surface_profiler"
    __index_column__ = "name"

    # Fields:
    name = Column(String(50), primary_key=True)
    surface_profiler_type = Column(String(50), nullable=False)

    # Relationships:
    surface_profiler_type_obj = relationship("SurfaceProfilerType", lazy=True)
    surface_profiler_version_obj = relationship("SurfaceProfilerVersion", lazy=True)

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["surface_profiler_type"], ["surface_profiler_type.surface_profiler_type"],
        ),
        {"info": {"er_tags": ["readings", "interval", "surface_profiler"]}},
    )


class SurfaceProfilerVersion(Table, Base):
    """
    Surface profiler version details.

    Used to track changes to the instrument following identification of faults or general
    improvements.

    :param surface_profiler_name: surface profiler instrument name (required)
    :param version_no: version number (required)
    :param version_details: details of changes from the previous version (required)
    :param version_notes: additional notes

    :relationships: - surface_profiler_obj

    """

    __tablename__ = "surface_profiler_version"
    __index_column__ = ["surface_profiler_name", "version_no"]

    # Fields:
    surface_profiler_name = Column(String(50), primary_key=True)
    version_no = Column(Integer, primary_key=True)
    version_details = Column(String(100), nullable=False)
    version_notes = Column(String(200))

    # Relationships:
    surface_profiler_obj = relationship("SurfaceProfiler", lazy=True)

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["surface_profiler_name"], ["surface_profiler.name"], onupdate="CASCADE",
        ),
        {"info": {"er_tags": ["readings", "interval", "surface_profiler"]}},
    )


class SurfaceProfilerSession(Table, Base):
    """
    Surface profile testing session.

    :param project_id: project ID (required)
    :param interval_id: interval ID (required)
    :param session_id: measurement session ID (required)
    :param track_condition: track condition during measurements (i.e. "before
        repair/surfacing (if any)" or "after repair/surfacing") (required)
    :param datetime: datetime of start of measurement session (required)
    :param surface_profiler_name: surface profiler name (required)
    :param surface_profiler_version_no: version number (required)
    :param file: measurement file reference
    :param notes: general notes, purpose of measurement session

    :relationships: - interval_obj
                    - track_condition_obj
                    - surface_profiler_obj
                    - surface_profiler_version_obj
                    - surface_profiler_reading_obj

    """

    __tablename__ = "surface_profiler_session"
    __index_column__ = ["project_id", "interval_id", "session_id"]

    project_id = Column(Integer, primary_key=True)
    interval_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, primary_key=True)
    track_condition = Column(String(50), nullable=False)
    datetime = Column(
        DateTime,
        nullable=False,
        comment="datetime of start of measurement session (used to determine lap_count)",
    )
    surface_profiler_name = Column(String(50), nullable=False)
    surface_profiler_version_no = Column(Integer, nullable=False)
    file = Column(String(100))
    notes = Column(String(200))

    # Relationships:
    interval_obj = relationship("Interval", lazy=True)
    track_condition_obj = relationship("TrackConditionReference", lazy=True)
    surface_profiler_obj = relationship(
        "SurfaceProfiler",
        lazy=True,
        secondary="surface_profiler_version",
        uselist=False,
    )
    surface_profiler_version_obj = relationship("SurfaceProfilerVersion", lazy=True)
    surface_profiler_reading_obj = relationship("SurfaceProfilerReading", lazy=True)

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id", "interval_id"],
            ["interval.project_id", "interval.interval_id"],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        ForeignKeyConstraint(
            ["track_condition"], ["track_condition_reference.track_condition"],
        ),
        ForeignKeyConstraint(
            ["surface_profiler_name", "surface_profiler_version_no"],
            [
                "surface_profiler_version.surface_profiler_name",
                "surface_profiler_version.version_no",
            ],
            onupdate="CASCADE",
        ),
        {"info": {"er_tags": ["readings", "interval", "surface_profiler"]}},
    )


class SurfaceProfilerReading(Table, Base):
    """
    Surface profiler reading.

    :param id: index
    :param project_id: project ID (required)
    :param interval_id: interval ID (required)
    :param session_id: measurement session ID (required)
    :param session_reading_no: session reading number (required)
    :param station_no: station number
    :param control_reading: control reading (True/False). Default: False
    :param datetime: datetime of reading (required)
    :param rut_depth_mm: rut depth (mm) (required)
    :param rut_depth_mm_secondary_wheel_path: rut depth (mm) of the rut in the secondary
        wheel path. This is used where a dual wheel path track configuration is used. The
        secondary position will relate to vehicle B.

    :relationships: - session_obj
                    - trace_obj

    """

    __tablename__ = "surface_profiler_reading"
    __index_column__ = "id"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    interval_id = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    session_reading_no = Column(Integer, nullable=False)
    station_no = Column(Integer, nullable=True)
    control_reading = Column(Boolean, nullable=False, default=False)
    datetime = Column(DateTime, nullable=False)
    rut_depth_mm = Column(Numeric(4, 1), nullable=False)
    rut_depth_mm_secondary_wheel_path = Column(Numeric(4, 1), nullable=True)

    # Relationships:
    session_obj = relationship("SurfaceProfilerSession", lazy=True)
    trace_obj = relationship("SurfaceProfilerTrace", lazy=True)

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id", "interval_id", "session_id"],
            [
                "surface_profiler_session.project_id",
                "surface_profiler_session.interval_id",
                "surface_profiler_session.session_id",
            ],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        ForeignKeyConstraint(
            ["project_id", "station_no"], ["station.project_id", "station.station_no"],
        ),
        {"info": {"er_tags": ["readings", "interval", "surface_profiler"]}},
    )


class SurfaceProfilerTrace(Table, Base):
    """
    Surface profiler reading trace value.

    :param reading_id: surface profiler reading ID (required)
    :param distance_mm: position of the profiler (mm) (required)
    :param relative_height_mm: height of the surface relative to the datum (mm) (required)

    :relationships: - reading_obj

    """

    __tablename__ = "surface_profiler_trace"
    __index_column__ = ["reading_id", "distance_mm"]

    reading_id = Column(Integer, primary_key=True)
    distance_mm = Column(Numeric(5, 1), primary_key=True)
    relative_height_mm = Column(Numeric(6, 3), nullable=False)

    # Relationships:
    reading_obj = relationship("SurfaceProfilerReading", lazy=True)

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["reading_id"], ["surface_profiler_reading.id"], ondelete="CASCADE"
        ),
        {"info": {"er_tags": ["readings", "interval", "surface_profiler"]}},
    )
