from __future__ import absolute_import, division, print_function

from logging import getLogger
from os.path import isfile, join

from .core.link import UnlinkLinkTransaction
from .core.package_cache import ProgressiveFetchExtract
from .exceptions import CondaFileIOError
from .gateways.disk.link import islink

log = getLogger(__name__)

# op codes
CHECK_FETCH = 'CHECK_FETCH'
FETCH = 'FETCH'
CHECK_EXTRACT = 'CHECK_EXTRACT'
EXTRACT = 'EXTRACT'
RM_EXTRACTED = 'RM_EXTRACTED'
RM_FETCHED = 'RM_FETCHED'
PREFIX = 'PREFIX'
PRINT = 'PRINT'
PROGRESS = 'PROGRESS'
SYMLINK_CONDA = 'SYMLINK_CONDA'
UNLINK = 'UNLINK'
LINK = 'LINK'
UNLINKLINKTRANSACTION = 'UNLINKLINKTRANSACTION'
PROGRESSIVEFETCHEXTRACT = 'PROGRESSIVEFETCHEXTRACT'


PROGRESS_COMMANDS = set([EXTRACT, RM_EXTRACTED])
ACTION_CODES = (
    CHECK_FETCH,
    FETCH,
    CHECK_EXTRACT,
    EXTRACT,
    UNLINK,
    LINK,
    SYMLINK_CONDA,
    RM_EXTRACTED,
    RM_FETCHED,
)


def PREFIX_CMD(state, prefix):
    state['prefix'] = prefix


def PRINT_CMD(state, arg):
    if arg.startswith(('Unlinking packages', 'Linking packages')):
        return
    getLogger('conda.stdout.verbose').info(arg)


def FETCH_CMD(state, package_cache_entry):
    raise NotImplementedError()


def EXTRACT_CMD(state, arg):
    raise NotImplementedError()


def PROGRESSIVEFETCHEXTRACT_CMD(state, progressive_fetch_extract):
    assert isinstance(progressive_fetch_extract, ProgressiveFetchExtract)
    progressive_fetch_extract.execute()


def UNLINKLINKTRANSACTION_CMD(state, arg):
    unlink_link_transaction = arg
    assert isinstance(unlink_link_transaction, UnlinkLinkTransaction)
    unlink_link_transaction.execute()


def check_files_in_package(source_dir, files):
    for f in files:
        source_file = join(source_dir, f)
        if isfile(source_file) or islink(source_file):
            return True
        else:
            raise CondaFileIOError(source_file, "File %s does not exist in tarball" % f)


# Map instruction to command (a python function)
commands = {
    PREFIX: PREFIX_CMD,
    PRINT: PRINT_CMD,
    FETCH: FETCH_CMD,
    PROGRESS: lambda x, y: None,
    EXTRACT: EXTRACT_CMD,
    RM_EXTRACTED: lambda x, y: None,
    RM_FETCHED: lambda x, y: None,
    UNLINK: None,
    LINK: None,
    SYMLINK_CONDA: lambda x, y: None,
    UNLINKLINKTRANSACTION: UNLINKLINKTRANSACTION_CMD,
    PROGRESSIVEFETCHEXTRACT: PROGRESSIVEFETCHEXTRACT_CMD,
}


OP_ORDER = (RM_FETCHED,
            FETCH,
            RM_EXTRACTED,
            EXTRACT,
            UNLINK,
            LINK,
            )
