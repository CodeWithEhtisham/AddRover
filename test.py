from deepface import DeepFace as df

embed = None
try:
    embed = df.analyze('person_id_1.png', actions=["age", "gender"], detector_backend='yolov8')[0]
except:
    print("face not detected")

print(embed['age'], embed['dominant_gender'])