import os
import pandas as pd
from django.shortcuts import render
from django.conf import settings

def welcome_view(request):
    return render(request, 'predictor/welcome.html')

def input_view(request):
    return render(request, 'predictor/input.html')

def predict(request):
    if request.method == 'POST':
        # 🟡 1. Collect student scores from POST
        student_scores = []
        for key, value in request.POST.items():
            if key.startswith('input'):
                try:
                    student_scores.append(float(value))
                except ValueError:
                    continue

        # print("Student Scores:", student_scores)

        # 🟡 2. Load the two CSV files
        students_csv = os.path.join(settings.BASE_DIR, 'predictor', 'data', '1403_kankor_scores.csv')
        faculties_csv = os.path.join(settings.BASE_DIR, 'predictor', 'data', '1403_faculties.csv')

        students_df = pd.read_csv(students_csv)
        faculties_df = pd.read_csv(faculties_csv)

        # 🟡 3. Clean and prepare the data
        students_df['result'] = students_df['result'].astype(str).str.strip().str.lower()
        students_df['score'] = pd.to_numeric(students_df['score'], errors='coerce')
        faculties_df.columns = faculties_df.columns.str.strip().str.lower().str.replace(" ", "_")
        faculties_df['faculty'] = faculties_df['faculty'].astype(str).str.strip().str.lower()

        students_df = students_df.dropna(subset=['result', 'score'])

        # print("\nStudents DataFrame:")
        # print(students_df.head())

        # print("\nFaculties DataFrame:")
        # print(faculties_df.head())


        # 🟡 4. Calculate average score per faculty
        faculty_avg = students_df.groupby('result')['score'].mean().reset_index()
        faculty_avg.columns = ['faculty', 'average_score']

        # 🟡 5. Merge average score with faculty info
        full_df = pd.merge(faculty_avg, faculties_df, on='faculty', how='inner')
        full_df = full_df.dropna(subset=['lowest_score', 'highest_score'])

        # 🟡 6. Calculate pass chances
        results = []
        for _, row in full_df.iterrows():
            faculty = row['faculty']
            low = row['lowest_score']
            high = row['highest_score']
            avg = row['average_score']

            best_chance = 0
            for score in student_scores:
                if score < low:
                    chance = 10  # minimum 10%
                elif score >= high:
                    chance = 100
                else:
                    chance = ((score - low) / (high - low)) * 100

                if chance > best_chance:
                    best_chance = chance

            results.append({
                'faculty': faculty.title(),
                'average_score': round(avg, 2),
                'lowest_score': int(low),
                'highest_score': int(high),
                'pass_chance': round(best_chance, 2)
            })
        # 🔥 (IMPORTANT) Move these lines OUTSIDE of the loop
        final_df = pd.DataFrame(results)

        valuable_top10 = final_df.sort_values(by='average_score', ascending=False).head(10)
        match_top10 = final_df.sort_values(by='pass_chance', ascending=False).head(10)

        # 🟡 7. Send context to template
        context = {
            'valuable_faculties': valuable_top10.to_dict(orient='records'),
            'best_matching_faculties': match_top10.to_dict(orient='records'),
        }
        return render(request, 'predictor/result.html', context)

    else:
        # If not POST, return to input page
        return render(request, 'predictor/input.html')
