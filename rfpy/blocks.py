# AUTOGENERATED! DO NOT EDIT! File to edit: 04_blocks.ipynb (unless otherwise specified).

__all__ = ['path_type', 'bin_val', 'bytes_encoded', 'datetime_object', 'create_base_block', 'BASEBLOCK',
           'dict_processing', 'dict_unit', 'TimedBlock', 'DType21', 'DType40', 'DataType63']

# Cell
from datetime import datetime
from collections import namedtuple
from typing import Union, Any, Optional, List, Tuple, Iterator, Mapping, Set, NamedTuple
from .utils import *
import numpy as np
from fastcore.foundation import GetAttr, L
path_type = Union[str, Any]
bin_val = Union[int, bytes]
bytes_encoded = Union[int, bytes]
datetime_object = datetime

# Cell
BASEBLOCK = ['thread_id', 'size', 'type', 'trailer', 'data']

# used in PROC: self._get_processing()
dict_processing: Mapping[int, str] = {0: 'single measurement', 1: 'average', 2: 'peak', 3: 'minimum'}
# used in DTYPE: self._get_unit()
dict_unit: Mapping[int, str] = {0: '%', 1: 'dBm', 2: 'dBuV/m'}

def create_base_block(bin_block: bytes)->Tuple:
    """
    Um bloco é um pedaço do arquivo .bin com inicio e final conhecidos e que contém diferentes tipos de informação.
    Possui varios campos: tipo, cabeçalho, dados e rodape.
    Cada campo possui comprimentos e informações definidas na documentação.
    Recebe um bloco do arquivo bin e retorna uma instância de Base Block com os atributos
    'thread_id', 'block_size', 'block_type', 'block_trailer', 'block_data'
    """
    if not isinstance(bin_block, bytes):
        raise TypeError(f"Expected type 'bytes', got '{type(bin_block)}' instead.")
    BaseBlock = namedtuple('BaseBlock', ' '.join(BASEBLOCK))
    return BaseBlock(*L(bin_block[:4], bin_block[4:8], bin_block[8:12]).map(bin2dec), bin_block[-4:], bin_block[12:])

# Cell
class TimedBlock(GetAttr):
    """
    Aplicável aos tipos de bloco:
        - DataType65
        - DataType63

    Implementa o mapeamento de funções dos blocos que possuem os seguintes campos
    (na mesma posição do vetor binario):F0 a F8

    F0 = (4 bytes) WALLDATE = Wall Clock Start Date of measurements
    F1 = (4 bytes) WALLTIME = Wall Clock Start Time
    F2 = (4u bytes) WALLNANO = Wall Clock Start Time Nanoseconds
    F3 = (2u bytes) STARTMEGA = Start Frequency MHz
    F4 = (4 bytes) STARTMILLI = Start Frequency mHz
    F5 = (2u bytes) STOPMEGA = Stop Frequency MHz
    F6 = (4 bytes) STOPMILLI = Stop Frequency mHz
    F7 = (2u bytes) STARTCHAN = Start Channel number
    F8 = (2u bytes) STOPCHAN = Stop Channel number

    Outros campos em posições diferentes do vetor binario devem possuir métodos na classe herdada:
    NAMAL, ANTUID, PROC, DTYPE, GERROR, GFLAGS, GROUPID, NPAD e NDATA

    """
    #The attributes which don't belong to this class are delegated to default: i.e Block
    def __init__(self, block: NamedTuple):
        self.default = block

    @property
    def date(self): return bin2date(self.data[:4]) #F0
    @property
    def time(self): return bin2time(self.data[4:8]) #F1
    @property
    def nano(self): return bin2dec(self.data[8:12], False) #F2
    @property
    def banda_mega(self): return bin2dec(self.data[12:14], False), bin2dec(self.data[18:20], False) #F3 e F5
    @property
    def banda_mili(self): return bin2dec(self.data[14:18]), bin2dec(self.data[20:24]) #F4 e F6
    @property
    def channel(self): return bin2dec(self.data[24:26], False), bin2dec(self.data[26:28], False) #F7 e F8
    @property
    def datetime_stamp(self):
        return  datetime(2000+self.date[2], self.date[1], self.date[0],
                            self.time[0], self.time[1], self.time[2], int(self.nano/1000))

# Cell
class DType21(GetAttr):
    """
    Data Type 21 – Unit and Job Information
    Tipo de bloco existente a partir da versão 3 do script LOGGER.
    F0 = (16 bytes) HOSTNAME = Unit Hostname.
                               Null terminated string (up to length 15), padded with nulls.
    F1 = (4 bytes) TEXT1LEN = Free Text length.
                              Including null termination and padding (must be a whole number of 4 bytes).
    F2 = (TEXT1LEN) TEXT1 = Null terminated Free Text – unit_info.
                            From ‘unit_info’ in cfg file Padded with \0 bytes,
                            E.g. could include
                                ‘method=blah;
                                other_key=blerg’ etc
                            keyword lookup in later analysis.
    F3 = (4 bytes) TEXT2LEN = Free Text length.
                              Including null termination and padding (must be a whole number of 4 bytes).
    F4 = (TEXT4LEN) TEXT4 = Null terminated Free Text – method.
                            From ‘method’ in cfg file.
    """
    #The attributes which don't belong to this class are delegated to default: i.e Block
    def __init__(self, block: NamedTuple):
        self.default = block

    def _get_text1_len(self) -> int:
        """
        Retorna o tamanho do campo TEXT1 que contém o ‘unit_info’ no arquivo cfg.
        :return:
        """
        return bin2dec(self.data[16:20])

    def _get_text2_len(self) -> int:
        """
        Retorna o tamanho do campo TEXT2 que contém o ‘unit_info’ no arquivo cfg.
        :return:
        """
        inicio = 20 + self._get_text1_len()
        final = 4 + inicio
        return bin2dec(self.data[inicio:final])

    @property
    def hostname(self) -> str:
        """
        Retorna o campo HOSTNAME que contém o "Unit Hostname".
        :return:
        """
        return bin2str(self.data[:16])

    @property
    def unit_info(self) -> str:
        """
        Retorna o campo TEXT1 que contém o ‘unit_info’ no arquivo cfg.
        :return:
        """
        fim = 20 + self._get_text1_len()
        return bin2str(self.data[16:fim])

    @property
    def method(self) -> str:
        """
        Retorna o campo TEXT2 que contém o ‘method’ no arquivo cfg.
        :return:
        """
        inicio = 24 + self._get_text1_len()
        fim = inicio + self._get_text2_len()
        return bin2str(self.data[inicio:fim])

# Cell
class DType40(GetAttr):
    """
    O Bloco do tipo 40 carrega dados de GPS.

    Data Type40 - GPS Data
    """

    def __init__(self, block: NamedTuple):
        """This implementation substitues inheritance of the class Block by Composition
        The attributes which belong to Block are accessed normally as if it was Inherited
        """
        self.default = block


    @property
    def date(self) -> Tuple[int, int, int, int]:
        """
        self > int, int, int, int
        :return: dia, mês, ano, reserva

        F0 = (4 bytes) WALLDATE = Wall Clock Start Date of measurements
        """
        return bin2date(self.data[:4])

    @property
    def time(self) -> Tuple[int, int, int, int]:
        """
        self > int, int, int, int
        :return: horas, minutos, segundos, décimos de segundo

        F1 = (4 bytes) WALLTIME = Wall Clock Start Time
        """
        return bin2time(self.data[4:8])

    @property
    def nanosecs(self) -> int:
        """
        self > int
        :return: nanosegundos

        F2 = (4u bytes) WALLNANO = Wall Clock Start Time Nanoseconds
        """
        return bin2dec(self.data[8:12], False)

    @property
    def wallclock_date_time_stamp(self) -> Tuple[Tuple[int, int, int, int], Tuple[int, int, int, int], int]:
        """
        self > int, int, int, int, int, int, int, int
        :return: dia, mês, ano, reserva, horas, minutos, segundos, décimos de segundo
        """
        return self.date, self.time, self.nanosecs

    @property
    def gps_date(self) -> Tuple[int, int, int, int]:
        """
        self > int, int, int, int
        :return: dia, mês, ano, reserva

        F3 = (4 bytes) WALLDATE = Wall Clock Start Date of measurements
        """
        return bin2date(self.data[12:16])

    @property
    def gps_time(self) -> Tuple[int, int, int, int]:
        """
        self > int, int, int, int
        :return: horas, minutos, segundos, décimos de segundo

        F4 = (4 bytes) WALLTIME = Wall Clock Start Time
        """
        return bin2time(self.data[16:20])

    @property
    def gps_date_time_stamp(self)-> Tuple[Tuple[int, int, int, int], Tuple[int, int, int, int], int]:
        """
        self > int, int, int, int, int, int, int, int
        :return: dia, mês, ano, reserva, horas, minutos, segundos, décimos de segundo
        """
        return self.gps_date, self.gps_time

    @property
    def gps_status(self) -> Union[str, int]:
        """
        self > int
        :return: "status" do GPS conforme documentação.

        F5 = (1 byte) Posicional Fix and Status.

        if status = 1:
            0 = No Fix
            1 = Standard GPS
            2 = Differencial GPS.
        if status = 0:
            Set to zero.
        """
        status_dict = {0:'No Fix', 1:'Standard GPS', 2:'Differential GPS'}
        status = bin2dec(self.data[20:21])
        return status_dict.get(status, status)

    @property
    def num_sattelites(self) -> int:
        """
        self > int
        :return: Número de satélites em visada.

        F6 = (1 byte) Sattelites in view

        0 = bad, 1+ better
        """
        return bin2dec(self.data[21:22])

    @property
    def heading(self) -> float:
        """
        self > float
        :return: Azimute de direção.

        F7 = (2 bytes) Heading = Degrees * 100
        """
        return bin2dec(self.data[22:24])/100

    @property
    def latitude(self) -> float:
        """
        self > float
        :return: Latitude em graus decimais. Valores positivos para emisferio Norte e negativos para Sul.

        F8 = (4 bytes) Latitude = Degrees * 1000000: +ve=N, -ve=S
        """
        return bin2dec(self.data[24:28]) / 1000000

    @property
    def longitude(self) -> float:
        """
        self > float
        :return: Longitude em graus decimais. Valores positivos para Leste e negativos para Oeste de greenwich.

        F9 = (4 bytes) Longitude = Degrees * 1000000: +ve=E, -ve=W
        """
        return bin2dec(self.data[28:32]) / 1000000

    @property
    def speed(self) -> float:
        """
        self > float
        :return: Velocidade em quilometros por hora.

        F10 = (4 bytes) Speed = kph * 1000
        """
        return bin2dec(self.data[32:36]) / 1000

    @property
    def altitude(self) -> float:
        """
        :return: Altidude do nivel do mar em metros.

        self > float

        F11 = (4 bytes) Altitude = Metres * 1000
        """
        return bin2dec(self.data[36:40]) / 1000

# Cell
class DataType63(GetAttr):
    """
    O Bloco do tipo 63 carrega dados de Nível por Canal de Frequência.

    Data Type 63 – Spectral Data

    F0 a F8, F10 a F13, F15 a F17 e F20 a F21 já inicializados na classe TimedBlock.

   *F0 = (4 bytes) WALLDATE = Wall Clock Start Date of measurements
   *F1 = (4 bytes) WALLTIME = Wall Clock Start Time
   *F2 = (4u bytes) WALLNANO = Wall Clock Start Time Nanoseconds
   *F3 = (2u bytes) STARTMEGA = Start Frequency MHz
   *F4 = (4 bytes) STARTMILLI = Start Frequency mHz
   *F5 = (2u bytes) STOPMEGA = Stop Frequency MHz
   *F6 = (4 bytes) STOPMILLI = Stop Frequency mHz
   *F7 = (2u bytes) STARTCHAN = Start Channel number
   *F8 = (2u bytes) STOPCHAN = Stop Channel number
    F9 = (4 bytes) SAMPLE = Duration of sampling.
                    Time taken by the FPGA and Radio to execute command in µs
    F10 =(4 bytes) NAMAL = Amalgamated  Results
    F11 = (1u byte) ANTUID Antenna number [ 0- 255]
    F12 = (1 byte) PROC = Processing
                    0 = single measurement,
                    1 = average,
                    2 = peak,
                    3 = minimum
    F13 = (1 byte) DTYPE = Data Type
                    1 = dBm,
                    2 = dBuV/m
    F14 = (1 byte) OFFSET = Data level offset in DTYPE units
                    2’s Complement, range [-128, 127].
    F15 = (1 byte)
    F16 = (1 byte)
    F17 = (1 byte)
    F18 = (2 bytes)
    F19 = (2 bytes)
    F20 = (1 byte)
    F21 = (4 bytes)
    F22 = (4*NTUN bytes)
    F23 = (NAGC bytes)
    F24 = (NDATA bytes)
    F25 = (NPAD bytes)
    """

    def __init__(self, timed_block: TimedBlock)-> None:
        self.default = timed_block

    @property
    def spent_time_microsecs(self) -> int:
        """
        self > int
        :return: O tempo levado pelo radio e FPGA para a aquisição da amostra, em microsegundos.

        F9 = (4 bytes) SAMPLE = Duration of sampling.
                    Time taken by the FPGA and Radio to execute command in µs
        """
        return bin2dec(self.data[28:32])

    @property
    def num_meas(self) -> int:
        """
        self > int
        :return: O número de resultados agrupados. Se for 1 equivale a uma única medida.

        Overrides method in TimedBlock.

        F10 = (4 bytes) NAMAL = Amalgamated Results
                    i.e. ‘number of loops’. Equal to 1 if single measurement.
        """
        return bin2dec(self.data[32:36])

    @property
    def id_antenna(self) -> int:
        """
        self > int
        :return: o ID da antena usada na medida.

        Overrides method in TimedBlock.

        F11 = (1u bytes) ANTUID Antenna number [ 0- 255]
        """
        return bin2dec(self.data[32:33], False)

    @property
    def processing(self) -> Union[str, int]:
        """
        self > (int, str)
        :return: O código e a descrição do tipo de processamento aplicado à medida.

        Overrides method in TimedBlock.

        F12 = (1 byte) PROC = Processing
                    0 = single measurement,
                    1 = average,
                    2 = peak,
                    3 = minimum
        """
        proc = bin2dec(self.data[37:38])
        return dict_processing.get(proc, proc)

    @property
    def unit(self) -> Union[str, int]:
        """
        self > str or int
        :return: A unidade de medida.
                Retorna um número inteiro se a unidade não foi documentada.

        Overrides method in TimedBlock.

        todo: Não está funcionando, todos os dados retornam o valor 0!

        F13 = DTYPE = Data Type
            0 = % (não documentado)
            1 = dBm
            2 = dBuV/m
        """
        unit: int = bin2dec(self.data[38:39])
        return dict_unit.get(unit, unit)

    @property
    def level_offset(self) -> int:
        """
        self > int
        :return: O deslocamento em nível adotado na compactação dos dados binários.
                 A unidade é dada por self._get_unit().

        F14 = (1 bytes) OFFSET = Data level offset in DTYPE units
                                2’s Complement, range [-128, 127].
        """
        return bin2dec(self.data[39:40])

    @property
    def global_error_code(self) -> int:
        """
        self > int
        :return: O código de erro global.

        Overrides method in TimedBlock.

        F15 = (1 byte) GERROR = Global Error Code.
                    Radio or processing global error code

        The radio error codes and flags can be provided on request.
        """
        return bin2dec(self.data[40:41])

    @property
    def global_flags_code(self) -> int:
        """
        self > int
        :return: Códigos de alertas globais ou de processamento do radio.

        Overrides method in TimedBlock.

        F16 = (1 byte) GFLAGS = Global clipping flags etc.
                    Radio or processing global flags.

        The radio error codes and flags can be provided on request.
        """
        return bin2dec(self.data[41:42])

    @property
    def group_id(self) -> int:
        """
        self > int
        :return: O ID do grupo à qual a medida pertence.
                 Caso 0 não pertence a nenhum grupo.
                 Use a classe 'DataType24' para detalhes do grupo.

        Overrides method in TimedBlock.

        F17 = (1 bytes) GROUPID = ID used to group sets of data
                    0 = not a member of a group
        """
        return bin2dec(self.data[42:43])

    @property
    def len_tunning_info(self) -> int:
        """
        self > int
        :return: 0 ou igual à quantidade de valores de AGC usados na amostra.

        F18 = (2 bytes) NTUN= Number of 4 byte Tuning info blocks. 0 or NAGC
        """
        return bin2dec(self.data[43:45])

    @property
    def len_agc(self) -> int:
        """
        self > int
        :return: 0 ou igual à quantidade de valores de "tunings" usados na amostra.

        F19 = (2 bytes) NAGC = Number of single byte AGC values
                                Can be 0, or = number of tunings in the sweep
        """
        return bin2dec(self.data[45:47])

    @property
    def len_padding(self) -> int:
        """
        self > int
        :return: Valor que varia de 0 a 3 indicando o preenchimento nulo para manter o tamanho do bloco (em bytes) fixo.

        Overrides method in TimedBlock.

        A extração do NPAD (quantidade) tem pouca utilidade prática.
        A extração do Padding (valor) não tem utilidade prática.

        F20 = (1 byte) NPAD = Number of bytes of padding. 0-3
        (NPAD bytes) Padding = As \0 bytes
        """
        return bin2dec(self.data[39:40])

    @property
    def data_points(self) -> int:
        """
        self > int
        :return: O número de canais (ou "steps") que dividem igualmente a largura de banda .

        Overrides method in TimedBlock.

        F21 = (4 bytes) NDATA = Number of single byte data points.
                        Number of equal width channels dividing the reported frequency width
        """
        return bin2dec(self.data[48:52])

    @property
    def rbw(self) -> float:
        """
        Retorna o RBW calculado a partir de STARTMEGA, STOPMEGA e NDATA.
        :return: RBW (Hz)
        """
        return int(((self.banda_mega[1] - self.banda_mega[0]) / (self.data_points - 1) * 1000000))

    @property
    def tunning_info_array(self) -> bytes:
        """
        self > bytes
        :return: Binario bruto de informações do 'tunning'.

        F22 = (4*NTUN bytes) = Array of Tuning info blocks
                        One block per tuning (1 or 10 MHz). See section 11.7.

        todo: implementar um método para traduzir o 'Tuning info block' de acordo com a seção 11.7 da documentação.
        """
        start = 52  # inicia aqui
        stop = start+(self.len_tunning_info*4)  # termina aqui
        return self.data[start:stop]

    @property
    def agc_array(self) -> bytes:
        """
        self > bytes
        :return: Binario bruto com toda a matriz de AGC.

        F23 = (NAGC  bytes) = Array of AGC values As dB in single unsigned byte.
                        Current actual values are 0..63.

        todo: implementar um método que forneça a matriz de números inteiros do AGC.
        """
        start = 52+(self.len_tunning_info * 4)  # inicia após F22
        stop = start+(self.len_agc)  # termina aqui
        return self.data[start:stop]

    @property
    def block_data(self) -> List[float]:
        """
        self > List[float]
        :return: A lista de todas as medidas de espectro do bloco em 'dB'.

        F24 = (NDATA  bytes) = Array of dB spectrum data points.
        Data points in a byte representing  the power in dBm in 0.5 dBm steps
        """
        start = 52+(self.len_tunning_info * 4) + self.len_agc  # inicia após F23
        stop = start+(self.data_points)  # termina aqui
        return np.fromiter(self.data[start:stop], dtype=np.float16) / 2 + self.level_offset - 127.5