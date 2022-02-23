import unittest
from unittest.mock import patch
from parameterized import parameterized

from synctron import prompt_multiple_selection


class TestPromptMultipleSelection(unittest.TestCase):
    """
    Test prompt_multiple_selection method.
    """

    ANY_QUESTION = "any-question"
    ANY_OPTION = "any-option"
    ANY_OTHER_OPTION = "any-other-option"
    ANY_HIDDEN_OPTION = ".any-other-option"
    ANY_OPTIONS = [ANY_OPTION, ANY_OTHER_OPTION, ANY_HIDDEN_OPTION]

    @parameterized.expand([
        [{"choices": [ANY_OPTION]}, [ANY_OPTION]],
        [{"choices": [ANY_OPTION, ANY_OTHER_OPTION]}, [ANY_OPTION, ANY_OTHER_OPTION]],
        [{"choices": [ANY_OPTION, ANY_HIDDEN_OPTION]}, [ANY_OPTION, ANY_HIDDEN_OPTION]],
        [{}, []],  # NOTE: no "choices" in prompt answers
    ])
    @patch('synctron.prompt')
    def test_prompt(self, answers, expected, mock_prompt):
        mock_prompt.return_value = answers

        result = prompt_multiple_selection(self.ANY_QUESTION, self.ANY_OPTIONS)

        self.assertEqual(expected, result)
        mock_prompt.assert_called_once_with([{
            "type": "checkbox",
            "name": "choices",
            "message": self.ANY_QUESTION,
            "choices": [
                {"name": self.ANY_OPTION, "checked": True},
                {"name": self.ANY_OTHER_OPTION, "checked": True},
                {"name": self.ANY_HIDDEN_OPTION, "checked": False},
            ]
        }])


if __name__ == '__main__':
    unittest.main()
