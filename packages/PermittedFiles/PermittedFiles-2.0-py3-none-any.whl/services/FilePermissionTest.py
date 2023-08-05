"""
FilePermissionTest.py

Programmer: Phiroj Kumar Dash
Course: CSC540

This unit test class will test permitted_file function of FilePermissionTest.py file
It tests the type of file can be uploaded and which cannot.
"""
import unittest
from services.FilePermission import permitted_file


class AllowedFilesForUpload(unittest.TestCase):
    def test_allowedFiles(self):
        """
                :param : No input parameter
                :return: True or False based on file type

        """
        fileName = 'upload.pdf'

        self.assertEqual(True, permitted_file(fileName))

    def test_not_allowedFiles(self):
        fileName = 'upload.doc'
        self.assertEqual(False, permitted_file
        (fileName))


if __name__ == '__main__':
    unittest.main( )
