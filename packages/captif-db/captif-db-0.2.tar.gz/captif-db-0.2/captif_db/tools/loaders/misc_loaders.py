import pandas as pd

from captif_db.models import LapCount
from captif_db.logging import create_logger
from captif_db.helpers.models import query_to_frame

from .generic_loaders import Loader
from .continuous_loaders import ContinuousStrainLoader


__all__ = [
    "LapCountLoader",
    "StaticStrainLapCountLoader",
]

logger = create_logger(__name__)


class LapCountLoader(Loader):
    raw_file_fields = ["lap_count", "date", "time"]

    def load_raw(self, path):
        df = pd.read_csv(path, skiprows=1, sep="\t", names=self.raw_file_fields)
        df.drop_duplicates("lap_count", inplace=True)

        df = self.combine_date_time(df)

        df["project_id"] = self.project_id  # Append project_id column
        df = df.where(pd.notnull(df), None)  # Convert NaN to None

        return self.validate(df)

    def upload(self, db_session):
        new_readings = self.new_readings(
            db_session, self.raw_readings, project_id=self.project_id
        )

        logger.info(f"adding {len(new_readings)} rows to lap_count table")

        lap_count_objs = []
        for _, row in new_readings.iterrows():
            reading_dict = row.to_dict()
            reading_dict["datetime"] = reading_dict["datetime"].to_pydatetime()

            lap_count_objs.append(LapCount(**reading_dict))

        db_session.bulk_save_objects(lap_count_objs)
        db_session.commit()

    @staticmethod
    def validate(df):
        is_valid = df["lap_count"] > 0
        return df.loc[is_valid]

    @staticmethod
    def current_lap_count(db_session, project_id):
        lap_count = (
            db_session.query(LapCount)
            .filter_by(project_id=project_id)
            .order_by(LapCount.datetime.desc())
            .first()
        )
        return lap_count.lap_count if lap_count else 0

    def new_readings(self, db_session, readings, project_id):
        lap_count = self.current_lap_count(db_session, project_id=project_id)
        return readings.loc[readings["lap_count"] > lap_count]


class StaticStrainLapCountLoader(ContinuousStrainLoader):
    """
    Loader object for lap counts stored in the static strain measurement file.

    """

    @staticmethod
    def extract_unique_lap_counts(df):
        return df.sort_values("datetime").drop_duplicates("lap_count", keep="first")

    @staticmethod
    def extract_missing_lap_counts(df_db, df_new):
        df_missing = df_new.loc[~df_new["lap_count"].isin(df_db["lap_count"])]
        df_missing = df_missing.loc[df_missing["lap_count"] > 0]
        return df_missing

    def upload(self, db_session):
        database_lap_counts = query_to_frame(db_session.query(LapCount))
        sensor_lap_counts = self.extract_unique_lap_counts(self.raw_readings)

        extra_lap_counts = self.extract_missing_lap_counts(
            database_lap_counts, sensor_lap_counts,
        )

        logger.info(f"adding {len(extra_lap_counts)} rows to lap_count table")

        lap_count_objs = []
        for _, row in extra_lap_counts.iterrows():
            lap_count_objs.append(
                LapCount(
                    project_id=self.project_id,
                    datetime=row["datetime"].to_pydatetime(),
                    lap_count=row["lap_count"],
                )
            )

        db_session.bulk_save_objects(lap_count_objs)
        db_session.commit()
