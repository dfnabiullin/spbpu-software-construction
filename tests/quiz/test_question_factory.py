"""
Tests the module quizbot.quiz.question_factory.
"""
import pytest
from quizbot.quiz.question_factory import QuestionNumber, QuestionString, \
    QuestionBool, QuestionChoice, QuestionChoiceSingle


def test_question_number():
    """
    Tests the general functions of the question class with an instance of the question_number class.
    """

    # Initialize a test instance of question_number
    question = QuestionNumber("Сколько букв в аббревиатуре ИКНК?", "4")

    # checks entered values
    assert question.correct_answer == "4"
    assert question.question == "Сколько букв в аббревиатуре ИКНК?"

    # exception for checking solution without entering user answer
    with pytest.raises(AssertionError):
        question.check_solution()

    # exception for entering no number
    with pytest.raises(AssertionError):
        question.enter_solution("не число")

    # Check wrong user answer
    question.enter_solution("23")
    assert question.user_answer == "23"
    assert not question.check_solution()

    # Check correct user answer
    question.enter_solution("4")
    assert question.check_solution()


def test_question_string():
    """
    Tests instances of the question_strings class.
    """

    # Initialize a test instance of question_number
    question = QuestionString("Какая фамилия у Тимура?", "Карама")

    # Check wrong user answer
    question.enter_solution("Камаро")
    assert not question.check_solution()

    # Check correct user answer
    question.enter_solution("Карама")
    assert question.check_solution()


def test_question_bool():
    """
    Tests instances of the question_bool class.
    """

    # Initialize a test instance of question_number
    question = QuestionBool("Дорога с твердым покрытием по отношению к грунтовой - главная?", "Да")

    # Exception for entering no boolean value
    with pytest.raises(AssertionError):
        question.enter_solution("неправда")

    # Check correct user answer
    question.enter_solution("Да")
    assert question.check_solution()


def test_question_choice():
    """
    Tests instances of the question_choice class.
    """

    # Exception for entering no correct answer
    with pytest.raises(AssertionError):
        QuestionChoice("Виктор-Бот - это ..?", "")

    # Initialize a test instance of question_number
    question = QuestionChoice(
        "Виктор-Бот - это ..?", "Питоновское приложение, Телеграм-бот")

    # Check setting random order
    assert not question.is_random
    question.is_random = True
    assert question.is_random

    # Check the list of possible answers
    assert isinstance(question.possible_answers, list)
    assert len(question.possible_answers) == 2
    question.add_possible_answer("Город")
    assert len(question.possible_answers) == 3

    # Check correct entered user answer
    question.enter_solution("Город, Питоновское приложение")
    assert not question.check_solution()
    question.enter_solution("Телеграм-бот, Питоновское приложение")
    assert question.check_solution()


def test_question_choice_single():
    """
    Tests instances of the question_choice_single class.
    """
    # Exception for entering empty string as correct answer
    with pytest.raises(AssertionError):
        QuestionChoiceSingle("Виктор-Бот - это ..?", "")

    # Initialize a test instance of question_number
    question = QuestionChoiceSingle("Виктор-Бот - это ..?", "Телеграм-бот")

    # Add possible answers
    question.add_possible_answer("Тыр пыр")
    question.add_possible_answer("Восемь дыр")

    # Exception for entering multiple answers by user
    with pytest.raises(AssertionError):
        question.enter_solution("Тыр пыр, Восемь дыр")

    # Check correct entered user answer
    question.enter_solution("Телеграм-бот")
    assert question.check_solution()
