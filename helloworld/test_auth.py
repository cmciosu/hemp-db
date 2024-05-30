from django.test import Client, TestCase
from urllib.parse import urlencode

class AuthTest(TestCase):
  c = Client()

  def testRegistrationLogin(self) -> None:
    """
    Tests registering a new user, then logging in with that user.
    Responses to both requests should be 302 redirects to '/' homepage

    Parameters:
    self (AuthTest)

    Returns:
    None
    """
    data = urlencode({
      "username": "test", 
      "email": "test@email.com", 
      "full_name": "test runner", 
      "password1": "testpassword1",
      "password2": "testpassword1"
    })
    res = self.c.post("/user/register", data, follow=True, content_type="application/x-www-form-urlencoded")
    self.assertEqual([('/', 302)], res.redirect_chain)

    data = urlencode({
      "username": "test",
      "password": "testpassword1"
    })  
    res = self.c.post("/user/login/", data, follow=True, content_type="application/x-www-form-urlencoded")
    self.assertEqual([('/', 302)], res.redirect_chain)

  def testRegistrationTemplate(self) -> None:
    """
    Verifies the correct template is served when user wants to register

    Parameters:
    self (AuthTest)

    Returns:
    None
    """
    res = self.c.get("/user/register")
    self.assertEqual(res.status_code, 200)
    self.assertTemplateUsed(res, template_name="registration/register.html")

  def testLoginTemplate(self) -> None:
    """
    Verifies the correct template is served when user wants to register

    Parameters:
    self (AuthTest)

    Returns:
    None
    """
    res = self.c.get("/user/login/")
    self.assertEqual(res.status_code, 200)
    self.assertTemplateUsed(res, template_name="registration/login.html")
