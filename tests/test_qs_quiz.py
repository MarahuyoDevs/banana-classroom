import pytest
from starlette import status

# Fixture to create a quiz
@pytest.fixture(scope="function")
def create_quiz_valid_data(test_client):
    """Fixture to create a quiz and return its ID."""
    response = test_client.post(
        "/quiz",
        json={
            "title": "Math Quiz",
            "description": "Test your math skills",
            "instructor": "Mr. Smith",
            "questions": [
                {"description": "What is 2 + 2?", "answer": "4"},
                {"description": "What is 5 * 5?", "answer": "25"},
            ],
        },
    )
    return response.json()["data"]["id"]

# Fixture to create a quiz without questions
@pytest.fixture(scope="function")
def create_quiz_valid_data_without_questions(test_client):
    """Fixture to create a quiz without questions."""
    response = test_client.post(
        "/quiz",
        json={
            "title": "Math Quiz",
            "description": "Test your math skills",
            "instructor": "Mr. Smith",
            "questions": [],
        },
    )
    quiz_id = response.json()["data"]["id"]
    yield quiz_id
    test_client.delete(f"/quiz/{quiz_id}")

# Fixture to create a quiz with duplicate questions
@pytest.fixture(scope="function")
def create_quiz_with_duplicate_questions(test_client):
    """Fixture to create a quiz with duplicate questions."""
    response = test_client.post(
        "/quiz",
        json={
            "title": "Duplicate Questions Quiz",
            "description": "Quiz with duplicate questions",
            "instructor": "Ms. Davis",
            "questions": [
                {"description": "What is 1 + 1?", "options": ["1", "2", "3"], "answer": "2"},
                {"description": "What is 2 + 2?", "options": ["2", "3", "4"], "answer": "4"},
                {"description": "What is 1 + 1?", "options": ["1", "2", "3"], "answer": "2"},
            ],
        },
    )
    return response

# Fixture to create a quiz
@pytest.fixture(scope="function")
def modify_quiz(test_client, create_quiz):
    """Fixture to create a quiz and modify its title."""
    quiz_id = create_quiz
    yield quiz_id
    test_client.delete(f"/quiz/{quiz_id}")

# Test class for creating a quiz
def test_create_quiz_valid_data(test_client):
    """Test creating a quiz with valid data and questions."""
    response = test_client.post(
        "/quiz",
        json={
            "title": "Math Quiz",
            "description": "Test your math skills",
            "instructor": "Mr. Brown",
            "questions": [
                {"description": "What is the capital of France?", "options": ["Paris", "London", "Berlin"], "answer": "Paris"},
                {"description": "2 + 2 = ?", "options": ["1", "2", "4"], "answer": "4"},
            ],
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["title"] == "Math Quiz"
    assert len(response.json()["data"]["questions"]) == 2

# Test class for creating a quiz
def test_create_quiz_valid_data_no_questions(test_client):
    """Test creating a quiz with valid data but without questions."""
    response = test_client.post(
        "/quiz",
        json={
            "title": "Test Quiz",
            "description": "This is a test quiz",
            "instructor": "John Doe",
            "questions": [],
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["title"] == "Test Quiz"
    assert response.json()["data"]["description"] == "This is a test quiz"
    assert response.json()["data"]["instructor"] == "John Doe"
    assert response.json()["data"]["questions"] == []

# Test class for creating a quiz
def test_create_quiz_missing_mandatory_fields(test_client):
    """Test creating a quiz with missing mandatory fields."""
    response = test_client.post(
        "/quiz",
        json={"title": "Test Quiz"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "description" in response.json()["detail"]

# Test class for creating a quiz
def test_create_quiz_with_duplicate_questions(create_quiz_with_duplicate_questions):
    """Test creating a quiz with duplicate questions."""
    response = create_quiz_with_duplicate_questions
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Questions must be unique" in response.json()["detail"]

# Test class for adding a question to an existing quiz
def test_add_valid_question_to_existing_quiz(test_client, create_quiz):
    """Test adding a valid question to an existing quiz."""
    quiz_id = create_quiz
    new_question_data = {
        "description": "What is the capital of France?",
        "options": ["London", "Paris", "Berlin", "Rome"],
        "answer": "Paris",
    }
    response = test_client.post(f"/quiz/{quiz_id}/question", json=new_question_data)
    print("Response status code:", response.status_code)
    print("Response content:", response.content)
    assert response.status_code == 200

# Test class for adding a question to an existing quiz
def test_add_question_with_missing_required_field(test_client, create_quiz):
    """Test adding a question with missing required field to an existing quiz."""
    quiz_id = create_quiz
    new_question_data = {
        "description": "What is the capital of Germany?",
        "options": ["London", "Paris", "Berlin"],  # Missing the answer field
    }
    response = test_client.post(f"/quiz/{quiz_id}/question", json=new_question_data)
    print("Response status code:", response.status_code)
    print("Response content:", response.content)
    assert response.status_code == 422

# Test class for modifying quiz title
def test_modify_quiz_title(test_client):
    """Test modifying quiz title."""
    response = test_client.post(
        "/quiz",
        json={
            "title": "Math Quiz",
            "description": "Test your math skills",
            "instructor": "Mr. Smith",
            "questions": [
                {"description": "What is 2 + 2?", "answer": "4"},
                {"description": "What is 5 * 5?", "answer": "25"},
            ],
        },
    )
    quiz_id = response.json()["data"]["id"]
    new_title = "Math Quiz Updated"
    response = test_client.put(f"/quiz/{quiz_id}/modify_title", json={"title": new_title})
    assert response.status_code == 200

# Test class for modifying quiz description
def test_modify_quiz_description(test_client):
    """Test modifying quiz description."""
    response = test_client.post(
        "/quiz",
        json={
            "title": "History Quiz",
            "description": "Test your knowledge of historical events",
            "instructor": "Ms. Johnson",
            "questions": [
                {"description": "When was the Declaration of Independence signed?", "answer": "1776"},
                {"description": "Who was the first president of the United States?", "answer": "George Washington"},
            ],
        },
    )
    quiz_id = response.json()["data"]["id"]
    new_description = "Test your knowledge of world history"
    response = test_client.put(
        f"/quiz/{quiz_id}/modify_description", json={"description": new_description}
    )
    assert response.status_code == 200