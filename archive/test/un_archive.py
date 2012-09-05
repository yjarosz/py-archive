import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest
from .. import Archive

in_path = 'samples'
in_archive = ('Archive.tgz', 'Archive.zip', 'sample.txt.gz')
out_path = 'out'
remove_file = True


class TestUnArchiving(unittest.TestCase):

    def setUp(self):
        print '[x] Starting un-archiving tests'


    def tearDown(self):
        print '[x] End un-archiving tests'
        if remove_file:
            print '[x] Remove test-files results'
            for f in os.listdir(out_path):
                os.remove(os.path.join(out_path, f))

    def runTest(self):
        for f in in_archive:
            print '[x] Testing file : %s' % f
            Archive(os.path.join(in_path, f)).extract(out=out_path)
