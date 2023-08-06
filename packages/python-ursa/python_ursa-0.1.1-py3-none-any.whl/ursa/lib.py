import logging
import sys
from ctypes import CDLL, CFUNCTYPE, c_void_p, c_int,\
    c_char_p, c_char_p, c_char_p, c_char_p, c_int

from .indy_error import ErrorCode, IndyCryptoError

from logging import ERROR, WARNING, INFO, DEBUG

TRACE = 5


def do_call(name, *args):
    logger = logging.getLogger(__name__)
    logger.debug("do_call: >>> name: %r, args: %r", name, args)

    err = getattr(_cdll(), name)(*args)

    logger.debug("do_call: Function %r returned err: %r", name, err)

    if err != ErrorCode.Success:
        raise IndyCryptoError(ErrorCode(err))


def _cdll():
    if not hasattr(_cdll, "cdll"):
        _cdll.cdll = _load_cdll()
        _set_logger()

    return _cdll.cdll


def _load_cdll():
    logger = logging.getLogger(__name__)
    logger.debug("_load_cdll: >>>")

    lib_prefix_mapping = {"darwin": "lib", "linux": "lib", "linux2": "lib", "win32": ""}
    lib_suffix_mapping = {"darwin": ".dylib", "linux": ".so", "linux2": ".so", "win32": ".dll"}

    os_name = sys.platform
    logger.debug("_load_cdll: Detected OS name: %s", os_name)

    try:
        ursa_prefix = lib_prefix_mapping[os_name]
        ursa_suffix = lib_suffix_mapping[os_name]
    except KeyError:
        logger.error("_load_cdll: OS isn't supported: %s", os_name)
        raise OSError("OS isn't supported: %s", os_name)

    lib_name = "libursa{0}".format(ursa_suffix)
    logger.debug("_load_cdll: Resolved URSA name is: %s", lib_name)

    try:
        res = CDLL(lib_name)

        logger.debug("_load_cdll: Init Ursa logger")

        logger.debug("_load_cdll: <<< res: %s", res)
        return res
    except OSError as e:
        logger.error("_load_cdll: Can't load libursa: %s", e)
        raise e


def _set_logger():
    logger = logging.getLogger(__name__)
    logging.addLevelName(TRACE, "TRACE")

    logger.debug("set_logger: >>>")

    def _log(context, level, target, message, module_path, file, line):
        ursa_logger = logger.getChild('native.' + target.decode().replace('::', '.'))

        level_mapping = {1: ERROR, 2: WARNING, 3: INFO, 4: DEBUG, 5: TRACE, }

        ursa_logger.log(level_mapping[level],
                           "\t%s:%d | %s",
                           file.decode(),
                           line,
                           message.decode())

    _set_logger.callbacks = {
        'enabled_cb': None,
        'log_cb': CFUNCTYPE(None, c_void_p, c_int, c_char_p, c_char_p, c_char_p, c_char_p, c_int)(_log),
        'flush_cb': None
    }

    do_call('ursa_set_logger',
            None,
            _set_logger.callbacks['enabled_cb'],
            _set_logger.callbacks['log_cb'],
            _set_logger.callbacks['flush_cb'])

    logger.debug("set_logger: <<<")