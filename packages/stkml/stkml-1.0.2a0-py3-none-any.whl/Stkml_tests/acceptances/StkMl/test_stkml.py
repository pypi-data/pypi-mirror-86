import io
import os
import unittest

import yaml

from Stkml.Stkml import Stkml, StkmlSyntaxicErrorList
from Stkml_tests.acceptances.Fixtures import clone_fixture


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_get_library_should_return_library_file_when_library_is_in_working_directory(self):
        # Assign
        with clone_fixture('local_package') as working_directory:
            stkml = Stkml(folder=working_directory)
            local_package = 'Lyra'

            # Acts
            package = stkml.get_library(local_package)

            # Assert
            self.assertIn(local_package, package['path'])
            self.assertTrue(package['file'])
            self.assertFalse(package['ignore-check'])

    def test_get_library_should_return_library_file_when_library_is_in_local(self):
        # Assign
        with clone_fixture('local_package') as working_directory:
            stkml = Stkml(folder=working_directory)
            local_package = 'my_package/Lyra'

            # Acts
            package = stkml.get_library(local_package)

            # Assert
            self.assertIn(local_package, package['path'])
            self.assertTrue(package['file'])
            self.assertFalse(package['ignore-check'])

    def test_get_library_should_return_library_file_when_library_is_in_stkml_packages(self):
        # Assign
        with clone_fixture('stkml_package') as working_directory:
            stkml = Stkml(folder=os.path.join(working_directory, 'example'))
            stkml_package = 'lx/Lyra'

            # Acts
            package = stkml.get_library(stkml_package)

            # Assert
            self.assertIn(stkml_package, package['path'])
            self.assertTrue(package['file'])
            self.assertTrue(package['ignore-check'])

    def test_get_library_should_return_library_folder_when_library_is_in_stkml_packages(self):
        # Assign
        with clone_fixture('stkml_package') as working_directory:
            stkml = Stkml(folder=os.path.join(working_directory, 'example'))
            stkml_package = 'lx'

            # Acts
            package = stkml.get_library(stkml_package)

            # Assert
            self.assertIn(stkml_package, package['path'])
            self.assertFalse(package['file'])
            self.assertTrue(package['ignore-check'])

    def test_check_file_should_return_true_when_file_is_lexcialy_correct(self):
        # Assign
        with clone_fixture('local_package') as working_directory:
            stkml = Stkml(folder=working_directory)
            local_package = 'my_package/Lyra'
            package = stkml.get_library(local_package)

            # Acts
            yaml = stkml.check_file(package)

            # Assert
            self.assertTrue(yaml)
    def test_check_file_should_return_true_when_all_stkml_folder_is_lexcialy_correct(self):
        # Assign
        with clone_fixture('local_package') as working_directory:
            stkml = Stkml(folder=working_directory)
            local_package = 'my_package'
            package = stkml.get_library(local_package)

            # Acts
            yaml = stkml.check_file(package)

            # Assert
            self.assertTrue(yaml)

    def test_validate_schema_should_return_true_when_all_stkml_folder_is_valid_with_stkml_schema(self):
        # Assign
        with clone_fixture('local_package') as working_directory:
            stkml = Stkml(folder=working_directory)
            local_package = 'my_package'
            package = stkml.get_library(local_package)

            # Acts
            yaml = stkml.validate_schema(package)

            # Assert
            self.assertEqual(len(stkml.errors), 0)

    def test_validate_schema_should_return_None_when_stkml_file_is_valid_with_stkml_schema(self):
        # Assign
        with clone_fixture('local_package') as working_directory:
            stkml = Stkml(folder=working_directory)
            local_package = 'my_package'
            package = stkml.get_library(local_package)

            # Acts
            stkml.validate_schema(package)

            # Assert
            self.assertEqual(len(stkml.errors), 0)

    def test_validate_stackml_project_should_return_None_when_stkml_files_is_valid_with_stkml_schema(self):
        # Assign
        with clone_fixture('not_valid_stackml_schema') as working_directory:
            stkml = Stkml(folder=working_directory)
            stkml.check_stackml_project()

            # Acts and Assert
            try:
                stkml.validate_stackml_project()
            except StkmlSyntaxicErrorList as errorList:
                self.assertGreater(len(errorList.errors), 0)

    def test_check_stkml_project_should_return_true_when_stkml_project_is_well_formed(self):
        # Assign
        with clone_fixture('local_package') as working_directory:
            stkml = Stkml(folder=working_directory)

            # Acts
            yaml = stkml.check_stackml_project()

            # Assert
            self.assertTrue(yaml)

    def test_valid_stkml_project_should_return_true_when_stkml_project_is_correct(self):
        # Assign
        with clone_fixture('local_package') as working_directory:
            stkml = Stkml(folder=working_directory)
            stkml.check_stackml_project()

            # Acts
            yaml = stkml.validate_stackml_project()

            # Assert
            self.assertEqual(len(stkml.errors), 0)

    def test_check_stkml_package_should_return_true_when_stkml_package_is_well_formed(self):
        # Assign
        with clone_fixture('stkml_package') as working_directory:
            stkml = Stkml(folder=os.path.join(working_directory, 'Things'))

            # Acts
            yaml = stkml.check_stckml_package()

            # Assert
            self.assertTrue(yaml)
    def test_check_stkml_package_should_raise_ScannerError_exception_when_stkml_package_is_well_formed(self):
        # Assign
        with clone_fixture('stkml_package') as working_directory:
            stkml = Stkml(folder=os.path.join(working_directory, 'Things_'))

            # Acts and Assert
            try:
                 stkml.check_stckml_package()
            except yaml.scanner.ScannerError:
                    pass
            except Exception as exception:
                self.fail(f'invalid exception - {exception}')

    def test_validate_stkml_package_should_return_true_when_stkml_package_respect_stackml_schema(self):
        # Assign
        with clone_fixture('stkml_package') as working_directory:
            stkml = Stkml(folder=os.path.join(working_directory, 'Things'))
            stkml.check_stckml_package()

            # Acts
            yaml = stkml.validate_stackml_project()

            # Assert
            self.assertEqual(len(stkml.errors), 0)

    def test_validate_stkml_package_should_raise__false_when_stkml_package_does_not_respect_stackml_schema(self):
        # Assign
        with clone_fixture('stkml_package') as working_directory:
            stkml = Stkml(folder=os.path.join(working_directory, 'Things__'))
            stkml.check_stckml_package()

            # Acts and Assert
            try :
                stkml.validate_stackml_project()
            except StkmlSyntaxicErrorList:
                pass
            except Exception as exception:
                self.fail(f'invalid exception - {exception}')


if __name__ == '__main__':
    unittest.main()
