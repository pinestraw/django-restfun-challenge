import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from order.models import Order


class OrderApiTest(APITestCase):
    fixtures = ["test-data.json"]

    def setUp(self):
        user, _ = User.objects.get_or_create(username="test")
        self.token, _ = Token.objects.get_or_create(user=user)
        self.valid_payload = {"items": [{"product": 2, "options": 2}, {"product": 3}]}
        self.invalid_items_payload = {"items": [{"product": 3, "options": 2}]}

    def test_make_ord_valid_data(self):
        response = self.make_order(self.valid_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(), {"status": "WAITING", "id": 1, "amount": "150.00"}
        )

    def test_make_ord_invalid_items(self):
        response = self.make_order(self.invalid_items_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"items": [{"non_field_errors": ["please select valid option"]}]},
        )

    def test_update_ord_valid_data(self):
        response = self.make_order(self.valid_payload)
        self.assertEqual(response.status_code, 201)
        order_id = response.json()["id"]
        response = self.client.put(
            reverse("orders:order-detail", kwargs={"pk": order_id}),
            data=json.dumps({"items": [{"product": 2, "options": 2}]}),
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.token.key,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"status": "WAITING", "id": 1, "amount": "100.00"}
        )

    def test_update_ord_status_waiting(self):
        response = self.make_order(self.valid_payload)
        self.assertEqual(response.status_code, 201)
        order_id = response.json()["id"]
        response = self.update_order(
            order_id, {"items": [{"product": 2, "options": 2}]}
        )
        self.assertEqual(
            response.json(), {"status": "WAITING", "id": 1, "amount": "100.00"}
        )
        self.assertEqual(response.status_code, 200)

    def test_update_ord_status_not_waiting(self):
        response = self.make_order(self.valid_payload)
        self.assertEqual(response.status_code, 201)
        order_id = response.json()["id"]
        for status in ["PREPARATION", "READY", "DELIVER"]:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            response = self.update_order(
                order_id, {"items": [{"product": 2, "options": 2}]}
            )
            self.assertEqual(
                response.json(),
                {"detail": "You do not have permission to perform this action."},
            )
            self.assertEqual(response.status_code, 403)

    def test_delete_ord_status_waiting(self):
        response = self.make_order(self.valid_payload)
        self.assertEqual(response.status_code, 201)
        order_id = response.json()["id"]
        response = self.delete_order(order_id)
        self.assertEqual(response.status_code, 204)

    def test_delete_ord_status_not_waiting(self):
        response = self.make_order(self.valid_payload)
        self.assertEqual(response.status_code, 201)
        order_id = response.json()["id"]
        for status in ["PREPARATION", "READY", "DELIVER"]:
            order = Order.objects.get(id=order_id)
            order.status = status
            order.save()
            response = self.delete_order(order_id)
            self.assertEqual(
                response.json(),
                {"detail": "You do not have permission to perform this action."},
            )
            self.assertEqual(response.status_code, 403)

    def update_order(self, order_id, data):
        response = self.client.put(
            reverse("orders:order-detail", kwargs={"pk": order_id}),
            data=json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.token.key,
        )
        return response

    def delete_order(self, order_id):
        response = self.client.delete(
            reverse("orders:order-detail", kwargs={"pk": order_id}),
            HTTP_AUTHORIZATION="Token " + self.token.key,
        )
        return response

    def make_order(self, data):
        response = self.client.post(
            reverse("orders:order-list"),
            data=json.dumps(data),
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.token.key,
        )
        return response
