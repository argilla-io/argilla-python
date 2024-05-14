import uuid

from argilla_sdk import Record, Suggestion, Response


class TestRecords:

    def test_record_repr(self):
        record_id = uuid.uuid4()
        user_id = uuid.uuid4()
        record = Record(
            id=record_id,
            fields={"name": "John", "age": "30"},
            metadata={"key": "value"},
            suggestions=[Suggestion(question_name="question", value="answer")],
            responses=[Response(question_name="question", value="answer", user_id=user_id)],
        )
        assert (
            record.__repr__() == f"Record(id={record_id},"
            "fields={'name': 'John', 'age': '30'},"
            "metadata={'key': 'value'},"
            "suggestions={'question': {'value': 'answer', 'score': None, 'agent': None}},"
            f"responses={{'question': [{{'value': 'answer'}}]}})"
        )
