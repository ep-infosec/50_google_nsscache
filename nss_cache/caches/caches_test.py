# Copyright 2007 Google Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""Unit tests for caches/caches.py."""

__author__ = 'jaq@google.com (Jamie Wilkinson)'

import os
import platform
import stat
import tempfile
import unittest
from unittest import mock

from nss_cache import config
from nss_cache.caches import caches


class FakeCacheCls(caches.Cache):

    CACHE_FILENAME = 'shadow'

    def __init__(self, config, map_name):
        super(FakeCacheCls, self).__init__(config, map_name)

    def Write(self, map_data):
        return 0

    def GetCacheFilename(self):
        return os.path.join(self.output_dir, self.CACHE_FILENAME + '.test')


class TestCls(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.config = {'dir': self.workdir}
        if platform.system() == 'FreeBSD':
            # FreeBSD doesn't have a shadow file
            self.shadow = config.MAP_PASSWORD
        else:
            self.shadow = config.MAP_SHADOW

    def tearDown(self):
        os.rmdir(self.workdir)

    def testCopyOwnerMissing(self):
        expected = os.stat(os.path.join('/etc', self.shadow))
        expected = stat.S_IMODE(expected.st_mode)
        cache = FakeCacheCls(config=self.config, map_name=self.shadow)
        cache._Begin()
        cache._Commit()
        data = os.stat(os.path.join(self.workdir, cache.GetCacheFilename()))
        self.assertEqual(expected, stat.S_IMODE(data.st_mode))
        os.unlink(cache.GetCacheFilename())

    def testCopyOwnerPresent(self):
        expected = os.stat(os.path.join('/etc/', self.shadow))
        expected = stat.S_IMODE(expected.st_mode)
        cache = FakeCacheCls(config=self.config, map_name=self.shadow)
        cache._Begin()
        cache._Commit()
        data = os.stat(os.path.join(self.workdir, cache.GetCacheFilename()))
        self.assertEqual(expected, stat.S_IMODE(data.st_mode))
        os.unlink(cache.GetCacheFilename())


class TestCache(unittest.TestCase):

    def testWriteMap(self):
        cache_map = caches.Cache({}, config.MAP_PASSWORD, None)
        with mock.patch.object(cache_map, 'Write') as write, mock.patch.object(
                cache_map,
                'Verify') as verify, mock.patch.object(cache_map,
                                                       '_Commit') as commit:
            write.return_value = 'entries_written'
            verify.return_value = True
            self.assertEqual(0, cache_map.WriteMap('writable_map'))


if __name__ == '__main__':
    unittest.main()
