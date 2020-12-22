from django.urls import reverse
import pytest
from pytest_django.asserts import assertContains

from test_index_view import create_question


@pytest.mark.django_db
class TestDetailView:
    def test_future_question(self, client):
        """The detail view of a question with a pub_date in the future returns 404"""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', kwargs={'pk': future_question.id})
        response = client.get(url)
        assert response.status_code == 404

    def test_past_question(self, client):
        """The detail view of a question with a pub_date in the past displays the question's text"""
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', kwargs={'pk': past_question.id})
        response = client.get(url)
        assertContains(response, past_question.question_text)
