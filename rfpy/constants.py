# AUTOGENERATED! DO NOT EDIT! File to edit: 04_constants.ipynb (unless otherwise specified).

__all__ = ['BYTES_HEADER', 'DATA_BLOCK_HEADER', 'CHECKSUM', 'ENDMARKER', 'LEN_MARKER', 'BASEBLOCK', 'EXCLUDE_ATTRS',
           'DICT_PROCESSING', 'DICT_UNIT', 'TUNING_BLOCK', 'BYTES_TIMED', 'BYTES_TIMED_NE', 'BYTES_6', 'BYTES_20',
           'BYTES_21', 'BYTES_24', 'BYTES_40', 'BYTES_41', 'BYTES_42', 'BYTES_51', 'BYTES_63', 'BYTES_64', 'BYTES_65',
           'BYTES_V5', 'BYTES_66', 'BYTES_67', 'META', 'LEVELS', 'BLOCK_SIZE', 'TIMED_BLOCKS']

# Cell
from typing import Mapping, List

BYTES_HEADER = 36

DATA_BLOCK_HEADER = 12

CHECKSUM = 4

ENDMARKER: bytes = b'\x00UUUU'

LEN_MARKER: int = 5

BASEBLOCK: List = ['thread_id', 'data_size', 'type', 'data', 'checksum']

EXCLUDE_ATTRS: List = ['count', 'index', 'checksum', 'default', 'date', 'time', 'nanosecs', 'data',
                 'block_data', 'frequencies', 'agc_array', 'tunning_info']

DICT_PROCESSING: Mapping[int, str] = {0: 'single measurement', 1: 'average', 2: 'peak', 3: 'minimum'}

DICT_UNIT: Mapping[int, str] = {0: '%', 1: 'dBm', 2: 'dBuV/m'}

TUNING_BLOCK: Mapping[int, str] = {0: 'completed without error',
                                   1: 'error occurred',
                                   2: 'radio produced an error',
                                   3: 'GPRS transmission occured during capture',
                                   4: 'ADC overflowed during capture'}


BYTES_TIMED: Mapping[int, slice] = { 0:  slice(0,4),
                                    1:  slice(4,8),
                                    2:  slice(8,12),
                                    3:  slice(12,14),
                                    4:  slice(14,18),
                                    5:  slice(18,20),
                                    6:  slice(20,24),
                                    7:  slice(24,26),
                                    8:  slice(26,28)}

BYTES_TIMED_NE: Mapping[int, slice] = {0:  slice(0,4),
                  1:  slice(4,8),
                  2:  slice(8,12)}

BYTES_6: Mapping[int, slice] = {0:  slice(0,4),
           1:  slice(4,8),
           2:  slice(8,12),
           3:  slice(12,16),
           4:  slice(16,20),
           5:  slice(20,24)}

BYTES_20: Mapping[int, slice] = {0:  slice(0,4),
            1:  slice(4,8),
            2:  slice(8,12),
            3:  slice(12,16),
            4:  slice(16,20),
            5:  slice(20,24),
            6:  slice(24,28),
            7:  slice(28,32),
            8:  slice(32,36),
            9:  slice(36,40)
           }


BYTES_21: Mapping[int, slice] = {0: slice(0,16),
            1: slice(16,20)}

BYTES_24: Mapping[int, slice] = {0: slice(0, 4),
            1: slice(4, 8)}

BYTES_40: Mapping[int, slice] = {3: slice(12,16),
            4: slice(16,20),
            5: slice(20,21),
            6: slice(21,22),
            7: slice(22,24),
            8: slice(24,28),
            9: slice(28,32),
            10: slice(32,36),
            11: slice(36,40)}

BYTES_41: Mapping[int, slice] = {3: slice(12,44),
            4: slice(44,48)}

BYTES_42: Mapping[int, slice] = {3: slice(12,16),
            4: slice(16,20),
            5: slice(20,52),
            6: slice(52,56)}

BYTES_51: Mapping[int, slice] = {5: slice(20,24)}

BYTES_63: Mapping[int, slice] = {9:  slice(28,32),
            10: slice(32,36),
            11: slice(36,37),
            12: slice(37,38),
            13: slice(38,39),
            14: slice(39,40),
            15: slice(40,41),
            16: slice(41,42),
            17: slice(42,43),
            18: slice(43,45),
            19: slice(45,47),
            20: slice(47,48),
            21: slice(48,52)}

BYTES_64: Mapping[int, slice] = {22: slice(52,56), 23: slice(56,60)}

BYTES_65: Mapping[int, slice] = { 9:  slice(28,32),
             10: slice(32,33),
             11: slice(33,34),
             12: slice(34,36),
             13: slice(36,37),
             14: slice(37,38),
             15: slice(38,39),
             16: slice(39,40),
             17: slice(40,42),
             18: slice(42,44),
             19: slice(44,48)}

BYTES_V5: Mapping[int, slice] = {3: slice(12,16),
            4: slice(16,20),
            5: slice(20,24)}

BYTES_66: Mapping[int, slice] = {3: slice(12,16),
            4: slice(16,20),
            5: slice(20,24)}

BYTES_67: Mapping[int, slice] = {3: slice(12,16),
            4: slice(16,20),
            5: slice(20,24)}

# Cell
META = {'Block_Number': 'uint16',
     'Latitude': 'float32',
     'Longitude': 'float32',
     'Altitude': 'float16',
     'Initial_Time': 'datetime64[ns]',
     'Sample_Duration': 'uint16',
     'Start_Frequency': 'uint32',
     'Stop_Frequency': 'uint32',
     'Vector_Length': 'uint16',
     'Trace_Type': 'category',
     'Antenna_Type': 'category',
     'Equipement_ID': 'category'}

LEVELS = {'Block_Number': 'category', 'Frequency(MHz)': 'float32', "Nivel(dBm)" : 'float16'}

BLOCK_SIZE = 4096

TIMED_BLOCKS = [40,41,42,51,63,64,65,66,67,68,69]