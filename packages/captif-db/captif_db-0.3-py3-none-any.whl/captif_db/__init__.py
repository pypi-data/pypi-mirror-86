__version__ = "0.3"


from captif_db.models.reference import TriggerMethodReference
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, event

from sqlalchemy_utils.functions import create_database, drop_database, database_exists

from captif_db_config import database_connection_str, get_config_param

import captif_db.models  # noqa
from captif_db.models import (
    Base,
    StationReference,
    RepairWidthReference,
    StrainCoilPairDirectionReference,
    StrainCoilPositionReference,
    TrackConditionReference,
    TrackMoistureReference,
)
from captif_db.models.constants import (
    REPAIR_WIDTH_VALUES,
    STRAIN_COIL_PAIR_DIRECTION_VALUES,
    STRAIN_COIL_POSITION_VALUES,
    TRACK_CONDITION_VALUES,
    TRACK_MOISTURE_VALUES,
    TRIGGER_METHOD_VALUES,
)

from . import models, tools, helpers  # noqa


class DbSession:
    factory = None
    engine = None

    @staticmethod
    def global_init(test_db=False, overwrite_test_db=True, echo=None):
        if DbSession.factory:
            return

        database = get_config_param("database")
        if test_db:
            database += "_test"

        if echo is None:
            echo = test_db

        engine = create_engine(database_connection_str(database), echo=echo)
        DbSession.engine = engine
        DbSession.factory = sessionmaker(bind=engine)

        if database_exists(engine.url):
            if test_db and overwrite_test_db:
                drop_database(engine.url)
                create_database(engine.url)
        else:
            create_database(engine.url)

        Base.metadata.create_all(engine)


@event.listens_for(StationReference.__table__, "after_create")
def _insert_station_values(target, connection, **kwargs):
    session = DbSession.factory()
    for station_no in range(60):
        session.add(StationReference(station_no=station_no))
    session.commit()
    session.close()


@event.listens_for(RepairWidthReference.__table__, "after_create")
def _insert_repair_width_values(target, connection, **kwargs):
    session = DbSession.factory()
    for vv in REPAIR_WIDTH_VALUES:
        session.add(RepairWidthReference(width=vv))
    session.commit()
    session.close()


@event.listens_for(TrackConditionReference.__table__, "after_create")
def _insert_track_condition_values(target, connection, **kwargs):
    session = DbSession.factory()
    for vv in TRACK_CONDITION_VALUES:
        session.add(TrackConditionReference(track_condition=vv))
    session.commit()
    session.close()


@event.listens_for(TrackMoistureReference.__table__, "after_create")
def _insert_track_moisture_values(target, connection, **kwargs):
    session = DbSession.factory()
    for vv in TRACK_MOISTURE_VALUES:
        session.add(TrackMoistureReference(track_moisture=vv))
    session.commit()
    session.close()


@event.listens_for(TriggerMethodReference.__table__, "after_create")
def _insert_trigger_method_values(target, connection, **kwargs):
    session = DbSession.factory()
    for vv in TRIGGER_METHOD_VALUES:
        session.add(TriggerMethodReference(trigger_method=vv))
    session.commit()
    session.close()


@event.listens_for(StrainCoilPositionReference.__table__, "after_create")
def _insert_strain_coil_position_values(target, connection, **kwargs):
    session = DbSession.factory()
    for vv in STRAIN_COIL_POSITION_VALUES:
        session.add(StrainCoilPositionReference(coil_position=vv))
    session.commit()
    session.close()


@event.listens_for(StrainCoilPairDirectionReference.__table__, "after_create")
def _insert_strain_coil_pair_direction_values(target, connection, **kwargs):
    session = DbSession.factory()
    for vv in STRAIN_COIL_PAIR_DIRECTION_VALUES:
        session.add(StrainCoilPairDirectionReference(coil_pair_direction=vv))
    session.commit()
    session.close()
