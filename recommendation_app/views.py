import logging
from django.http import HttpResponse, HttpResponseServerError
from django.utils.datastructures import MultiValueDictKeyError

from recommendation_utils import get_recommended_courses

logger = logging.getLogger("recommendation")



def pizza():
    data = [{"id":1,"course_topics":[1,2,3,4,5,6],"novice_skills":[1,2,3],"intermediate_skills":[],"expert_skills":[]},{"id":2,"course_topics":[1,7,8],"novice_skills":[3,4,5],"intermediate_skills":[],"expert_skills":[]},{"id":3,"course_topics":[1,9,10],"novice_skills":[6,7,8,9],"intermediate_skills":[],"expert_skills":[]},{"id":4,"course_topics":[1,9],"novice_skills":[4,5,8,10],"intermediate_skills":[],"expert_skills":[]},{"id":5,"course_topics":[1,7],"novice_skills":[3,5,8,11],"intermediate_skills":[],"expert_skills":[]},{"id":6,"course_topics":[1,9],"novice_skills":[2,3,12],"intermediate_skills":[],"expert_skills":[]},{"id":7,"course_topics":[1,2,3,4,5],"novice_skills":[1,2],"intermediate_skills":[],"expert_skills":[]},{"id":8,"course_topics":[1,2,3,4,5],"novice_skills":[2,3,4,5,10,12,13],"intermediate_skills":[],"expert_skills":[]},{"id":9,"course_topics":[1,2,3,4,5],"novice_skills":[3,12,14],"intermediate_skills":[],"expert_skills":[]},{"id":10,"course_topics":[1,7,11],"novice_skills":[4,5,10,13,15],"intermediate_skills":[],"expert_skills":[]},{"id":11,"course_topics":[11,12,13,14],"novice_skills":[9,13,15],"intermediate_skills":[],"expert_skills":[]},{"id":12,"course_topics":[11,12,14,15],"novice_skills":[9,13,15,16,17,18],"intermediate_skills":[],"expert_skills":[]},{"id":13,"course_topics":[8,11,16],"novice_skills":[3,5,9,10,13,15,17,18],"intermediate_skills":[],"expert_skills":[]},{"id":14,"course_topics":[11,14,17,18],"novice_skills":[4,5,13,15,17,18],"intermediate_skills":[],"expert_skills":[]},{"id":15,"course_topics":[11,14,19,20],"novice_skills":[4,5,13,15,17,18],"intermediate_skills":[],"expert_skills":[]},{"id":16,"course_topics":[11,20],"novice_skills":[5,9,13,18],"intermediate_skills":[],"expert_skills":[]},{"id":17,"course_topics":[11,12,14],"novice_skills":[9,13,15,17,18],"intermediate_skills":[],"expert_skills":[]},{"id":18,"course_topics":[11,12,14,21],"novice_skills":[5,13,18],"intermediate_skills":[],"expert_skills":[]},{"id":19,"course_topics":[11,13,20],"novice_skills":[5,13],"intermediate_skills":[],"expert_skills":[]},{"id":20,"course_topics":[8,11,14,22],"novice_skills":[5,13,14,15,17,18],"intermediate_skills":[],"expert_skills":[]},{"id":21,"course_topics":[9],"novice_skills":[2,3,12],"intermediate_skills":[],"expert_skills":[]},{"id":22,"course_topics":[23],"novice_skills":[14],"intermediate_skills":[],"expert_skills":[]},{"id":23,"course_topics":[23],"novice_skills":[1],"intermediate_skills":[],"expert_skills":[]},{"id":24,"course_topics":[10],"novice_skills":[6,7,8,19],"intermediate_skills":[],"expert_skills":[]},{"id":25,"course_topics":[24],"novice_skills":[6,11],"intermediate_skills":[],"expert_skills":[]},{"id":26,"course_topics":[23],"novice_skills":[6,11],"intermediate_skills":[],"expert_skills":[]},{"id":27,"course_topics":[23],"novice_skills":[19],"intermediate_skills":[],"expert_skills":[]},{"id":28,"course_topics":[9,23],"novice_skills":[2,12],"intermediate_skills":[],"expert_skills":[]},{"id":29,"course_topics":[10,25],"novice_skills":[6,7,8,9,11],"intermediate_skills":[],"expert_skills":[]},{"id":30,"course_topics":[10,25],"novice_skills":[8,9],"intermediate_skills":[],"expert_skills":[]},{"id":31,"course_topics":[26],"novice_skills":[13,20,21],"intermediate_skills":[],"expert_skills":[]},{"id":32,"course_topics":[26,27],"novice_skills":[10,13,20,21],"intermediate_skills":[],"expert_skills":[]},{"id":33,"course_topics":[26,27],"novice_skills":[10,20],"intermediate_skills":[],"expert_skills":[]},{"id":34,"course_topics":[26,27],"novice_skills":[10,21],"intermediate_skills":[],"expert_skills":[]},{"id":35,"course_topics":[28],"novice_skills":[3,14,20],"intermediate_skills":[],"expert_skills":[]},{"id":36,"course_topics":[26,27],"novice_skills":[10,20,21],"intermediate_skills":[],"expert_skills":[]},{"id":37,"course_topics":[29],"novice_skills":[2],"intermediate_skills":[],"expert_skills":[]},{"id":38,"course_topics":[26,27],"novice_skills":[13,20,21],"intermediate_skills":[],"expert_skills":[]},{"id":39,"course_topics":[26,27],"novice_skills":[10,13,20,21],"intermediate_skills":[],"expert_skills":[]},{"id":40,"course_topics":[26,27],"novice_skills":[10,13,20],"intermediate_skills":[],"expert_skills":[]},{"id":41,"course_topics":[25,30,31],"novice_skills":[1,2,8],"intermediate_skills":[],"expert_skills":[]},{"id":42,"course_topics":[8,32,33,34],"novice_skills":[9,15,16],"intermediate_skills":[],"expert_skills":[]},{"id":43,"course_topics":[25,35],"novice_skills":[8,11],"intermediate_skills":[],"expert_skills":[]},{"id":44,"course_topics":[17,25],"novice_skills":[6,9,19],"intermediate_skills":[],"expert_skills":[]},{"id":45,"course_topics":[4,5,8,25,36],"novice_skills":[8,9,11,15,16],"intermediate_skills":[],"expert_skills":[]},{"id":46,"course_topics":[17,25,37],"novice_skills":[6,8,9,11],"intermediate_skills":[],"expert_skills":[]},{"id":47,"course_topics":[8,14,25],"novice_skills":[6,9,11,15,17],"intermediate_skills":[],"expert_skills":[]},{"id":48,"course_topics":[25,38],"novice_skills":[2,6,11],"intermediate_skills":[],"expert_skills":[]},{"id":49,"course_topics":[25,39,40],"novice_skills":[2,11],"intermediate_skills":[],"expert_skills":[]},{"id":50,"course_topics":[10,25,41,42,43],"novice_skills":[8,11],"intermediate_skills":[],"expert_skills":[]},{"id":51,"course_topics":[25,44],"novice_skills":[19],"intermediate_skills":[],"expert_skills":[]}]
    return data

def pasta():
    data = {"course_topics":[36, 44],"novice_skills":[21, 19],"intermediate_skills":[],"expert_skills":[]}
    return data



def get_recommendations(request):
    
    try:

        keycloak_id = request.GET['keycloak_id']

        # TODO: authenticate the user with Keycloak service

        user_topics_and_skills = pasta()

        courses_topics_and_skills = pizza()
        
        #recommended_courses = get_recommended_courses(courses_topics_and_skills, user_topics_and_skills)

        #return HttpResponse(''.join([str(x) for x in recommended_courses]))
        return HttpResponse('OK')

    except MultiValueDictKeyError as e:
        logger.exception(e)
        return HttpResponseServerError("Keycloak id not found")

    except Exception as e:
        logger.exception(e)
        return HttpResponseServerError("Internel server error")


    # step 3: get profile service url - not the public one
    # step 4: make network request to profile service passing the ID - if no endpoint, add to profile service
    # step 5: explore GRPC and how to call profile service to get data

    # step 6: get course service url - not the public one
    # step 7: make network request to course service

    # step 8: apply algorithm to filter down courses - no problem for order, present all top ones
    # step 9: pass courses back to front-end