import unittest
from unittest.mock import patch
from parameterized import parameterized

from synctron import prompt_confirmation


class TestPromptConfirmation(unittest.TestCase):
    """
    Test prompt_confirmation method.
    """

    ANY_QUESTION = "any-question"

    @parameterized.expand([
        [{"choice": False}, False],
        [{"choice": True}, True],
        [{}, False],  # NOTE: no "choice" in prompt answer
    ])
    @patch('synctron.prompt')
    def test_prompt(self, answers, expected, mock_prompt):
        mock_prompt.return_value = answers

        result = prompt_confirmation(self.ANY_QUESTION)

        self.assertEqual(expected, result)
        mock_prompt.assert_called_once_with([{
            "type": "confirm",
            "name": "choice",
            "message": self.ANY_QUESTION,
            "default": False
        }])


if __name__ == '__main__':
    unittest.main()
