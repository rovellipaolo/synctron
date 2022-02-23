import unittest
from unittest.mock import patch

from synctron import prompt_single_selection


class TestPromptSingleSelection(unittest.TestCase):
    """
    Test prompt_single_selection method.
    """

    ANY_QUESTION = "any-question"
    ANY_OPTION = "any-option"
    ANY_OTHER_OPTION = "any-other-option"
    ANY_OPTIONS = [ANY_OPTION, ANY_OTHER_OPTION]

    @patch('synctron.prompt')
    def test_happy_case(self, mock_prompt):
        mock_prompt.return_value = {"choice": self.ANY_OPTION}

        result = prompt_single_selection(self.ANY_QUESTION, self.ANY_OPTIONS)

        self.assertEqual(self.ANY_OPTION, result)
        mock_prompt.assert_called_once_with([{
            "type": "list",
            "name": "choice",
            "message": self.ANY_QUESTION,
            "choices": self.ANY_OPTIONS
        }])

    @patch('synctron.prompt')
    def test_no_choice_error(self, mock_prompt):
        mock_prompt.return_value = {}  # NOTE: no "choice" in prompt answer

        with self.assertRaises(SystemExit) as result:
            prompt_single_selection(self.ANY_QUESTION, self.ANY_OPTIONS)

        self.assertEqual(1, result.exception.code)
        mock_prompt.assert_called_once()


if __name__ == '__main__':
    unittest.main()
