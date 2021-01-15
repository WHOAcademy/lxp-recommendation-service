from functools import wraps
from unittest.mock import patch

from django.urls import reverse
from django.conf import settings
from rest_framework.test import APITestCase

from requests import codes


def mocked_cache_page(timeout):
    """
    defining mocked cache service response adopted within the 
    tested method execution:
    """
    def do_nothing():
        pass

    class MockCacheBehavior:
        def __init__(self, *args):
            pass

        def __call__(self):
            return do_nothing
    
    return MockCacheBehavior(timeout)
    
def mocked_requests_get(url):
    """
    defining mocked responses reveived when calling the APIs of the profile 
    service and the course service within the tested method execution:
    """
    class MockServiceResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    # when calling the profile service:
    if url.startswith(settings.LXP_PROFILE_SERVICE):

        if url.endswith('0'):

            mock_data = {
                "possessed skill levels": {
                    "2": 0
                },
                "topics of interest": [
                    "Q84263196",
                    "Q192995"
                ]
            }

        elif url.endswith('1'):

            mock_data = {
                "possessed skill levels": {
                    "2": 1
                },
                "topics of interest": [
                    "Q189603"
                ]
            }

        elif url.endswith('2'):

            mock_data = {
                "possessed skill levels": {
                    "0": 2,
                    "1": 2,
                    "2": 2,
                    "3": 2,
                    "4": 2
                },
                "topics of interest": [
                    "Q84263196",
                    "Q192995",
                    "Q189603"
                ]
            }

        elif url.endswith('3'):

            mock_data = {
                "possessed skill levels": {
                    
                },
                "topics of interest": [
                    
                ]
            }

        elif url.endswith('4'):

            mock_data = {
                "possessed skill levels": {
                    "1": 2,
                    "0": 1
                },
                "topics of interest": [
                    "Q192995"
                ]
            }

        else:

            raise Exception("can't work: unexpected mocked Keycloak id - \
                corresponding test case does not exist")

        return MockServiceResponse(mock_data, 200)

    # when calling the course service:
    elif url.startswith(settings.LXP_COURSE_SERVICE):

        mock_data = [{"model":"module_model","pk":0,"fields":{"title":"Biology at a Microscopic Scale","required_skill_levels":[{"skill":2,"expertise_level":0}],"awarded_skill_levels":[{"skill":2,"expertise_level":1}],"contained_topics":["Q84263196"]}},{"model":"module_model","pk":1,"fields":{"title":"Advanced Epidemiology: The Science Behind","required_skill_levels":[{"skill":2,"expertise_level":1}],"awarded_skill_levels":[{"skill":4,"expertise_level":2}],"contained_topics":["Q192995"]}},{"model":"module_model","pk":2,"fields":{"title":"COVID-19 Response: Advanced Prevention Strategies","required_skill_levels":[{"skill":4,"expertise_level":2}],"awarded_skill_levels":[{"skill":1,"expertise_level":2}],"contained_topics":["Q84263196"]}},{"model":"module_model","pk":3,"fields":{"title":"Advanced Practices: Infection, Prevention and Control","required_skill_levels":[{"skill":2,"expertise_level":1}],"awarded_skill_levels":[{"skill":1,"expertise_level":2}],"contained_topics":["Q189603"]}},{"model":"module_model","pk":4,"fields":{"title":"A Gentle Introduction to Personal Protective Equipment against COVID-19","required_skill_levels":[],"awarded_skill_levels":[{"skill":0,"expertise_level":1}],"contained_topics":["Q84263196"]}},{"model":"module_model","pk":5,"fields":{"title":"Outbreaks: How to Guide Populations During Public Healthcare Emergencies","required_skill_levels":[{"skill":1,"expertise_level":2},{"skill":0,"expertise_level":1}],"awarded_skill_levels":[{"skill":3,"expertise_level":2}],"contained_topics":["Q189603"]}}]
        return MockServiceResponse(mock_data, 200)

    else:

        raise Exception("can't work: unknown service URL")

def patch_all_mocks(original_function):
    """
    combining all patch decorators used for mocking external services/
    dependencies in unit tests
    """
    # mocking the cache service response and the cache behavior happening 
    # within the tested method execution:
    @patch('recommendation_app.views.cache_page',
        side_effect=mocked_cache_page)

    # mocking the API calls happening within the tested method execution:
    @patch('recommendation_app.views.requests_get',
        side_effect=mocked_requests_get)

    @wraps(original_function)

    def decorated_function(*args, **kwargs):
        return original_function(*args, **kwargs)
        
    return decorated_function
    

class TestRecommendationView(APITestCase):

    # def get_valid_keycloak_id(self):
    #     """
    #     get a valid Keycloak id by fetching the existing profiles
    #     https://test-lxp-profile-service-labs-test.apps.who.lxp.academy.who.int/api/v1/profiles
    #     """
    #     # sending request to profile service to retrieve the available profiles:
    #     profile_service_api_url = settings.LXP_PROFILE_SERVICE + '/api/v1/profiles'
    #     profile_service_response = requests_get(profile_service_api_url)

    #     # when the request to the profile service is not successful:
    #     if profile_service_response.status_code != codes.ok:
    #         return None

    #     profiles = profile_service_response.json()
        
    #     # when no valid id currently exists:
    #     if not profiles:
    #         return None
        
    #     # returning the first id encountered:
    #     return profiles[0]['keycloak_id']

    @patch_all_mocks          
    def test_get_method(self, *args):
        """
        get() returns a json response following the expected structure and 
        yielding all ond only the expected recommendations and in the correct
        order of importance for the given test cases.
        """
        
        # # getting a valid Keycloak id for testing:
        # keycloak_id = self.get_valid_keycloak_id()
        # NOTE: not using a real Keycloak id because doing only unit tests

        # invented Keycloak ids for testing:
        keycloak_ids = [
            "abcdefgh0",
            "abcdefgh1",
            "abcdefgh2",
            "abcdefgh3",
            "abcdefgh4"
        ]

        # corresponding expected recommendations to be returned:
        corresponding_expected_recommendations = [
            [
                {
                    "id": 0,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 4,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 1,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                }
            ],
            [
                {
                    "id": 3,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 5,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 0,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                }
            ],
            [
                {
                    "id": 0,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 1,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 2,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                }
            ],
            [
                {
                    "id": 4,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 0,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 1,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                }
            ],
            [
                {
                    "id": 1,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 4,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                },
                {
                    "id": 5,
                    "title": "Lorem Ipsum",
                    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                    "duration_seconds": 18000,
                    "creation_date": "2020-07-13T12:45:26.401000Z",
                    "last_mod_date": "2020-08-11T10:38:29Z"
                }
            ]
        ]

        # asserting correctness of results for different test cases:
        for keycloak_id, expected_recommendations in \
            zip(keycloak_ids, corresponding_expected_recommendations):

            # making request to test the view's get method:
            url = reverse("list-recommendations",
                args=[keycloak_id])
            response = self.client.get(url, format='json')
            
            # asserting the request has succeeded:
            self.assertEqual(response.status_code, 200)

            computed_recommendations = response.data
            
            # asserting the response contains all ond only the expected, 
            # correct recommendations, both in terms of content and data 
            # types of fields, and in the right order:
            self.assertEqual(expected_recommendations, \
                computed_recommendations)
