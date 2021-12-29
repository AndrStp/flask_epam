from py import test
import pytest


def test_get_all_courses(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/' endpoint
    WHEN sending a GET request
    THEN response with HTTP status code 200 and data with
    all Courses in json format is returned
    """
    response = test_client.get('/api/v1/courses/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert len(json_data.get('courses')) == 2


def test_get_course_by_id(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/' endpoint
    WHEN sending a GET request
    THEN response with HTTP status code 200 and data with
    a Course (id=id) in json format is returned
    """
    response = test_client.get('/api/v1/courses/1/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data.get('label') == 'course1'


def test_get_course_not_exists(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>' endpoint
    WHEN sending a GET request with 'id' of non-existent Course
    THEN response with HTTP status code 404 and error message
    in json format are returned
    """
    response = test_client.get('/api/v1/courses/3/')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data


def test_post_course(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>' endpoint
    WHEN sending a POST request with a valid request body (json):
    'label', 'level', 'small_desc'. 'exam' field is optional
    and valid User id
    THEN response with HTTP status code 201 is returned
    and a new course is created with fields provided within POST request body
    """
    request_body = {
        'label': 'New Test Course',
        'exam': 'true',
        'level': 'R',
        'small_desc': 'Some description'
    }
    post_response = test_client.post('/api/v1/courses/1/', json=request_body)
    assert post_response.status_code == 201

    get_response = test_client.get('/api/v1/courses/3/')
    json_data = get_response.get_json()
    assert get_response.status_code == 200
    assert json_data.get('label') == 'New Test Course'


def test_post_course_no_id(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>' endpoint
    WHEN sending a POST request with a valid request body (json):
    'label', 'exam', 'level', 'small_desc' and no User id
    THEN response with HTTP status code 400 
    and error message in json format are returned
    """
    request_body = {
        'label': 'New Test Course',
        'exam': 'true',
        'level': 'R',
        'small_desc': 'Some description'
    }
    post_response = test_client.post('/api/v1/courses/', json=request_body)
    assert post_response.status_code == 400


def test_post_course_id_not_exists(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>' endpoint
    WHEN sending a POST request with a valid request body (json):
    'label', 'exam', 'level', 'small_desc' and User id is not
    present in the db
    THEN response with HTTP status code 400 
    and error message in json format are returned
    """
    request_body = {
        'label': 'New Test Course',
        'exam': 'true',
        'level': 'R',
        'small_desc': 'Some description'
    }
    post_response = test_client.post('/api/v1/courses/4/', json=request_body)
    assert post_response.status_code == 400


@pytest.mark.parametrize('request_body', 
                         [
                            {
                                'level': 'R',
                                'small_desc': 'Some description'
                            },
                            {
                                'label': 'New Test Course',
                                'small_desc': 'Some description'
                            },
                            {
                                'label': 'New Test Course',
                                'level': 'R',
                            }
                         ])
def test_post_course_missing_fields(init_db, test_client, request_body):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>' endpoint
    WHEN sending a POST request with a invalid request body (json):
    missing one of the following fields: 'label', 'level', 'small_desc'
    THEN response with HTTP status code 400 
    and error message in json format are returned
    """
    response = test_client.post('/api/v1/courses/1/', json=request_body)
    assert response.status_code == 400


def test_post_not_unique_label(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>' endpoint
    WHEN sending a POST request with a invalid request body (json):
    'label' is already taken by another Course in the db
    THEN response with HTTP status code 400 
    and error message in json format are returned
    """
    request_body = {
        'label': 'course1',
        'exam': 'true',
        'level': 'R',
        'small_desc': 'Some description'
    }
    response = test_client.post('/api/v1/courses/1/', json=request_body)
    assert response.status_code == 400


def test_put_course(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with a valid request body (json):
    Requires 'label', 'level', 'small_desc' fileds and a Course id.
    THEN response with HTTP status code 204 is returned
    """
    request_body = {
        'label': 'course1',
        'exam': 'true',
        'level': 'R',
        'small_desc': 'New description'
    }
    put_response = test_client.put('/api/v1/courses/1/', json=request_body)
    assert put_response.status_code == 204

    get_response = test_client.get('/api/v1/courses/1/')
    json_data = get_response.get_json()
    assert json_data.get('exam') == True
    assert json_data.get('level') == 'R'
    assert json_data.get('small_desc') == 'New description'


def test_put_course_no_id(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with a Course id missing.
    THEN response with HTTP status code 400 is returned
    """
    request_body = {
        'label': 'course1',
        'exam': 'true',
        'level': 'R',
        'small_desc': 'New description'
    }
    response = test_client.put('/api/v1/courses/', json=request_body)
    assert response.status_code == 400


def test_put_course_id_not_exists(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with a non-existent Course id.
    THEN response with HTTP status code 404 is returned
    """
    request_body = {
        'label': 'course1',
        'exam': 'true',
        'level': 'R',
        'small_desc': 'New description'
    }
    response = test_client.put('/api/v1/courses/3/', json=request_body)
    assert response.status_code == 400


@pytest.mark.parametrize('request_body', 
                         [
                            {
                                'level': 'R',
                                'small_desc': 'Some description'
                            },
                            {
                                'label': 'New Test Course',
                                'small_desc': 'Some description'
                            },
                            {
                                'label': 'New Test Course',
                                'level': 'R',
                            }
                         ])
def test_put_course_missing_fields(init_db, test_client, request_body):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with a invalid request body (json):
    missing one of the following fields: 'label', 'level', 'small_desc'
    THEN response with HTTP status code 400 is returned
    """
    response = test_client.put('/api/v1/courses/1/', json=request_body)
    assert response.status_code == 400


def test_put_course_not_unique_label(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with a invalid request body (json):
    'label' is already taken by another Course in the db
    THEN response with HTTP status code 204 is returned
    """
    request_body = {
        'label': 'course2',
        'exam': 'true',
        'level': 'R',
        'small_desc': 'New description'
    }
    response = test_client.put('/api/v1/courses/1/', json=request_body)
    assert response.status_code == 400


def test_delete_course(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a DELETE request with a valid request body (json):
    Requires 'username', 'confirmed', 'first_name' and 'second_name' fileds.
    THEN response with HTTP status code 204 is returned
    and the Course is removed from the db
    """
    del_response = test_client.delete('/api/v1/courses/1/')
    assert del_response.status_code == 204
    
    get_response = test_client.get('/api/v1/courses/1/')
    assert get_response.status_code == 404


def test_delete_course_no_id(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a DELETE request with a no Course id provided:
    THEN response with HTTP status code 400 is returned
    """
    response = test_client.delete('/api/v1/courses/')
    assert response.status_code == 400


def test_delete_course_id_not_exists(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a DELETE request with a non-existent Course id :
    THEN response with HTTP status code 404 is returned
    """
    response = test_client.delete('/api/v1/courses/3/')
    assert response.status_code == 404
