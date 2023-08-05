from sqlalchemy import Column, Integer, String, ForeignKeyConstraint, Numeric, DateTime
from sqlalchemy.orm import relationship

from captif_db.models.base import Table, Base


__all__ = [
    "DynamicStrainSession",
    "DynamicStrainReading",
    "DynamicStrainTrace",
]


class DynamicStrainSession(Table, Base):
    """
    Dynamic strain testing session.

    :param project_id: project ID (required)
    :param interval_id: interval ID (required)
    :param session_id: measurement session ID (required)
    :param track_condition: track condition during measurements (i.e. "before
        repair/surfacing (if any)" or "after repair/surfacing") (required)
    :param track_moisture: "wet" or "dry" (required)
    :param trigger_method: "indexed" or "photo" (required)
    :param datetime: datetime of start of measurement session (required)
    :param notes: general notes, purpose of measurement session

    :relationships: - interval_obj
                    - track_condition_obj
                    - track_moisture_obj
                    - dynamic_strain_reading_obj

    """

    __tablename__ = "dynamic_strain_session"
    __index_column__ = ["project_id", "interval_id", "session_id"]

    project_id = Column(Integer, primary_key=True)
    interval_id = Column(Integer, primary_key=True)
    session_id = Column(Integer, primary_key=True)
    track_condition = Column(String(50), nullable=False)
    track_moisture = Column(String(20), nullable=False)
    trigger_method = Column(String(20), nullable=False)
    load_kn = Column(Integer, nullable=False)
    datetime = Column(
        DateTime,
        nullable=False,
        comment="datetime of start of measurement session (used to determine lap_count)",
    )
    notes = Column(String(200))

    # Relationships:
    interval_obj = relationship("Interval", lazy=True)
    track_condition_obj = relationship("TrackConditionReference", lazy=True)
    track_moisture_obj = relationship("TrackMoistureReference", lazy=True)
    trigger_method_obj = relationship("TriggerMethodReference", lazy=True)
    dynamic_strain_reading_obj = relationship("DynamicStrainReading", lazy=True)

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
            ["track_moisture"], ["track_moisture_reference.track_moisture"],
        ),
        ForeignKeyConstraint(
            ["trigger_method"], ["trigger_method_reference.trigger_method"],
        ),
        {"info": {"er_tags": ["readings", "interval", "dynamic_strain"]}},
    )


class DynamicStrainReading(Table, Base):
    """
    Dynamic strain reading.

    :param id: index
    :param project_id: project ID (required)
    :param interval_id: interval ID (required)
    :param session_id: measurement session ID (required)
    :param section_id: section ID (required)
    :param sensor_position_id:

    :param lap_count: lap count of trace recording (required)
    :param datetime: datetime of the reading (required)
    :param coil_spacing_mm: static coil spacing (mm)
    :param vehicle_speed_kph: vehicle speed (km/h)
    :param vehicle_position_cm: vehicle position (cm)
    :param sampling_frequency_hz: sampling frequency (Hz)
    :param high_pass_cutoff_hz: highpass filter cutoff frequency (Hz)
    :param airbag_pressure_kpa: airbag pressure (kPa)
    :param peak_strain_um_mm: peak strain (micrometres/mm)
    :param max_tensile_strain_um_mm: maximum tensile strain (micrometres/mm)
    :param max_compressive_strain_um_mm: maximum compressive strain (micrometres/mm)
    :param max_tensile_strain_trace_index: trace index of the maximum tensile strain
    :param max_compressive_strain_trace_index: trace index of the maximum compressive strain


    :param control_reading: control reading (True/False). Default: False
    :param datetime: datetime of reading (required)
    :param rut_depth_mm: rut depth (mm) (required)
    :param rut_depth_mm_secondary_wheel_path: rut depth (mm) of the rut in the secondary
        wheel path. This is used where a dual wheel path track configuration is used. The
        secondary position will relate to vehicle B.

    :relationships: - session_obj
                    - trace_obj

    """

    __tablename__ = "dynamic_strain_reading"
    __index_column__ = "id"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    interval_id = Column(Integer, nullable=False)
    session_id = Column(Integer, nullable=False)
    section_id = Column(String(1), nullable=False)
    sensor_position_id = Column(String(20), nullable=False)
    lap_count = Column(Integer, nullable=False)
    datetime = Column(DateTime, nullable=False)
    coil_spacing_mm = Column(Numeric(5, 3), nullable=True)
    vehicle_speed_kph = Column(Numeric(3, 1), nullable=True)
    vehicle_position_cm = Column(Integer, nullable=True)
    sampling_frequency_hz = Column(Integer, nullable=True)
    high_pass_cutoff_hz = Column(Integer, nullable=True)
    airbag_pressure_kpa = Column(Numeric(4, 1), nullable=True)
    peak_strain_um_mm = Column(Integer, nullable=True)
    max_tensile_strain_um_mm = Column(Integer, nullable=True)
    max_compressive_strain_um_mm = Column(Integer, nullable=True)
    max_tensile_strain_trace_index = Column(Integer, nullable=True)
    max_compressive_strain_trace_index = Column(Integer, nullable=True)

    # Relationships:
    strain_coil_pair_obj = relationship("StrainCoilPair", lazy=True, viewonly=True)
    session_obj = relationship("DynamicStrainSession", lazy=True)
    trace_obj = relationship("DynamicStrainTrace", lazy=True)

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["project_id", "section_id", "sensor_position_id"],
            [
                "strain_coil_pair.project_id",
                "strain_coil_pair.section_id",
                "strain_coil_pair.sensor_position_id",
            ],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        ForeignKeyConstraint(
            ["project_id", "interval_id", "session_id"],
            [
                "dynamic_strain_session.project_id",
                "dynamic_strain_session.interval_id",
                "dynamic_strain_session.session_id",
            ],
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        {"info": {"er_tags": ["readings", "interval", "dynamic_strain"]}},
    )


class DynamicStrainTrace(Table, Base):
    """
    Dynamic strain trace.

    :param reading_id: dynamic strain reading ID (required)
    :param sample_no: trace sample number (required)
    :param coil_spacing_mm: coil spacing (mm) (required)
    :param raw_strain_um_mm: raw strain value (micrometres/mm)
    :param filtered_strain_um_mm: filtered strain value (micrometres/mm)

    :relationships: - reading_obj

    """

    __tablename__ = "dynamic_strain_trace"
    __index_column__ = ["reading_id", "sample_no"]

    # Fields:
    reading_id = Column(Integer, primary_key=True)
    sample_no = Column(Integer, primary_key=True)
    coil_spacing_mm = Column(Numeric(8, 6), nullable=False)
    raw_strain_um_mm = Column(Integer, nullable=True)
    filtered_strain_um_mm = Column(Integer, nullable=True)

    # Relationships:
    reading_obj = relationship("DynamicStrainReading", lazy=True)

    # Foreign keys:
    __table_args__ = (
        ForeignKeyConstraint(
            ["reading_id"], ["dynamic_strain_reading.id"], ondelete="CASCADE"
        ),
        {"info": {"er_tags": ["readings", "interval", "dynamic_strain"]}},
    )
