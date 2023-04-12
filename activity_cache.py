from pip._vendor import requests
import json

url='https://trackapi.nutritionix.com/v2/natural/exercise'
headers = {
    "x-app-id": "ce50cb8a",
    "x-app-key": "23ab83e7ce98ac4d9ca3df633a91d0b9",
    "Content-Type" : "application/json"
}

activities = ["Running","Swimming","Cycling","Weightlifting","Yoga","Pilates","High-intensity interval training (HIIT)","CrossFit","Boxing","Kickboxing","Martial arts","Dancing","Zumba","Aerobics","Step aerobics","Jogging","Walking","Hiking","Rock climbing","Kayaking","Canoeing","Rowing","Sailing","Surfing","Skiing","Snowboarding","Ice skating","Rollerblading","Skateboarding","Parkour","Calisthenics","Gymnastics","Tennis","Badminton","Table tennis","Basketball","Volleyball","Soccer","Football","Baseball","Softball","Golf","Archery","Fencing","Shooting","Horseback riding","Fishing","Hunting","Bungee jumping","Skydiving","Paragliding","Hang gliding","Scuba diving","Snorkeling","Free diving","Surf fishing","Fly fishing","Bodybuilding","Powerlifting","Strongman","Olympic weightlifting","Functional training","TRX","Kettlebell training","Battle ropes","Medicine ball training","Resistance band training","Sled pushing/pulling","Farmers walk","Deadlift","Squat","Bench press","Overhead press","Pull-up","Chin-up","Dip","Leg press","Leg curl","Leg extension","Calf raise","Abdominal crunch","Plank","Russian twist","Side plank","Glute bridge","Lunges","Step-ups","Burpees","Jumping jacks","Mountain climbers","Plie squat","Wall sit","Bear crawl","Crab walk","Inchworm","Jump rope","Stair climbing","Elliptical trainer","Rowing machine","Stationary bike","Treadmill","Sled training","Prowler push","Sprints","Circuit training","Tabata training","Bodyweight training","Gymnastics rings","Swiss ball training","Plyometrics","Sprint training","Tempo runs","Fartlek","Hill repeats","Intervals","Pyramid training","EMOM","AMRAP","AFAP","Tabata"]

exercise_data = []
added_names = set()
for activity in activities:
    # Request body
    input = {
        'query': activity
    }

    # Send POST request to API
    response = requests.post(url, headers=headers, json=input)

    # Get the calorie burned from the response
    if response.status_code == 200:
        for exercise in response.json()["exercises"]:
            name = exercise['name']
            if name not in added_names:
                added_names.add(name)
                exercise_data.append({
                    "name": name,
                    "MET": exercise['met'],
                    "calories per min": exercise['nf_calories'] / (exercise['duration_min']+1),
                })

            with open("activityList.json", "w") as f:
                json.dump(exercise_data, f, indent=2)
