from collections import defaultdict
import csv
import numpy as np
import pandas as pd

from captif_db.models import (
    DeflectionBeamSession,
    DeflectionBeamReading,
    DeflectionBeamTrace,
    SurfaceProfilerReading,
    SurfaceProfilerSession,
    SurfaceProfilerTrace,
    StrainCoilPair,
    DynamicStrainReading,
    DynamicStrainSession,
    DynamicStrainTrace,
)
from captif_db.helpers.parse_datetime import to_datetime, is_datetime
from captif_db.helpers.parse_number import to_number, is_number

from .generic_loaders import DynamicIntervalLoader, StationIntervalLoader


__all__ = [
    "DeflectionBeamLoader",
    "SurfaceProfilerLoader",
    "DynamicStrainLoader",
]


"""
Deflection beam loader

"""

IGNORE_FIELDS = [
    "CF [Dpk-D200]",
    "Distance (m)",
    "Bowl Corrected",
    "Operator",
    "Max Deflection Corrected",
    "Latitude",
    "Longitude",
    "Load",
]
DEFLECTION_BEAM_READING_COLUMN_MAPPER = {
    "location": "station_no",
    "max_deflection_measured": "raw_max_deflection_mm",
}


class DeflectionBeamLoader(StationIntervalLoader):
    session_model = DeflectionBeamSession
    reading_model = DeflectionBeamReading
    trace_model = DeflectionBeamTrace
    reading_fields = ["raw_max_deflection_mm"]

    def load_raw(self):
        readings, reading = [], None

        with open(self.path.joinpath(self.session_info["filename"]), "r") as f:

            for line in csv.reader(f, delimiter="\t"):
                try:
                    kk, vv = line
                except ValueError:
                    continue

                if kk.strip(":") in IGNORE_FIELDS:
                    continue

                kk = self.safe_field_name(kk)

                if self.is_new_reading(kk):
                    if reading is not None:
                        readings.append(self.format_reading(reading))
                    reading = {"trace": []}

                if is_datetime(vv):
                    reading[kk] = to_datetime(vv)
                    continue

                if not is_number(kk):
                    if len(kk):
                        reading[kk] = to_number(vv)
                    continue

                try:
                    reading["trace"].append(
                        {"distance_m": float(kk), "raw_deflection_mm": float(vv)}
                    )
                except ValueError:
                    pass

            # Make sure to append the final reading in the file:
            readings.append(self.format_reading(reading))

        self.raw_readings = pd.DataFrame.from_records(readings).rename(
            columns=DEFLECTION_BEAM_READING_COLUMN_MAPPER
        )
        self.raw_readings["station_no"] = self.raw_readings["station_no"].astype(np.int)
        self.session_info["session"]["datetime"] = (
            self.raw_readings["datetime"].min().to_pydatetime()
        )

    @staticmethod
    def is_new_reading(s):
        return s == "date"

    @staticmethod
    def safe_field_name(s):
        return "_".join(s.strip(":").lower().split(" "))

    @staticmethod
    def format_reading(df):
        df["datetime"] = df.pop("date") + df.pop("time")
        return df


"""
Surface profiler loader

"""


class SurfaceProfilerLoader(StationIntervalLoader):
    session_model = SurfaceProfilerSession
    reading_model = SurfaceProfilerReading
    trace_model = SurfaceProfilerTrace

    profile_trace_file_fields = [
        "station_no",
        "date",
        "lap_count",
        "distance_mm",
        "relative_height_mm",
    ]
    reading_file_fields = [
        "station_no",
        "date",
        "lap_count",
        "wheel_path_cm",
        "rut_depth_mm",
    ]
    reading_fields = [
        "rut_depth_mm",
        "rut_depth_mm_secondary_wheel_path",
        "control_reading",
    ]
    trace_fields = ["distance_mm", "relative_height_mm"]

    def load_raw(self):

        self.raw_readings = self.load_single_file(
            self.path.joinpath(self.session_info["filename"]["reading_filename"]),
            self.reading_file_fields,
        )

        raw_traces = self.load_single_file(
            self.path.joinpath(self.session_info["filename"]["profile_trace_filename"]),
            self.profile_trace_file_fields,
        )

        self.raw_readings = self.append_traces_to_readings(
            self.raw_readings, raw_traces
        )
        self.raw_readings = self.set_control_reading_details(
            self.raw_readings, self.control_station_no()
        )

        # Convert NaN to None:
        self.raw_readings = self.raw_readings.where(pd.notnull(self.raw_readings), None)

        self.session_info["session"]["datetime"] = (
            self.raw_readings["datetime"].min().to_pydatetime()
        )

    def control_station_no(self):
        if "control" not in self.session_info.keys():
            return None
        return self.session_info["control"]["station_no"]

    @classmethod
    def append_traces_to_readings(cls, df, traces):
        reading_traces = []
        for ii, row in df.iterrows():
            selected_traces = traces.loc[traces["station_no"] == row["station_no"]]
            reading_traces.append(
                [rr.to_dict() for _, rr in selected_traces[cls.trace_fields].iterrows()]
            )
        df["trace"] = reading_traces
        return df

    @staticmethod
    def set_control_reading_details(df, control_station_no):
        df["control_reading"] = False
        is_control = df["station_no"] == control_station_no
        df.loc[is_control, "control_reading"] = True
        df.loc[is_control, "station_no"] = None
        return df

    @staticmethod
    def load_single_file(path, column_names):
        try:
            df = pd.read_csv(path, skiprows=1, sep="\t", names=column_names)

            df["station_no"] = df["station_no"].astype(np.int)
            df["datetime"] = df["date"].apply(to_datetime)
            df.drop(columns="date", inplace=True)
            return df

        except FileNotFoundError as e:
            raise FileNotFoundError(f"{path.name} not found") from e


"""
Dynamic strain loader

"""


class DynamicStrainLoader(DynamicIntervalLoader):
    session_model = DynamicStrainSession
    reading_model = DynamicStrainReading
    trace_model = DynamicStrainTrace
    sensor_position_model = StrainCoilPair

    profile_trace_file_fields = [
        "trace_id",
        "sample_no",
        "filtered_strain_um_mm",
        "raw_strain_um_mm",
        "coil_spacing_mm",
        "raw_signal_volts",
    ]

    reading_file_fields_mapper = {
        "Pair Name": "sensor_position_id",
        "Date": "date",
        "Depth": "depth_mm",
        "Orientation": "coil_pair_direction",
        "coil transverse  position": "vertical_stack_position",
        "station": "station_no",
        "loading Vehicle": "vehicle_id",
        "tyre type": "tyre",
        "trace identifier": "trace_id",
        "sampling freq": "sampling_frequency_hz",
        "low cutoff": "high_pass_cutoff_hz",
        "lapcount": "lap_count",
        "speed": "vehicle_speed_kph",
        "vehicle position": "vehicle_position_cm",
        "load": "load_kn",
        "airbag pressure": "airbag_pressure_kpa",
        "Peak Strain": "peak_strain_um_mm",
        "Max Tensile Strain": "max_tensile_strain_um_mm",
        "Max Compressive Strain": "max_compressive_strain_um_mm",
        "Max tensile strain index": "max_tensile_strain_trace_index",
        "Max Comp strain index": "max_compressive_strain_trace_index",
        "Static Spacing (mm)": "coil_spacing_mm",
        "Pavement Temp C": "temperature",
    }

    reading_fields = [
        "lap_count",
        "coil_spacing_mm",
        "vehicle_speed_kph",
        "vehicle_position_cm",
        "sampling_frequency_hz",
        "high_pass_cutoff_hz",
        "airbag_pressure_kpa",
        "peak_strain_um_mm",
        "max_tensile_strain_um_mm",
        "max_compressive_strain_um_mm",
        "max_tensile_strain_trace_index",
        "max_compressive_strain_trace_index",
    ]

    trace_fields = [
        "sample_no",
        "coil_spacing_mm",
        "raw_strain_um_mm",
        "filtered_strain_um_mm",
    ]

    reading_file_pattern = "dynamic strain data*"
    trace_file_pattern = "dynamic strain traces*"

    def load_raw(self):

        self.raw_readings = self.append_traces_to_readings(
            self.load_raw_readings(), self.load_raw_traces(),
        )

        # Append project_id column:
        self.raw_readings["project_id"] = self.project_id

        # Convert NaN to None:
        self.raw_readings = self.raw_readings.where(pd.notnull(self.raw_readings), None)

        self.session_info["session"]["datetime"] = (
            self.raw_readings["datetime"].min().to_pydatetime()
        )

    @classmethod
    def append_traces_to_readings(cls, df, traces):
        reading_traces_dict = defaultdict(list)
        for trace_id, gg in traces.groupby("trace_id"):
            reading_traces_dict["trace_id"].append(trace_id)
            reading_traces_dict["trace"].append(gg[cls.trace_fields].to_dict("records"))
        reading_traces = pd.DataFrame(reading_traces_dict).set_index("trace_id")

        df = df.join(reading_traces, on="trace_id")
        return df

    def load_raw_readings(self):
        df = pd.concat(
            [
                pd.read_csv(ff, sep="\t", index_col=None).rename(
                    columns=self.reading_file_fields_mapper
                )
                for ff in self.path.glob(self.reading_file_pattern)
            ],
            ignore_index=True,
        )
        df["datetime"] = df["date"].str.strip().apply(to_datetime)
        df.drop(columns="date", inplace=True)
        return df

    def load_raw_traces(self):
        df = pd.concat(
            [
                pd.read_csv(
                    ff,
                    skiprows=1,
                    sep="\t",
                    index_col=None,
                    names=self.profile_trace_file_fields,
                )
                for ff in self.path.glob(self.trace_file_pattern)
            ],
            ignore_index=True,
        )
        return df
