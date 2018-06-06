from django.test import TestCase

from unittest.mock import patch


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_homepage(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self):
        # self.send_mail_called = False

        # # uses self to assign vars to outer scope
        # def fake_send_email(subject, body, from_email, to_list):
        #     self.send_mail_called = True
        #     self.subject = subject
        #     self.body = body
        #     self.from_email = from_email
        #     self.to_list = to_list

        # # works because send_mail is imported by account.views
        # # this line reassigns the function definition to our fake send mail
        # accounts.views.send_mail = fake_send_email

        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'noreply@superlists')
        self.assertEqual(self.to_list, ['edith@example.com'])