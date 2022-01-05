import unittest
import sys
import os

import config

sys.path.append("..")


class TestTasks(unittest.TestCase):

      
    def test_content_path_is_a_valid_directory(self):
        '''Check we can access and list the files contained in constant
        CONTENT_PATH.
        '''
        
        path_to_content_dir = config.CONTENT_PATH
        # check content path is a directory
        self.assertTrue(os.path.isdir(path_to_content_dir))
        # check content path is not empty
        self.assertGreater(len(os.listdir(path_to_content_dir)), 0)
        # Check we have write permission to directory
        self.assertTrue(os.access(path_to_content_dir, os.W_OK))


if __name__ == '__main__':
    unittest.main()
