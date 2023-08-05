from .config import Settings
import os
import lz4.frame
from Crypto.Cipher import AES
import rsa
from datetime import datetime

# typedef struct _BUFFER_HEADER
# {
#    CHAR Magic[6];         --> 8 BITS --> 1 byte * 6
#    CHAR BufferVersion;    --> 8 BITS --> 1 byte
#    CHAR Flags;            --> 8 BITS --> 1 byte
#    DWORD dwExtraDataLen;  --> 32 bits = 4 bytes
#    BYTE bExtraData[0];    --> 8 BITS --> 1 byte
# } BUFFER_HEADER, *PBUFFER_HEADER;
class OradadFileHeaderException(Exception):
    pass

class OradadFileDataException(Exception):
    pass

class OradadFileException(Exception):
    pass

class OradadFileHeader(object):

    def __init__(self, parent):
        self.__parent = parent
        self.magic = None
        self.bufferVersion = None
        self.flags = None
        self.extraDataLen = None
        self.extraDataLen_int = None
        self.extraData = None

    def process(self)->bool:
        self.magic = self.file.read(Settings.HEADER_MAGIC_SIZE * Settings.CHAR_BYTE_SIZE)
        self.bufferVersion = self.file.read(Settings.CHAR_BYTE_SIZE)
        self.flags = self.file.read(Settings.CHAR_BYTE_SIZE)
        self.extraDataLen = self.file.read(Settings.DWORD_BYTE_SIZE)
        self.extraDataLen_int = int.from_bytes(
            self.extraDataLen,
            byteorder=Settings.BYTE_ORDER_LITTLE,
            signed=False)
        if self.extraDataLen_int > 0:
            self.extraData = self.file.read(self.extraDataLen_int)
        
    @property
    def file(self):
        return self.__parent.file

    @property
    def size(self)-> int:
        return len(self.magic) + len(self.bufferVersion) +\
                len(self.flags) + len(self.extraDataLen) +\
                self.extraDataLen_int

    def __print_flags(self)-> None:
        print('compressed: {0}'.format(self.__parent.compressed))
        print('encrypted: {0}'.format(self.__parent.encrypted))

    def __print_extradata(self)-> None:
        print('extraDataLen (bytes): {0}'.format(self.extraDataLen))
        print('extraDataLen (int): {0}'.format(self.extraDataLen_int))
        if self.extraDataLen_int > 0 and self.__parent.verbose >= Settings.LOG_LEVEL_DEBUG:
            print('extraData:\n\t{0}'.format(self.extraData))

    def print(self)-> None:
        print('headerSize: {0}'.format(self.size))
        print('magic: {0}'.format(self.magic))
        print('bufferVersion: {0}'.format(self.bufferVersion))
        self.__print_flags()
        print('')
        self.__print_extradata()

class OradadFileData(object):
    
    def __init__(self, parent):
        self.__parent = parent
        iv = b'\0' * 16 # empty iv
        if self.__parent.encrypted:
            self.__cipher = AES.new(self.__parent.aes_key, AES.MODE_CBC, iv)

    def _decrypt(self, c_data):
        return self.__cipher.decrypt(c_data)

    def process(self)-> bool:
        if not self.__parent.write_file :
            self.__data = b''
        else:
            output_f = open(self.__parent.filepath[:-7], 'wb') # len(".oradad") is 7
            block_read = 0
        if self.__parent.compressed:
            d_context = lz4.frame.create_decompression_context()
        while True:
            block = self.file.read(Settings.BUFFER_SIZE)
            block_read += 1
            if self.__parent.verbose >= Settings.LOG_LEVEL_DEBUG:
                print("processing block {0}: ".format(block_read))
                print("\tlength: {0}".format(len(block)))
            if not block:
                break
            if self.__parent.encrypted:
                block = self._decrypt(block)
            if self.__parent.compressed:
               block, b, e = lz4.frame.decompress_chunk(d_context, block)
            if not self.__parent.write_file :
                self.__data += block
            else:
                output_f.write(block)

    def print(self, encoding=Settings.ISO_8859_1_LATIN_1):
        if self.__data:
            print(self.__data.decode(encoding))

    @property
    def file(self):
        return self.__parent.file

class OradadFile(object):
    """
    OradadFile class
    """

    def _run_pre_checks(self):
        if not os.path.isfile(self.filepath):
            raise OradadFileException("Oradad file not found:\n\t{0}\n".format(self.filepath))
        if not self.filepath[-7:] == ".oradad":
            raise OradadFileException("File {0} is not .oradad type".format(self.filepath))
        if self.__private_key_file is not None and not os.path.isfile(self.__private_key_file):
            raise OradadFileException("Private key file not found: {0}".format(self.__private_key_file))
        # TODO : validate all input from user

    def __init__(self, filepath, private_key_file=None, write_file=True, verbose=Settings.LOG_LEVEL_INFORMATIONS):
        self.__filepath = filepath
        self.__private_key_file = private_key_file
        self.__verbose = verbose
        self.__fileSize = None
        self.__header = None
        self.__data = None
        self.__private_key = None
        self.__aes_key = None
        self.__file = None
        self.__write_file = write_file
        self.__start_time = None
        self.__end_time = None
        self._run_pre_checks()

    def _get_aes_key(self)->bytes:
        if self.__private_key_file is None:
            raise Exception("Private key file not found")
        self.__private_key = rsa.PrivateKey.load_pkcs1(open(self.__private_key_file).read())
        # first 12 bytes are aes key informations (wincrypt.h)
        # can be parsed in future version to increase versatility
        reversed_extra_data = self.__header.extraData[12:][::-1]
        self.__aes_key = rsa.decrypt(reversed_extra_data, self.__private_key)

    def _init_headers(self)-> None:
        self.__header = OradadFileHeader(self)
        if self.__verbose >= Settings.LOG_LEVEL_WARNING:
            print("\treading headers")
        if self.__header.process() and  self.__verbose >= Settings.LOG_LEVEL_WARNING:
            print("\theaders read")
        if self.__verbose > Settings.LOG_LEVEL_WARNING:
            self.__header.print()

    def _init_data(self)-> None:
        self.__data = OradadFileData(self)
        if self.__verbose >= Settings.LOG_LEVEL_WARNING:
            print("\treading data")
        if self.__data.process() and  self.__verbose >= Settings.LOG_LEVEL_WARNING:
            print("\tdata read")
            self.__data.print()


    def process(self)-> None:
        self.__start_time = datetime.now()
        with open(self.__filepath, 'rb') as file:
            self.__file = file
            self._init_headers()
            if self.encrypted:
                self._get_aes_key()
            self._init_data()
        self.__end_time = datetime.now()

    @property
    def data(self)->OradadFileData:
        return self.__data

    @property
    def processed_time(self)->OradadFileData:
        if self.__start_time and self.__end_time:
            return (self.__end_time - self.__start_time)
    
    @property
    def header(self)->OradadFileHeader:
        return self.__header

    @property
    def file(self):
        return self.__file

    @property
    def filepath(self):
        return self.__filepath

    @property
    def write_file(self)->bool:
        return self.__write_file

    @property
    def aes_key(self):
        return self.__aes_key

    @property
    def verbose(self):
        return self.__verbose

    @property
    def size(self)-> int:
        if not self.__fileSize:
            self.__fileSize = os.path.getsize(self.__filepath)
        return self.__fileSize
    
    @property
    def compressed(self)-> bool:
	    return (self.__header.flags[0] & Settings.BUFFER_COMPRESSED_FLAG[0]) == Settings.BUFFER_COMPRESSED_FLAG[0]

    @property
    def encrypted(self)-> bool:
        return  (self.__header.flags[0] & Settings.BUFFER_ENCRYPTED_FLAG[0]) == Settings.BUFFER_ENCRYPTED_FLAG[0]

