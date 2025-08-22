from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import records

# Create your tests here.

class DeleteRecordViewTest(TestCase):
    def setUp(self):
        """Set up test data for the tests."""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.record = records.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            address='123 Main St',
            city='Anytown',
            state='Anystate',
            zipcode='12345'
        )

    def test_delete_record_authenticated(self):
        """Test that an authenticated user can delete a record."""
        self.client.login(username='testuser', password='testpassword')
        
        url = reverse('delete_record', kwargs={'pk': self.record.pk})
        response = self.client.get(url)

        # Check for redirect to home
        self.assertRedirects(response, reverse('home'))

        # Check that the record was deleted
        with self.assertRaises(records.DoesNotExist):
            records.objects.get(pk=self.record.pk)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "record deleted successfully")

    def test_delete_record_unauthenticated(self):
        """Test that an unauthenticated user is redirected and cannot delete."""
        url = reverse('delete_record', kwargs={'pk': self.record.pk})
        response = self.client.get(url)

        # Check for redirect to home
        self.assertRedirects(response, reverse('home'))

        # Check that the record still exists
        self.assertTrue(records.objects.filter(pk=self.record.pk).exists())

        # Check for error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please Login")

    def test_delete_non_existent_record_raises_error(self):
        """Test that trying to delete a non-existent record raises DoesNotExist."""
        self.client.login(username='testuser', password='testpassword')
        non_existent_pk = 999
        url = reverse('delete_record', kwargs={'pk': non_existent_pk})
        
        with self.assertRaises(records.DoesNotExist):
            self.client.get(url)
