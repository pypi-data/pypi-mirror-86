class Settings(object):
    """
    Settings
    """
    BUFFER_SIZE = 1024 * 1024
    HEADER_MAGIC = b'ORADAD'
    HEADER_MAGIC_SIZE = len(HEADER_MAGIC)
    #DECOMPRESS_BUFFER_SIZE = (1 << 20) # = 1MB, not used. (yet ?)
    #DECRYPT_BUFFER_SIZE = BUFFER_SIZE # not used. (yet ?)

    CHAR_BYTE_SIZE = 1
    DWORD_BYTE_SIZE = 4
    BYTE_BYTE_SIZE = 1

    BUFFER_COMPRESSED_FLAG = b'\x01'
    BUFFER_ENCRYPTED_FLAG = b'\x02'


    BYTE_ORDER_LITTLE = 'little' # little endian

    LOG_LEVEL_INFORMATIONS = 0
    LOG_LEVEL_WARNING = 1
    LOG_LEVEL_DEBUG = 2

    ISO_8859_1_LATIN_1 = 'iso-8859-1'

Settings = Settings()