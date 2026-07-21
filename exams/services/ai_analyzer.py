def generate_ai_feedback(attempt):

    percentage = attempt.percentage


    if percentage >= 80:

        overall_feedback = (
            "Excellent performance. "
            "You have strong understanding of the concepts."
        )

        strengths = (
            "Good accuracy in solving questions.\n"
            "Strong conceptual understanding."
        )

        weaknesses = (
            "Continue practicing advanced topics."
        )


        recommendations = (
            "Practice more difficult level questions "
            "to improve further."
        )


    elif percentage >= 60:


        overall_feedback = (
            "Good performance but improvement is possible."
        )

        strengths = (
            "Basic concepts are clear."
        )


        weaknesses = (
            "Needs more practice in difficult questions."
        )


        recommendations = (
            "Revise important topics and attempt more mock exams."
        )


    else:


        overall_feedback = (
            "More practice is required."
        )


        strengths = (
            "Some concepts are understood."
        )


        weaknesses = (
            "Many concepts require improvement."
        )


        recommendations = (
            "Study fundamentals and practice regularly."
        )


    return {

        "strengths": strengths,

        "weaknesses": weaknesses,

        "recommendations": recommendations,

        "overall_feedback": overall_feedback

    }