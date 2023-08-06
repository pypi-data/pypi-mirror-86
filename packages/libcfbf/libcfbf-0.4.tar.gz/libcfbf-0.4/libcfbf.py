# This file is part of the libcfbf distribution (https://git.rcarz.net/bobc/libcfbf).
# Copyright (c) 2020 Bob Carroll (bob.carroll@alum.rit.edu)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import math
from itertools import chain, takewhile
from io import BytesIO, SEEK_CUR, SEEK_END


class CfbfDocument(object):
    """
    An implementation of Microsoft's Compound File Binary Format.

    :param file: an open file resource
    :param header: a CFBF header structure
    """

    LITTLE_ENDIAN = b'\xfe\xff'

    FREE_SEC_ID = -1
    END_OF_CHAIN_ID = -2
    SAT_SEC_ID = -3
    MSAT_SEC_ID = -4

    def __init__(self, file, header):
        self.header = header
        self._file = file
        self._sector_size = int(math.pow(2, header.sector_size))
        self._sector_at = None
        self._file_size = None
        self._root_dir = None

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def sector_size(self):
        """
        :returns: the width of a sector in bytes
        """
        return self._sector_size

    @property
    def file_size(self):
        """
        :returns: the byte size of the file
        """
        if self._file_size is None:
            self._file.seek(0, SEEK_END)
            self._file_size = self._file.tell()

        return self._file_size

    @property
    def sector_alloc_table(self):
        """
        :returns: the Sector Allocation Table
        """
        if not self._sector_at:
            self._sector_at = list(self.build_sector_alloc_table())

        return self._sector_at

    @property
    def root_entry(self):
        """
        :returns: the root directory entry
        """
        if self._root_dir is None:
            self._root_dir = DirectoryEntry.open(self)

        return self._root_dir

    @classmethod
    def open(cls, path):
        """
        Opens a CFBF file for reading.

        :param path: document file path
        :returns: a document object
        """
        file = open(path, 'rb')

        try:
            header = CfbfHeader.read(file)
            if header.byte_order != cls.LITTLE_ENDIAN:
                raise CfbfError('Only little-endian encoding is supported')

            document = cls(file, header)
        except:     # noqa: E722
            file.close()
            raise
        else:
            return document

    def close(self):
        """
        Closes the file stream.
        """
        if self._file:
            self._file.flush()
            self._file.close()
            self._file = None

    def compute_sector_offset(self, sec_id):
        """
        Compute a sector's byte offset in the file.

        :param sec_id: sector ID
        :returns: a byte offset
        """
        return self.header.size + (sec_id * self.sector_size)

    def read_sector(self, sec_id):
        """
        Reads sector data from the file.

        :param sec_id: sector ID
        :returns: sector data
        """
        if sec_id < 0:
            raise CfbfError('Bad sector ID')

        offset = self.compute_sector_offset(sec_id)
        if offset >= self.file_size:
            raise CfbfError('End of file')

        self._file.seek(offset)
        return self._file.read(self.sector_size)

    def partition_sectors(self, data):
        """
        Splits the buffer into sector IDs.

        :param data: buffer to read
        :returns: a list of sector IDs
        """
        n = self.header.SEC_ID_SIZE
        if len(data) % n != 0:
            raise CfbfError('Buffer length is not divisible by sector ID size')

        return [btoi(data[i:i + n]) for i in range(0, len(data), n)]

    def walk_msat_sectors(self, sec_id, results, chain=None):
        """
        Reads the extended MSAT from sectors.

        :param sec_id: the sector ID to read
        :param results: running list of results
        :param chain: running set of sector IDs visited
        :returns: a set of MSAT sector IDs
        """
        if chain is None:
            chain = set()

        sector = self.partition_sectors(self.read_sector(sec_id))
        results.extend(takewhile(lambda x: x != self.FREE_SEC_ID, sector[:-1]))

        if sector[-1] == self.END_OF_CHAIN_ID:
            return chain | {sec_id}
        elif sector[-1] in chain:
            raise CfbfError('Extended Master Sector Allocation Table is corrupted')

        return self.walk_msat_sectors(sector[-1], results, chain | {sec_id})

    def read_msat_sectors(self):
        """
        Reads the Master Sector Allocation Table and generates a list of sectors.

        :return: a tuple of a list of SAT sector IDs and a list of MSAT sector IDs
        """
        self._file.seek(self.header.master_sat_offset)
        data = self._file.read(self.header.MSAT_SIZE)
        sat_ids = self.partition_sectors(data)[:self.header.sat_sectors]

        if self.header.master_sat_first != self.END_OF_CHAIN_ID:
            msat_ids = self.walk_msat_sectors(self.header.master_sat_first, sat_ids)
        else:
            msat_ids = []

        return (sat_ids, msat_ids)

    def check_msat_integrity(self, msat, ids):
        """
        Perform integrity checking on the Master Sector Allocation Table.

        :param msat: the MSAT
        :param ids: set of sector IDs for the extended table
        :returns: True if clean, False otherwise
        """
        if msat[0] < 0:
            return False
        elif len(ids) != self.header.master_sat_count:
            return False

        visited = set()
        for sec_id in takewhile(lambda x: x != self.FREE_SEC_ID, msat):
            if sec_id * self.sector_size + self.header.size >= self.file_size:
                return False
            elif sec_id in visited:
                return False
            else:
                visited.add(sec_id)

        return True

    def build_sector_alloc_table(self):
        """
        Builds the Sector Allocation Table as an array of sector ID chains.

        :returns: the SAT
        """
        def raise_():
            raise CfbfError('Master Sector Allocation Table is corrupted')

        def check(x):
            if x[0] in msat and x[1] != self.SAT_SEC_ID:
                raise_()
            if x[0] in msat_ids and x[1] != self.MSAT_SEC_ID:
                raise_()
            else:
                return x[1]

        msat, msat_ids = self.read_msat_sectors()
        if not self.check_msat_integrity(msat, msat_ids):
            raise_()

        return map(check, enumerate(
            chain(*(self.partition_sectors(self.read_sector(x)) for x in msat))))

    def walk_sector_chain(self, start):
        """
        Generator for discovering sector IDs from the Sector Allocation Table.

        :param start: entry point in the SAT where the chain begins
        :returns: an iterator that yields sector IDs
        """
        index = start
        visited = set()

        def raise_():
            raise CfbfError('Sector Allocation Table is corrupted')

        while index != self.END_OF_CHAIN_ID:
            if index < 0 or index in visited:
                raise raise_()

            yield index
            visited.add(index)

            try:
                index = self.sector_alloc_table[index]
            except IndexError:
                raise_()

    def concat_sectors(self, start):
        """
        Creates a concatenated byte string of sectors.

        :param start: the starting sector ID
        :returns: a byte string
        """
        buf = b''

        for x in self.walk_sector_chain(start):
            buf += self.read_sector(x)

        return buf


class CfbfHeader(object):
    """
    Compound Document Format header structure.
    """

    CFBF_MAGIC_NUMBER = b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'

    SEC_ID_SIZE = 4
    MSAT_SIZE = 436

    def __init__(self, file):
        self.uid = file.read(16)
        self.revision = btoi(file.read(2))
        self.version = btoi(file.read(2))
        self.byte_order = file.read(2)
        self.sector_size = btoi(file.read(2))
        self.short_sector_size = btoi(file.read(2))
        file.seek(10, SEEK_CUR)
        self.sat_sectors = btoi(file.read(4))
        self.directory_sector = btoi(file.read(4))
        file.seek(4, SEEK_CUR)
        self.min_stream_size = btoi(file.read(4))
        self.short_sat_first = btoi(file.read(4))
        self.short_sat_count = btoi(file.read(4))
        self.master_sat_first = btoi(file.read(4))
        self.master_sat_count = btoi(file.read(4))
        self._master_sat_offset = file.tell()
        self.master_sat = file.read(self.MSAT_SIZE)
        self._header_size = file.tell()

    @property
    def master_sat_offset(self):
        """
        :returns: the offset of the start of the MSAT
        """
        return self._master_sat_offset

    @property
    def size(self):
        """
        :returns: the width of the header in bytes
        """
        return self._header_size

    @classmethod
    def read(cls, file):
        """
        Reads the CFBF file header into a structure.

        :param file: an open file resource
        :returns: a CFBF header structure
        """
        file.seek(0)

        if file.read(8) != cls.CFBF_MAGIC_NUMBER:
            raise CfbfError('Bad magic number')

        return cls(file)


class CfbfError(Exception):
    """
    Catch-all exception for CFBF read errors.
    """
    pass


class DirectoryEntry(object):
    """
    Compound Document Format storage container.

    :param document: an open CFBF document
    :param stream: directory entry byte stream
    """

    DIR_ENTRY_SIZE = 128
    DIR_ENTRY_NULL = -1

    TYPE_EMPTY = 0x0
    TYPE_USER_STORAGE = 0x1
    TYPE_USER_STREAM = 0x2
    TYPE_LOCK_BYTES = 0x3
    TYPE_PROPERTY = 0x4
    TYPE_ROOT_STORAGE = 0x5

    def __init__(self, document, stream):
        self._document = document
        self._stream = stream
        self._children = None
        name = stream.read(64)
        self.entry_name_sz = btoi(stream.read(2))
        self.entry_type = btoi(stream.read(1))
        self.node_color = btoi(stream.read(1))
        self.node_left = btoi(stream.read(4))
        self.node_right = btoi(stream.read(4))
        self.node_root = btoi(stream.read(4))
        self.uid = stream.read(16)
        self.user_flags = stream.read(4)
        self.created_at = stream.read(8)
        self.modified_at = stream.read(8)
        self.stream_sector = btoi(stream.read(4))
        self.stream_size = btoi(stream.read(4))
        stream.seek(4, SEEK_CUR)

        self.entry_name = str(name[:self.entry_name_sz - 2], 'utf-16-le')

    def __getitem__(self, key):
        """
        Looks up children by name. Key can be a path separated by /.

        :param key: child entry name to find
        :returns: the entry or None
        """
        ent = next((x for x in self.children if x.entry_name == key), None)
        if ent is None:
            raise KeyError(key)

        return ent

    @property
    def storage_type(self):
        """
        :returns: True if this entry is a storage type, False otherwise
        """
        return self.entry_type in [self.TYPE_USER_STORAGE, self.TYPE_ROOT_STORAGE]

    @property
    def stream_type(self):
        """
        :returns: True if this entry is a user stream, False otherwise
        """
        return self.entry_type == self.TYPE_USER_STREAM

    @property
    def children(self):
        """
        :returns: a list of all direct child entries
        """
        if self._children is None:
            self._children = self.find_children()

        return self._children

    def compute_offset(self, id_):
        """
        Computes the byte offset of the given directory entry.

        :param id_: directory entry ID
        :return: stream offset where entry begins
        """
        return id_ * self.DIR_ENTRY_SIZE

    @classmethod
    def open(cls, document):
        """
        Opens the root directory.

        :param document: a CFBF document
        :returns: the root directory entry
        """
        sec_id = document.header.directory_sector
        if sec_id < 0 and sec_id >= len(document.sector_alloc_table):
            raise CfbfError('Bad directory sector')

        buf = document.concat_sectors(sec_id)
        return cls(document, BytesIO(buf))

    def stream(self):
        """
        Opens a stream for reading.

        :returns: a byte stream object
        """
        if not self.stream_type:
            raise CfbfError('Entry is not a stream')
        elif self.stream_size < self._document.header.min_stream_size:
            raise CfbfError('Short streams are not implemented')

        buf = self._document.concat_sectors(self.stream_sector)
        return BytesIO(buf)

    def _descend(self, id_, results):
        """
        Recursively descends into the given node and finds siblings.

        :param id_: directory entry ID to descend to
        :param results: resulting entries collected during descent
        """
        self._stream.seek(self.compute_offset(id_))
        ent = DirectoryEntry(self._document, self._stream)
        results.append(ent)
        results.extend(ent.find_siblings())

    def find_children(self):
        """
        Finds all direct child entries of this entry.

        :returns: a list of child entries.
        """
        results = []

        if self.storage_type and self.node_root != self.DIR_ENTRY_NULL:
            self._descend(self.node_root, results)

        return results

    def find_siblings(self):
        """
        Walks the red-black tree looking for nodes that are sibling entries.

        :returns: a list of sibling entries
        """
        results = []

        if self.node_left != self.DIR_ENTRY_NULL:
            self._descend(self.node_left, results)

        if self.node_right != self.DIR_ENTRY_NULL:
            self._descend(self.node_right, results)

        return results


def btoi(bstr, signed=True):
    """
    Converts a little-endian byte string to an integer.

    :param buf: a byte string
    :param signed: optional flag for sign-magnitude
    :returns: an integer
    """
    return int.from_bytes(bstr, byteorder='little', signed=signed)
