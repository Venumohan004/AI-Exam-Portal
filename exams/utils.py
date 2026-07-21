# exams/utils.py

def analyze_performance(attempt):
    percentage = attempt.percentage

    if percentage >= 80:
        level = "Excellent"
        strengths = ["Strong problem solving", "Good conceptual understanding"]
        weaknesses = ["Advanced optimization techniques"]
        topics = ["Advanced Python", "Algorithms"]
        prep_time = "1-2 weeks"

    elif percentage >= 60:
        level = "Good"
        strengths = ["Good understanding of basics"]
        weaknesses = ["Complex programming concepts"]
        topics = ["Functions", "OOP", "Error Handling"]
        prep_time = "2-3 weeks"

    elif percentage >= 40:
        level = "Average"
        strengths = ["Basic syntax knowledge"]
        weaknesses = ["Loops", "Functions", "Logical thinking"]
        topics = ["Variables", "Loops", "Functions"]
        prep_time = "4-6 weeks"

    else:
        level = "Needs Improvement"
        strengths = ["Willingness to learn"]
        weaknesses = ["Core programming concepts", "Problem solving"]
        topics = ["Variables", "Loops", "Functions", "OOP"]
        prep_time = "6-8 weeks"

    return {
        "overall_level": level,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommended_topics": topics,
        "estimated_preparation_time": prep_time,
    }