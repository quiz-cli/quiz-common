from pydantic import TypeAdapter

from quiz_common.models import Message, TextMessage, QuestionMessage, AnswerMessage

def test_json_text_message_round_trip() -> None:
    """Test that TextMessage can be validated and serialized and has correct fields."""
    
    json_data = '{"type":"text","text":"Hello, {user_name}!","params":{"user_name":"Alice"}}'
    
    msg = TypeAdapter(Message).validate_json(json_data)
    assert isinstance(msg, TextMessage) 
    assert msg.type == "text"
    assert msg.text == "Hello, {user_name}!"
    assert msg.params == {"user_name": "Alice"}

    json_received = msg.model_dump_json()
    assert json_received == json_data

def test_json_question_message_round_trip() -> None:
    """Test that QuestionMessage can be validated and serialized and has correct fields."""
    
    json_data = '{"type":"quiz_question","question":{"text":"2+2 = ?","time_limit":null,"options":[{"answer":"4","correct":true},{"answer":"3","correct":false}]}}'
    
    msg = TypeAdapter(Message).validate_json(json_data)
    assert isinstance(msg, QuestionMessage) 
    assert msg.type == "quiz_question"
    assert msg.question.text == "2+2 = ?"
    assert len(msg.question.options) == 2
    assert msg.question.options[0].answer == "4"
    assert msg.question.options[0].correct is True
    assert msg.question.options[1].answer == "3"
    assert msg.question.options[1].correct is False

    json_received = msg.model_dump_json()
    assert json_received == json_data   

def test_json_answer_message_round_trip() -> None:
    """Test that AnswerMessage can be validated and serialized and has correct fields."""
    
    json_data = '{"type":"quiz_answer","client_id":"Alice","answer":[true,false,true]}'
    
    msg = TypeAdapter(Message).validate_json(json_data)
    assert isinstance(msg, AnswerMessage) 
    assert msg.type == "quiz_answer"
    assert msg.client_id == "Alice"
    assert msg.answer == [True, False, True]

    json_received = msg.model_dump_json()
    assert json_received == json_data
