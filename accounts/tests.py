from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegistrationTests(APITestCase):
    def test_public_signup_cannot_assign_privileged_role(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "customer1", "email": "customer1@example.com",
            "password": "Valid-Strong-Password-2026!",
            "password_confirm": "Valid-Strong-Password-2026!", "role": "ADMIN",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username="customer1")
        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_password_mismatch_is_rejected(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "customer2", "email": "customer2@example.com",
            "password": "Valid-Strong-Password-2026!", "password_confirm": "Mismatch-Password-2026!",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="customer", email="customer@example.com", password="Valid-Strong-Password-2026!")

    def test_login_returns_access_and_refresh(self):
        response = self.client.post(reverse("accounts:login"), {"username": "customer", "password": "Valid-Strong-Password-2026!"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_me_requires_authentication(self):
        self.assertEqual(self.client.get(reverse("accounts:me")).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_role(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("accounts:me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], User.Role.CUSTOMER)

    def test_logout_blacklists_users_refresh_token(self):
        self.client.force_authenticate(self.user)
        refresh = str(RefreshToken.for_user(self.user))
        response = self.client.post(reverse("accounts:logout"), {"refresh": refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
