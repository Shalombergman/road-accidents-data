import pytest
from datetime import datetime
from bson import ObjectId
import mongomock

from app import app
from repository.accidents_repository import get_sum_accidents_by_region, get_accidents_by_region_and_date, \
    get_accidents_grouped_by_cause, get_injury_statistics_by_region




@pytest.fixture(scope='function')
def mock_db():
    mock_db = mongomock.MongoClient().db
    return mock_db

@pytest.fixture(scope='function')
def setup_mock_data(mock_db):
    mock_db.accidents.insert_many([
        {
            "_id": ObjectId(),
            "beat_of_occurrence": "225",
            "crash_date": datetime(2022, 5, 8),
            "prim_contributory_cause": "Speeding",
            "injuries_id": ObjectId()
        },
        {
            "_id": ObjectId(),
            "beat_of_occurrence": "225",
            "crash_date": datetime(2022, 6, 10),
            "prim_contributory_cause": "Drunk Driving",
            "injuries_id": ObjectId()
        }
    ])

    mock_db.injuries.insert_many([
        {
            "_id": ObjectId(),
            "injuries_total": 3,
            "injuries_fatal": 1
        },
        {
            "_id": ObjectId(),
            "injuries_total": 2,
            "injuries_fatal": 0
        }
    ])

    return mock_db




def test_get_sum_accidents_by_region(setup_mock_data, monkeypatch):
    mock_db = setup_mock_data
    monkeypatch.setattr('repository.accidents_repository.accidents', mock_db.accidents)
    result = get_sum_accidents_by_region("225")
    assert result == 2


def test_get_accidents_grouped_by_cause_with_context(setup_mock_data, monkeypatch):
    mock_db = setup_mock_data
    monkeypatch.setattr('repository.accidents_repository.accidents', mock_db.accidents)

    with app.app_context():
        result = get_accidents_grouped_by_cause("225")
    result_json = result.json
    assert len(result_json) == 2
    assert result_json[0]['_id'] == "Speeding"
    assert result_json[0]['total_accidents'] == 1

def test_get_accidents_by_region_and_date(setup_mock_data, monkeypatch):
    mock_db = setup_mock_data
    monkeypatch.setattr('repository.accidents_repository.accidents', mock_db.accidents)
    result = get_accidents_by_region_and_date("225", "2022-05-01", "2022-05-10")
    assert len(result) == 1
    assert result[0]['prim_contributory_cause'] == "Speeding"


def test_get_accidents_grouped_by_cause(setup_mock_data, monkeypatch):
    mock_db = setup_mock_data
    monkeypatch.setattr('repository.accidents_repository.accidents', mock_db.accidents)
    result = get_accidents_grouped_by_cause("225")
    assert len(result) == 2
    assert result[0]['_id'] == "Speeding"
    assert result[0]['total_accidents'] == 1


def test_get_injury_statistics_by_region(setup_mock_data, monkeypatch):
    mock_db = setup_mock_data
    monkeypatch.setattr('repository.accidents_repository.accidents', mock_db.accidents)
    monkeypatch.setattr('repository.accidents_repository.injuries', mock_db.injuries)
    result = get_injury_statistics_by_region("225")
    assert result[0]['total_injuries'] == 3
    assert result[0]['fatal_injuries'] == 1
    assert result[0]['non_fatal_injuries'] == 2