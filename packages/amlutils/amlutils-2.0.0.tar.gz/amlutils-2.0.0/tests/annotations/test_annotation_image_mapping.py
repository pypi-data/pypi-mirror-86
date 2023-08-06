import os
import tempfile
import unittest

# amlutils imports
from amlutils.annotations import annotation_image_mapping
from amlutils.files_and_folders import folder_utils


class TestAnnotationImageMapping(unittest.TestCase):
    def _create_file(self, file_path, content):
        with open(file_path, "w") as f:
            f.write(content)

    def setUp(self):
        temp_folder = tempfile.mkdtemp()
        self.image_folder = os.path.join(temp_folder, "images")
        self.annotations_folder = os.path.join(temp_folder, "annotations")
        folder_utils.make_folder_if_not_exists(self.image_folder)
        folder_utils.make_folder_if_not_exists(self.annotations_folder)
        num_files_to_create = 5
        for i in range(num_files_to_create):
            self._create_file(os.path.join(self.image_folder, f"prefix_{i}.jpeg"), "jpeg_file")
            self._create_file(os.path.join(self.annotations_folder, f"prefix_{i}.xml"), "annotation_file")
        for i in range(num_files_to_create):
            self._create_file(os.path.join(self.image_folder, f"prefix_{num_files_to_create+i}.png"), "jpeg_file")
            self._create_file(
                os.path.join(self.annotations_folder, f"prefix_{num_files_to_create+i}.xml"),
                "annotation_file",
            )

    def test_annotation_image_mapping(self):
        annotation_image_map = annotation_image_mapping.AnnotationImageMap(
            images_folder=self.image_folder,
            annotations_folder=self.annotations_folder,
        )

        self.assertEqual(
            annotation_image_map.get_image_for_annotation_file("prefix_1.xml"),
            os.path.join(self.image_folder, "prefix_1.jpeg"),
        )
