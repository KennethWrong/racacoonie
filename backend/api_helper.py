from flask import request, json, jsonify, make_response, send_from_directory

def create_response(message='', status_code=200, mimetype='application/json'):

    # if isinstance(message, list):
    #     json_return = {}
    #     for i, x in enumerate(message):
    #         temp_json = {}
    #         temp_json['id'] = x[0]
    #         temp_json['title'] = x[1]
    #         temp_json['content'] = x[2]
    #         temp_json['upvotes'] = len(clean_string(x[3]))
    #         temp_json['downvotes'] = len(clean_string(x[4]))
    #         # -1 for dislike, 0 for nothing, 1 for like (only used for initial load)
    #         temp_json['vote'] = get_prev_vote(
    #             clean_string(x[3]), clean_string(x[4]), user_id)
    #         temp_json['date'] = x[5]
    #         temp_json['user_id'] = x[6]
    #         json_return[i] = temp_json
    #     response = make_response(json_return)

    response = make_response(message)
    # elif isinstance(message, tuple):
    #     temp_json = {}
    #     temp_json['username'] = message[0]
    #     temp_json['user_id'] = message[2]
    #     temp_json['picture_id'] = message[3]
    #     response = make_response(temp_json)
    # else:
    #     response = make_response(message)

    response.status_code = status_code
    response.mimetype = mimetype
    return response