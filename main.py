from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

link_map = {
    "Recruitment": "https://platform.draup.com/draup/recruitment",
    "Reskill Navigator": "https://platform.draup.com/draup/reskilling/reskillnavigator",
    "Braindesk sales": "https://platform.draup.com/draup/braindesk",
    "My Accounts": "https://platform.draup.com/draup/home",
}

with open('data_latest.json') as f:
    data = json.load(f)

# roles = {'HR': ['Recruitment', 'jd', 'attrition'],
#          'L&D': ['Reskill Navigator'],
#          'Sales': ['competitor', 'Braindesk sales', 'My Accounts'],
#          'Analyst': ['Braindesk sales', 'My Accounts']}


def parse_feature_text(text):
    text = text.replace("\n", "<br>")
    return {"html": "<html>" + text + "</html>"}


def add_link(input_string):
    link = "https://platform.draup.com/draup/"
    pattern = r'(.*?):<br>(.+?)<br>+'

    # Use re.findall to find all matches in the text
    matches = re.findall(pattern, input_string, re.DOTALL)
    for match in matches:
        feature_name = match[0].strip()
        feature_name_modified = feature_name.replace('<html>', '').replace('</html>', '').replace('<br>', '')
        print(feature_name_modified)
        print(link_map[feature_name_modified])
        desc = match[1].strip()
        input_string = re.sub(feature_name, f"<a href={link_map[feature_name_modified]}\>{feature_name}</a>", input_string)
    return input_string


def find_map(company_name, job_title):
    feature = None

    for doc in data:
        try:
            if company_name.lower() in doc.get("Account").lower():
                if job_title.lower() == "hr":
                    feature = parse_feature_text(doc.get("HR_recommendations"))
                elif job_title.lower() == "sales":
                    feature = parse_feature_text(doc.get("Sales_recommendations"))
                elif job_title.lower() == "l&d":
                    feature = parse_feature_text(doc.get("L&D_recommendations"))
                else:
                    feature = parse_feature_text(doc.get("Analyst_recommendations"))

                if feature:
                    modified_html = add_link(feature["html"])
                    feature["html"] = modified_html
                    break
        except:
            print("Error parsing document")
            continue

    return feature


@app.route('/get_feature', methods=['POST'])
def process_data():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'no data found'})
    company_name = data.get("company_name", "")
    job_title = data.get("job_title", "")
    resp = find_map(company_name, job_title)
    return jsonify({'features': resp})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
