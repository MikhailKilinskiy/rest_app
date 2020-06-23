from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
from ..models import Cost
from ..serializers import CostSerializer
from ..views import CostService
from datetime import date
import json


class CostTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='TestUser', password='test1234%')
        self.client.force_authenticate(user=self.user)
        self.view = CostService.as_view()
        self.serializer = CostSerializer
        self.fields = ['id', 'name', 'amount', 'date', 'create_date', 'user']

    def do_test_can_post_cost(self):
        count_before = Cost.objects.count()
        cost = Cost(name='Test', amount=122.88, date=date(2019,10,1), user=self.user)
        data = JSONRenderer().render(self.serializer(cost).data)
        response = self.client.post("/fin/", content_type='application/json', pk=1, data=data)
        print("RESP: ", response.json())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(count_before + 1, Cost.objects.count())

    def do_test_can_put_cost(self):
        cost = Cost.objects.filter(name='Test').values(*self.fields).first()
        cost['name']='TestTest'
        data = JSONRenderer().render(cost)
        response = self.client.put("/fin/", pk=cost['id'], content_type='application/json', data=data)
        print("RESP: ", response.json())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), json.loads(data))

    def do_test_can_get_cost(self):
        response = self.client.get("/fin/")
        print("RESP: ", response.json())
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response['content-type'], 'application/json')

    def do_test_can_delete_cost(self):
        count_before = Cost.objects.count()
        cost = Cost.objects.get(pk=1)
        data = JSONRenderer().render(self.serializer(cost).data)
        response = self.client.delete("/fin/", pk=cost.id, content_type='application/json', data=data)
        print("RESP: ", response)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(count_before - 1, Cost.objects.count())

    def test_rest_api(self):
        print("************* TEST POST *************")
        self.do_test_can_post_cost()
        print("************* TEST PUT *************")
        self.do_test_can_put_cost()
        print("************* TEST GET *************")
        self.do_test_can_get_cost()
        print("************* TEST DELETE *************")
        self.do_test_can_delete_cost()



