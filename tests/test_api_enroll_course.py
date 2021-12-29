import pytest


def test_put_enroll_user(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>/enroll/<int:id>/' endpoint
    WHEN sending a PUT request with both Course id and User id provided.
    THEN response with HTTP status code 204 is returned
    and the User is enrolled to the Course
    """
    put_response = test_client.put('/api/v1/courses/2/enroll/1/')
    assert put_response.status_code == 204

    get_response = test_client.get('/api/v1/courses/2/')
    json_data = get_response.get_json()
    # assert that User id (id=1) is in the list of enrolled users_id
    assert 1 in json_data.get('users_id')


@pytest.mark.parametrize(
    'route,http_code',
    [('/api/v1/courses/2/enroll//', 404), ('/api/v1/courses//enroll/1/', 404)]
)
def test_put_enroll_missing_params(init_db, test_client, route, http_code):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>/enroll/<int:id>/' endpoint
    WHEN sending a PUT request with either Course id or User id missing.
    THEN response with HTTP status code 404
    and error message is returned
    """
    response = test_client.put(route)
    assert response.status_code == http_code


@pytest.mark.parametrize(
    'route,http_code',
    [('/api/v1/courses/3/enroll/1/', 404), ('/api/v1/courses/1/enroll/4/', 404)]
)
def test_put_enroll_not_exists(init_db, test_client, route, http_code):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>/enroll/<int:id>/' endpoint
    WHEN sending a PUT request where either Course id or User id does not exist.
    THEN response with HTTP status code 404
    and error message is returned
    """
    response = test_client.put(route)
    assert response.status_code == http_code


def test_put_enroll_already_enrolled(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>/enroll/<int:id>/' endpoint
    WHEN sending a PUT request where the User is already enrolled to the Course
    THEN response with HTTP status code 400
    and error message is returned
    """
    response = test_client.put('/api/v1/courses/1/enroll/2/')
    assert response.status_code == 400


def test_put_unenroll_user(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>/unenroll/<int:id>/' endpoint
    WHEN sending a PUT request with both Course id and User id provided.
    THEN response with HTTP status code 204 is returned
    and the User is unenrolled from the Course
    """
    put_response = test_client.put('/api/v1/courses/1/unenroll/2/')
    assert put_response.status_code == 204

    get_response = test_client.get('/api/v1/courses/2/')
    json_data = get_response.get_json()
    # assert that User id (id=2) is no more in the list of enrolled users_id
    assert 2 not in json_data.get('users_id')


@pytest.mark.parametrize(
    'route,http_code',
    [('/api/v1/courses/2/unenroll//', 404), ('/api/v1/courses//unenroll/1/', 404)]
)
def test_put_unenroll_missing_params(init_db, test_client, route, http_code):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>/unenroll/<int:id>/' endpoint
    WHEN sending a PUT request with either Course id or User id missing.
    THEN response with HTTP status code 404
    and error message is returned
    """
    response = test_client.put(route)
    assert response.status_code == http_code


@pytest.mark.parametrize(
    'route,http_code',
    [
        ('/api/v1/courses/3/unenroll/1/', 404), 
        ('/api/v1/courses/1/unenroll/4/', 404)
    ]
)
def test_put_unenroll_not_exists(init_db, test_client, route, http_code):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>/unenroll/<int:id>/' endpoint
    WHEN sending a PUT request where either Course id or User id does not exist.
    THEN response with HTTP status code 404
    and error message is returned
    """
    response = test_client.put(route)
    assert response.status_code == http_code


def test_put_unenroll_not_enrolled(init_db, test_client):
    """
    GIVEN a Flask app with '/api/v1/courses/<int:id>/unenroll/<int:id>/' endpoint
    WHEN sending a PUT request where the User is not enrolled to the Course
    THEN response with HTTP status code 404
    and error message is returned
    """
    response = test_client.put('/api/v1/courses/2/unenroll/1/')
    assert response.status_code == 400
