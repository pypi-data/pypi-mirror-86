import unittest
import tempfile
from pyWorkflowRevealjs import Generator


class TestGenerator(unittest.TestCase):

    def test_generator(self):

        with tempfile.TemporaryDirectory() as temp_dir:
            settings = {'workflowFile': 'tests/resources/workflow.csv', 'imageFolder': 'tests/resources/images', 'outputFolder': temp_dir,
                        'slideFolder': 'tests/resources/slides', 'versions': [0, 1], 'createLinearPresentations': True, 'createWorkflowPresentation': True}

            Generator(settings)
