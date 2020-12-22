import datetime

from django.utils import timezone
from django.urls import reverse
import pytest
from pytest_django.asserts import assertContains, assertQuerysetEqual

from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given question_text and publication date set to a given number of
    days from now. Set 'days' argument to a negative number to indicate a publication date in the
    past.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


@pytest.mark.django_db
class TestIndexView:
    def test_no_questions(self, client):
        """If no questions exist, an appropriate message is displayed"""
        response = client.get(reverse('polls:index'))
        assert response.status_code == 200
        assertContains(response, 'No polls are available.')
        assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self, client):
        """Questions with a pub_date in the past are displayed on the index page."""
        create_question(question_text='Past question.', days=-30)
        response = client.get(reverse('polls:index'))
        assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: Past question.>'])

    def test_future_question(self, client):
        """Questions with a pub_date in the future aren't displays on the index page."""
        create_question(question_text='Future question.', days=30)
        response = client.get(reverse('polls:index'))
        assertContains(response, 'No polls are available.')
        assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self, client):
        """Even if both past and future questions exist, only past questions are displayed."""
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        response = client.get(reverse('polls:index'))
        assertQuerysetEqual(response.context['latest_question_list'],
                            ['<Question: Past question.>'])

    def test_two_past_questions(self, client):
        """The questions index page may display multiple questions."""
        create_question(question_text='Past question 1.', days=-30)
        create_question(question_text='Past question 2.', days=-5)
        response = client.get(reverse('polls:index'))
        assertQuerysetEqual(response.context['latest_question_list'],
                            ['<Question: Past question 2.>',
                             '<Question: Past question 1.>'])
