from django.conf import settings
import logging
import requests
from django.http import HttpResponse, HttpResponseServerError
from django.utils.datastructures import MultiValueDictKeyError

from .recommendation_utils import get_recommended_courses
from .service_discovery import get_service_url

logger = logging.getLogger("recommendation")



def pasta():
    data = {"course_topics":[36, 44],"novice_skills":[21, 19],"intermediate_skills":[],"expert_skills":[]}
    return data



def get_recommendations(request):
    
    try:

        keycloak_id = request.GET['keycloak_id']

        # TODO: authenticate the user with Keycloak service

        user_topics_and_skills = pasta()
        
        # course_service_url = get_service_url('COURSE_SERVICE') + '/api/courses-topics-and-skills'
        course_service_url = settings.LXP_COURSE_SERVICE + '/api/courses-topics-and-skills'
        logger.info(course_service_url)

        courses_topics_and_skills = requests.get(course_service_url).json()
        
        recommended_courses = get_recommended_courses(courses_topics_and_skills, user_topics_and_skills)
        
        return HttpResponse(course_service_url + ' '.join([str(x) for x in recommended_courses]))

    except MultiValueDictKeyError as e:
        logger.exception(e)
        return HttpResponseServerError("Keycloak id not found")

    except Exception as e:
        logger.exception(e)
        return HttpResponseServerError("Internet server error")


    # step 3: get profile service url - not the public one
    # step 4: make network request to profile service passing the ID - if no endpoint, add to profile service
    # step 5: explore GRPC and how to call profile service to get data

    # step 6: get course service url - not the public one
    # step 7: make network request to course service

    # step 8: apply algorithm to filter down courses - no problem for order, present all top ones
    # step 9: pass courses back to front-end