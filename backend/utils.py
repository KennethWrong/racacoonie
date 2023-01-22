import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm


def cosine_similarity(a, b):
    return dot(a, b)/ (norm(a) * norm(b))


def cosine_similarity_to_all_other_user(user_index, user_recipe_matrix):
    # structure [[other_user_index, similarity_score],
    #            [other_user_index1, similarity_score1],
    #            ]
    user_similarities = {}

    for other_user_id in range(user_recipe_matrix.shape[0]):
        if other_user_id == user_index:
            continue

        curr_user = user_recipe_matrix[user_index]
        other_user = user_recipe_matrix[other_user_id]

        similarity = cosine_similarity(curr_user, other_user)
        # user_similarities.append([other_user_id, similarity])
        # user_similarities.append(similarity)
        user_similarities[other_user_id] = similarity
    
    # return np.array(user_similarities)
    return user_similarities