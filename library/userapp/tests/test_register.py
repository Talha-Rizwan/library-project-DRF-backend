# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from userapp.models import User  
# import json

# class UserProfileViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user_data = {
#         "username": "new_name",
#         "full_name": "q ",
#         "password": "123",
#         "gender" : "M",
#         "phone": "00039383"
#         }
        
#         self.user = User.objects.create_user(**self.user_data)

#     def test_create_user_profile(self):
#         url = '/api/user/user-profile/'  
#         response = self.client.post(url, data=self.user_data, format='json')
#         print(response.data, " the response.")

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         new_user = User.objects.get(username=self.user_data['username'])
#         self.assertIsNotNone(new_user)
        

#     def test_update_user_profile(self):
#         url = '/api/user/user-profile/'  
#         self.client.login(username=self.user_data['username'], password=self.user_data['password'])
#         updated_data = {
#             'username': 'newusername',
#         }
        
#         response = self.client.put(url, data=updated_data, format='json')
#         print(response.data, " the response.")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)

        
#         updated_user = User.objects.get(username=updated_data['username'])
#         self.assertIsNotNone(updated_user)

