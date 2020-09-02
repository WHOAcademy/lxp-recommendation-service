"""Utilities for Computing Recommendations - Trivial Content-based Matching"""

from math import exp, pi, cos, sin
from numpy import empty, zeros, matmul, transpose, amax, squeeze, argsort



EXP_LEVELS = ['Novice', 'Intermediate', 'Expert']
# converting expertise levels to one-based ordinal values:
exp_level_value_dict = {k: (v + 1) for v, k in enumerate(EXP_LEVELS)}



def get_courses_features(courses_topics_and_skills):
    """Create and return all courses' topic and skill, respectively, feature vectors."""

    # creating dictionaries of topic and skill ids:
    topic_index_dict = {}
    skill_index_dict = {}
    # for each course:
    for course in courses_topics_and_skills:

        # counting unique topics:
        for topic_info in course['course_topics']:
            topic_id = topic_info['id']
            topic_name = topic_info['name']
            if topic_name not in topic_index_dict.keys():
                topic_index_dict[topic_name] = topic_id

        # counting unique skills:
        for skill_info in course['novice_skills']:
            skill_id = skill_info['id']
            skill_slug = skill_info['slug']
            if skill_slug not in skill_index_dict.keys():
                skill_index_dict[skill_slug] = skill_id
        for skill_info in course['intermediate_skills']:
            skill_id = skill_info['id']
            skill_slug = skill_info['slug']
            if skill_slug not in skill_index_dict.keys():
                skill_index_dict[skill_slug] = skill_id
        for skill_info in course['expert_skills']:
            skill_id = skill_info['id']
            skill_slug = skill_info['slug']
            if skill_slug not in skill_index_dict.keys():
                skill_index_dict[skill_slug] = skill_id

    feature_info = (topic_index_dict, skill_index_dict)

    n_courses = len(courses_topics_and_skills)
    course_title_dict = {}

    # course features array - samples along first dimension (position represents course id), topics along second dimension:
    course_topic_features = zeros((n_courses, len(topic_index_dict)))
    # skill features array - samples along first dimension (position represents course id), skills along second dimension:
    course_skill_features = zeros((n_courses, len(skill_index_dict)))

    # for each course:
    for course in courses_topics_and_skills:

        course_id = course['id'] - 1 # ZERO BASED
        # updating dictionary of course titles:
        course_title = course['title']
        course_title_dict[course_id] = course_title

        # topic features:
        for topic_info in course['course_topics']:

            topic_id = topic_info['id']
            course_topic_features[course_id, topic_id - 1] = 1

        # skill features:
        # TO BE BETTER IMPLEMENTED:
        expertise = EXP_LEVELS[0]
        for skill_info in course['novice_skills']:

            skill_id = skill_info['id']
            course_skill_features[course_id, skill_id - 1] = exp_level_value_dict[expertise]

        expertise = EXP_LEVELS[1]
        for skill_info in course['intermediate_skills']:

            skill_id = skill_info['id']
            course_skill_features[course_id, skill_id - 1] = exp_level_value_dict[expertise]

        expertise = EXP_LEVELS[2]
        for skill_info in course['expert_skills']:

            skill_id = skill_info['id']
            course_skill_features[course_id, skill_id - 1] = exp_level_value_dict[expertise]

    return course_topic_features, course_skill_features, feature_info, course_title_dict



def get_user_features(user_topics_and_skills, topic_index_dict, skill_index_dict):
    """Compute and return respectively topic and skill feature vectors for user."""

    n_topics = len(topic_index_dict)
    n_skills = len(skill_index_dict)

    # extracting topics:
    print(user_topics_and_skills)
    user_topics = user_topics_and_skills['interests']

    # topic features:
    user_topic_features = zeros((1, n_topics)) # unfilled features already equal zero
    for topic in user_topics:
        topic_id = topic_index_dict[topic['name']]
        user_topic_features[0, topic_id - 1] = 1

    # extracting skills' expertise:
    user_skills_with_expertise = user_topics_and_skills['skills']

    # skill features:
    user_skill_features = zeros((1, n_skills)) # unfilled features already equal zero
    for skill_with_expertise in user_skills_with_expertise:
        skill_id = skill_with_expertise['slug']
        expertise = skill_with_expertise['rating']
        # TO BE BETTER IMPLEMENTED - fixing ununified naming convention:
        if expertise == '':
            continue
        if expertise == 'Master':
            expertise = 'Expert'
        user_skill_features[0, skill_id - 1] = exp_level_value_dict[expertise]

    return user_topic_features, user_skill_features



def compute_topic_similarities(course_topic_feature_vectors, user_topic_feature_vector):
    """Compute topic similarities between user and courses."""

    # computing topic similarities - scalar product among dummy topic variables, so as to maximize
    # the similarity for a given course when the number of topics that both the considered course and
    # the user deal with is maximum:
    topic_similarities = matmul(course_topic_feature_vectors, transpose(user_topic_feature_vector))

    return topic_similarities



def expertise_matching(course_skill_exp_level, user_skill_exp_level):
    """Compute the matching score between two expertise levels.
    (argument names do not imply distinctions in the current implementation)"""

    # if either one of the two expertise levels is 0, there is no matching; the function used
    # in the complementary case would be (i) maximized when both skills are 0, and (ii) yield
    # non-null values which can overwhelm the score in case of highly sparse skill feature vectors,
    # while this case must count as "no match" (no level inserted by user or required by course)
    # so as not to underweight relevant skills in a sparse representation with a high skill feature
    # space dimensionality:
    if course_skill_exp_level == 0 or user_skill_exp_level == 0:
        return 0

    # else, yielding the actual matching score:
    else:
        # returning a gaussian evolving only along one of the two axes resulting by tilting
        # by pi/4 in the bidimensional input space of the two expertise levels - emplpoed to
        # maximize (maximum is 1) matching score of equal expertise levels while decreasing
        # matching score increasingly with difference in expertise levels, tending to 0 for
        # an infinite difference:
        level_matching = exp(-(((course_skill_exp_level * (-sin(pi / 4)) + user_skill_exp_level * cos(pi / 4)) ** 2) * 1))

        return level_matching



def compute_skill_similarities(course_skill_feature_vectors, user_skill_feature_vector):
    """Compute skill expertise similarities between user and courses."""

    # each user-course pair has a score:
    n_courses = course_skill_feature_vectors.shape[0]
    skill_similarities = empty((n_courses, 1))

    # for each course:
    for i in range(n_courses):

        #for each skill:
        for matching_score in map(expertise_matching, course_skill_feature_vectors[i,], user_skill_feature_vector[0,]):

            # computing skill expertise similarity for the considered skill - custom function to maximize expertise matching -
            # and adding it to the course similarity score:
            skill_similarities[i,] += matching_score

    return skill_similarities



def get_recommended_courses(courses_topics_and_skills, user_topics_and_skills, n_top = 7):
    """Compute top n recommended courses, descendingly ordered by relevance."""

    # getting curses' features:
    courses_topic_features, courses_skill_features, feature_info, course_title_dict = get_courses_features(courses_topics_and_skills)
    # ... and feature index dictionaries:
    (topic_index_dict, skill_index_dict) = feature_info

    # getting user features:
    user_topic_features, user_skill_features = get_user_features(user_topics_and_skills, topic_index_dict, skill_index_dict)

    # user-course similarity scores based on topics:
    topic_similarities = compute_topic_similarities(courses_topic_features, user_topic_features)

    # user-course similarity scores based on skills:
    skill_similarities = compute_skill_similarities(courses_skill_features, user_skill_features)

    # recommendation based on maximizing average of (normalized) topic and skill scores:
    similarities = (topic_similarities / amax(topic_similarities)) + (skill_similarities / amax(skill_similarities))

    # returning the most top relevant courses' indexes, in ascending order:
    top_indexes = argsort(squeeze(similarities))[-1 : -(n_top+1) : -1]

    # retrieving respective course titles:
    top_titles = [course_title_dict[indx] for indx in top_indexes]

    return top_titles
