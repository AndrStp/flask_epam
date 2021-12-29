import pytest


def test_get_all_users(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/' endpoint
    WHEN sending a GET request
    THEN response with HTTP status code 200 and data with
    all Users in json format is returned
    """
    response = test_client.get('/api/v1/users/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert len(json_data.get('users')) == 3


def test_get_user_by_id(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/' endpoint
    WHEN sending a GET request with 'id'
    THEN response with HTTP status code 200 and data with
    a User (id=id) in json format is returned
    """
    response = test_client.get('/api/v1/users/1/')
    json_data = response.get_json()
    assert response.status_code == 200
    assert json_data.get('username') == 'user1'


def test_get_user_not_exists(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/' endpoint
    WHEN sending a GET request with 'id' of non-existent User
    THEN response with HTTP status code 404 and error message
    in json format is returned
    """
    response = test_client.get('/api/v1/users/4/')
    json_data = response.get_json()
    assert response.status_code == 404
    assert json_data


def test_post_user(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/' endpoint
    WHEN sending a POST request with a valid request body (json):
    'username', 'email', 'password'
    THEN response with HTTP status code 201 is returned
    and new user is created with fields provided within POST request body
    """
    request_body = {
        'username': 'new_test_user',
        'email': 'new_test@email.org',
        'password': 'secure_password'
    }
    post_response = test_client.post('/api/v1/users/', json=request_body)
    assert post_response.status_code == 201

    get_response = test_client.get('/api/v1/users/4/')
    json_data = get_response.get_json()
    assert json_data.get('username') == 'new_test_user'
    assert json_data.get('email') == 'new_test@email.org'


@pytest.mark.parametrize('request_body', 
                         [
                            {
                                'username': 'new_test_user', 
                                'email': 'new_test@email.org',
                            },
                            {
                                'username': 'new_test_user', 
                                'password': 'new_test@email.org',
                            },
                            {
                                'email': 'new_test@email.org', 
                                'password': 'password',
                            }
                         ])
def test_post_user_missing_fields(init_db, test_client, request_body):
    """
    GIVEN a Flask app with '/api/v1/users/' endpoint
    WHEN sending a POST request with invalid request body (json):
    missing one of the following fields: 'username', 'email', 'password'
    THEN response with HTTP status code 400 is returned
    """
    response = test_client.post('/api/v1/users/', json=request_body)
    assert response.status_code == 400


@pytest.mark.parametrize('request_body', 
                         [
                             {
                                'username': 'user1',
                                'email': 'valid@email.org',
                                'password': 'password'
                             },
                             {
                                'username': 'user4',
                                'email': 'test1@email.org',
                                'password': 'password'
                             }
                         ])
def test_post_user_not_unique_fields(init_db, test_client, request_body):
    """
    GIVEN a Flask app with '/api/v1/users/' endpoint
    WHEN sending a POST request with invalid request body (json):
    either: 'username' or 'email' are already present in the db
    THEN response with HTTP status code 400 is returned
    """
    response = test_client.post('/api/v1/users/', json=request_body)
    assert response.status_code == 400
    

def test_put_user(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with a valid request body (json):
    Requires 'username', 'confirmed', 'first_name' and 'second_name' fileds.
    THEN response with HTTP status code 204 is returned
    """
    request_body = {
        'username': 'user1',
        'confirmed': 'true',
        'first_name': 'New_fname',
        'second_name': 'New_sname'
    }
    put_response = test_client.put('/api/v1/users/1/', json=request_body)
    assert put_response.status_code == 204

    get_response = test_client.get('/api/v1/users/1/')
    json_data = get_response.get_json()
    assert json_data.get('confirmed') == True
    assert json_data.get('first_name') == 'New_fname'
    assert json_data.get('second_name') == 'New_sname'


def test_put_user_missing_id(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request without providing a User id
    THEN response with HTTP status code 400 is returned
    """
    request_body = {
        'username': 'user1',
        'confirmed': 'true',
        'first_name': 'New_fname',
        'second_name': 'New_sname'
    }
    response = test_client.put('/api/v1/users/', json=request_body)
    assert response.status_code == 400


def test_put_user_not_exists(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with a not existing User id
    THEN response with HTTP status code 404 is returned
    """
    request_body = {
        'username': 'user1',
        'confirmed': 'true',
        'first_name': 'New_fname',
        'second_name': 'New_sname'
    }
    response = test_client.put('/api/v1/users/4/', json=request_body)
    assert response.status_code == 404


@pytest.mark.parametrize('request_body', 
                         [
                            {
                                'confirmed': 'true',
                                'first_name': 'new_s_name',
                                'second_name': 'new_f_name',
                            },
                            {
                                'username': 'user1', 
                                'first_name': 'new_s_name',
                                'second_name': 'new_f_name',
                            },
                            {
                                'username': 'user1', 
                                'confirmed': 'true',
                                'second_name': 'new_f_name',
                            },
                            {
                                'username': 'user1', 
                                'confirmed': 'true',
                                'first_name': 'new_s_name',
                            }
                         ])
def test_put_user_missing_fields(init_db, test_client, request_body):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with invalid request body (json):
    missing one of the following fields: 
    'username', 'confirmed', 'first_name', 'second_name'.
    THEN response with HTTP status code 400 is returned
    """
    response = test_client.put('/api/v1/users/1/', json=request_body)
    assert response.status_code == 400


@pytest.mark.parametrize('request_body', 
                         [
                             {
                                'username': 'user2',
                                'confirmed': 'true',
                                'first_name': 'new_s_name',
                                'second_name': 'new_f_name',
                             },
                             {
                                'username': 'user3',
                                'confirmed': 'true',
                                'first_name': 'new_s_name',
                                'second_name': 'new_f_name',
                             }
                         ])
def test_post_user_not_unique_username(init_db, test_client, request_body):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a PUT request with invalid request body (json):
    'username' is already taken by another User
    THEN response with HTTP status code 400 is returned
    """
    response = test_client.put('/api/v1/users/1/', json=request_body)
    assert response.status_code == 400


def test_delete_user(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a DELETE request with User id provided
    THEN response with HTTP status code 204 is returned
    and User is deleted from the db
    """
    del_response = test_client.delete('/api/v1/users/1/')
    assert del_response.status_code == 204

    get_response = test_client.get('/api/v1/users/1/')
    assert get_response.status_code == 404
    

def test_delete_user_missing_id(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a DELETE request with no User id provided
    THEN response with HTTP status code 400 is returned
    """
    response = test_client.delete('/api/v1/users/')
    assert response.status_code == 400


def test_delete_user_not_exists(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/users/<int:id>' endpoint
    WHEN sending a DELETE request with a not existing User id
    THEN response with HTTP status code 404 is returned
    """
    response = test_client.delete('/api/v1/users/4/')
    assert response.status_code == 404
