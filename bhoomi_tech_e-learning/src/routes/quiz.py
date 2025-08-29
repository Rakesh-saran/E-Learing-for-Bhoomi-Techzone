from fastapi import APIRouter, HTTPException, Depends
from database.schemas.quiz import QuizSchema
from database.schemas.quiz_result import QuizSubmission, QuizResult
from database.repositories.quiz_repository import QuizRepository
from database.repositories.quiz_result_repository import QuizResultRepository
from middleware import get_current_user, require_role

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.post("/")
def add_quiz(quiz: QuizSchema, current_user = Depends(require_role("instructor"))):
    result = QuizRepository.create(quiz.dict()) 
    
    quiz_dict = quiz.dict()
    quiz_dict["id"] = str(result.inserted_id)
    return quiz_dict

@router.get("/")
def list_quizzes():
    quizzes = QuizRepository.find_all()
    for q in quizzes:
        q["id"] = str(q["_id"])
        q.pop("_id")
    return quizzes

@router.get("/{quiz_id}")
def get_quiz(quiz_id: str):
    quiz = QuizRepository.find_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    quiz["id"] = str(quiz["_id"])
    quiz.pop("_id")
    
    # Remove correct answers from response for students
    for question in quiz.get("questions", []):
        question.pop("answer", None)
    
    return quiz

@router.post("/{quiz_id}/submit")
def submit_quiz(quiz_id: str, submission: QuizSubmission, current_user = Depends(get_current_user)):
    quiz = QuizRepository.find_by_id(quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Calculate score
    questions = quiz.get("questions", [])
    correct_answers = 0
    total_questions = len(questions)
    
    for i, question in enumerate(questions):
        if i < len(submission.answers) and submission.answers[i] == question["answer"]:
            correct_answers += 1
    
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Save result
    result_dict = {
        "user_id": str(current_user["_id"]),
        "quiz_id": quiz_id,
        "score": score,
        "total_questions": total_questions,
        "correct_answers": correct_answers
    }
    
    result = QuizResultRepository.create(result_dict)

    return {
        "id": str(result.inserted_id),
        "user_id": result_dict["user_id"],
        "quiz_id": result_dict["quiz_id"],
        "score": result_dict["score"],
        "total_questions": result_dict["total_questions"],
        "correct_answers": result_dict["correct_answers"]
    }


@router.get("/{quiz_id}/results")
def get_quiz_results(quiz_id: str, current_user = Depends(require_role("instructor"))):
    results = QuizResultRepository.find_by_quiz(quiz_id)
    for r in results:
        r["id"] = str(r["_id"])
        r.pop("_id")
    return results

@router.delete("/{quiz_id}")
def remove_quiz(quiz_id: str, current_user = Depends(require_role("instructor"))):
    result = QuizRepository.delete(quiz_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return {"message": "Quiz deleted"}
