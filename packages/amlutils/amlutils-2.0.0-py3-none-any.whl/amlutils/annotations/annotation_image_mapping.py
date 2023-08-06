from typing import Optional

import os
import random
import typing


class AnnotationImageMap:
    def __init__(self, images_folder: str, annotations_folder: str) -> None:
        """Helper class to map annotations files to corresponding images irrespective of extension

        Parameters
        ----------
        images_folder: str
            full path to folder where images are stored
        annotations_folder: str
            full path to folder where the XML annotations are stored
            the annotations should end in .xml
        """
        self.images_folder = images_folder
        self.annotations_folder = annotations_folder
        self.images = os.listdir(images_folder)
        self.annotations = os.listdir(annotations_folder)
        self.base_to_image_name = {
            os.path.splitext(image_name)[0]: image_name for image_name in self.images
        }

    def get_image_for_annotation_file(self, annotation_file_name: str) -> Optional[str]:
        """get corresponding full image path for the given annotation file name

        Parameters
        ----------
        annotation_file_name: str
            only the file_name of the annotation file for whom the corresponding image file is needed

        Returns
        -------
            full image path to the corresponding image file in the image subfolder or None if image does not exist
        """
        annotation_base_name, _ = os.path.splitext(os.path.basename(annotation_file_name))
        image_name = self.base_to_image_name.get(annotation_base_name)

        if not image_name:
            return None

        image_path = os.path.join(self.images_folder, image_name)
        if os.path.exists(image_path):
            return image_path
        else:
            return None

    def get_all_annotations_to_images(self) -> typing.Dict[str, str]:
        """get all annotation to image files paths for the given folders

        Returns
        -------
            Dictionary of annotation file names to image file names
        """
        annotations_to_images = {}
        for annotation_name in self.annotations:
            base_name = os.path.splitext(annotation_name)[0]
            if base_name in self.base_to_image_name:
                annotations_to_images[annotation_name] = self.base_to_image_name[base_name]
        return annotations_to_images

    def get_image_annotation_pair(self) -> typing.Optional[typing.Dict[str, str]]:
        """get a random image annotation pair

        Returns:
            typing.Optional[typing.Dict[str, str]]: Dictionary containing paths of image and annotation
            {
                "image": full path to image file,
                "annotation": full path to annotation file,
            }
            or None if no image annotation pair can be found
        """
        for trial in range(5):
            annotation_name = random.choice(self.annotations)
            base_name = os.path.splitext(annotation_name)[0]
            if base_name in self.base_to_image_name:
                image_name = self.base_to_image_name.get(base_name)
                return {
                    "image": os.path.join(self.images_folder, image_name),
                    "annotation": os.path.join(self.annotations_folder, annotation_name),
                }

        return None
