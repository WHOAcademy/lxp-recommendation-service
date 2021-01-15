from typing import Dict, List, Tuple, Union


def arrange_content_metadata(
    module_json_content: List[Dict[str, Union[str, int, Dict[str, \
        Union[str, List[Dict[str, int]], List[str]]]]]]
)-> Tuple[Dict[int, Dict[int, int]], Dict[int, Dict[int, int]], \
        Dict[int, str], List[int]]:  
    """
    Loading all dummy module data in convenient variable types
    """

    # loading modules...

    # ... as an id-to-required-skill-levels mapping:
    module_id_2_required_skill_2_level_dicts = {
        module['pk']: {
            requirements['skill']: requirements['expertise_level'] \
                for requirements in module['fields']['required_skill_levels']
        } for module in module_json_content
    }

    # ... as an id-to-awarded-skill-levels mapping:
    module_id_2_awarded_skill_2_level_dicts = {
        module['pk']: {
            award['skill']: award['expertise_level'] \
                for award in module['fields']['awarded_skill_levels']
        } for module in module_json_content
    }

    # ... as an id-to-contained-topics mapping:
    module_id_2_contained_topic_ids_dict = {
        module['pk']: module['fields']['contained_topics'] \
            for module in module_json_content
    }

    # as ids:
    module_ids = {module['pk'] for module in module_json_content}

    return module_id_2_required_skill_2_level_dicts, \
        module_id_2_awarded_skill_2_level_dicts, \
        module_id_2_contained_topic_ids_dict, \
        module_ids

def get_top_recommendations(
    module_id_2_required_skill_2_level_dicts: Dict[int, Dict[int, int]],
    module_id_2_awarded_skill_2_level_dicts: Dict[int, Dict[int, int]],
    module_id_2_contained_topic_ids_dict: Dict[int, List[str]],
    module_ids: List[int],
    user_skill_id_2_level_id_dict: Dict[int, int],
    user_topics_of_interest: List[str],
    n_top: int
    ) -> List[int]:
    """
    Returning the list of course ids sorted by recommended importance, in 
    descending order, ranking based on number of contained topics of interest
    first, and, this criterion being equal, on being attendable or not as 
    second criterion.
    """
    module_scores = []
    module_attendable_flags = [True] * len(module_ids)
    for i, module_id  in enumerate(module_ids):
        module_scores.append(
            len(
                set(user_topics_of_interest) & \
                    set(module_id_2_contained_topic_ids_dict[module_id])
            )
        )
        for skill_id in \
            module_id_2_required_skill_2_level_dicts[module_id].keys():
            if user_skill_id_2_level_id_dict.get(skill_id, -1) < \
                module_id_2_required_skill_2_level_dicts[module_id][skill_id]:
                module_attendable_flags[i] = False
                break
    sorted_module_ids,  _, _ = list(
        zip(
            *sorted(
                zip(
                    module_ids,
                    module_scores,
                    module_attendable_flags
                ),
                key=lambda x: (x[1], x[2]),
                reverse=True
            )
        )
    )
    return sorted_module_ids[:n_top]
