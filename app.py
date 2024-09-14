from flask import Flask, request, render_template
import pickle
import pandas as pd
app = Flask(__name__)
medicine_dict = pickle.load(open('medicine_dict.pkl','rb'))
medicines = pd.DataFrame(medicine_dict)
similarity=pickle.load(open('similarity.pkl','rb'))


def recommend(medicine):
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    # Get a sorted list of medicines based on similarity
    medicine_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)

    recommended_medicines = []

    # Select top 5 medicines (excluding the input medicine itself)
    for i in medicine_list[1:6]:  # Start from index 1 to skip the input medicine
        recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)

    return recommended_medicines


@app.route('/', methods=['GET',"POST"])

def index():
    recommendations=[]
    selected_medicine_name = None
    if request.method == 'POST':
        selected_medicine_name = request.form['medicine']
        recommendations = recommend(selected_medicine_name)
    return render_template('index.html',medicines=medicines['Drug_Name'].values,recommendations=recommendations,selected_medicine_name=selected_medicine_name)

if __name__ == '__main__':
    app.run(debug=True)
