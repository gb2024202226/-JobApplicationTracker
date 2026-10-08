from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)


try:
    with open("applications.json", "r") as file:
        applications = json.load(file)

except FileNotFoundError:
    applications = []


try:
    with open("companies.json", "r") as file:
        companies = json.load(file)

except FileNotFoundError:
    companies = []


def prepare_applications(application_list):

    prepared = []

    for original_index, application in application_list:

        application_copy = application.copy()

        application_copy["original_index"] = original_index

        prepared.append(application_copy)

    return prepared


@app.route("/")
def home():

    total = len(applications)

    applied = 0
    interview = 0
    selected = 0
    rejected = 0

    for application in applications:

        status = application["status"].strip().lower()

        if status == "applied":
            applied += 1

        elif status == "interview":
            interview += 1

        elif status == "selected":
            selected += 1

        elif status == "rejected":
            rejected += 1

    if total > 0:

        selection_rate = round(
            (selected / total) * 100,
            2
        )

    else:

        selection_rate = 0


    indexed_applications = list(
        enumerate(applications)
    )

    recent_applications = sorted(
        indexed_applications,
        key=lambda item: item[1].get("date", ""),
        reverse=True
    )[:5]


    recent_applications = prepare_applications(
        recent_applications
    )


    return render_template(
        "home.html",
        total=total,
        applied=applied,
        interview=interview,
        selected=selected,
        rejected=rejected,
        selection_rate=selection_rate,
        recent_applications=recent_applications
    )


@app.route("/applications", methods=["GET", "POST"])
def application_page():

    if request.method == "POST":

        company = request.form["company"]
        role = request.form["role"]
        date = request.form["date"]
        status = request.form["status"]

        application = {
            "company": company,
            "role": role,
            "date": date,
            "status": status
        }

        applications.append(application)

        with open("applications.json", "w") as file:

            json.dump(
                applications,
                file,
                indent=4
            )

        return redirect("/applications")


    indexed_applications = list(
        enumerate(applications)
    )


    sorted_applications = sorted(
        indexed_applications,
        key=lambda item: item[1].get("date", ""),
        reverse=True
    )


    prepared = prepare_applications(
        sorted_applications
    )


    return render_template(
        "index.html",
        applications=prepared
    )


@app.route("/search")
def search():

    search_company = request.args.get(
        "company",
        ""
    ).strip().lower()

    results = []

    for index, application in enumerate(applications):

        if search_company in application["company"].lower():

            results.append(
                (index, application)
            )


    results = sorted(
        results,
        key=lambda item: item[1].get("date", ""),
        reverse=True
    )


    prepared = prepare_applications(
        results
    )


    return render_template(
        "index.html",
        applications=prepared,
        search_company=search_company
    )


@app.route("/filter")
def filter_applications():

    selected_status = request.args.get(
        "status",
        "All"
    )

    results = []


    if selected_status == "All":

        results = list(
            enumerate(applications)
        )


    else:

        for index, application in enumerate(applications):

            if application["status"].strip().lower() == selected_status.lower():

                results.append(
                    (index, application)
                )


    results = sorted(
        results,
        key=lambda item: item[1].get("date", ""),
        reverse=True
    )


    prepared = prepare_applications(
        results
    )


    return render_template(
        "index.html",
        applications=prepared
    )


@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit_application(index):

    if index < 0 or index >= len(applications):

        return redirect("/applications")


    if request.method == "POST":

        applications[index]["company"] = request.form["company"]

        applications[index]["role"] = request.form["role"]

        applications[index]["date"] = request.form["date"]

        applications[index]["status"] = request.form["status"]


        with open("applications.json", "w") as file:

            json.dump(
                applications,
                file,
                indent=4
            )


        return redirect("/applications")


    application = applications[index]


    return render_template(
        "edit.html",
        application=application,
        index=index
    )


@app.route("/update/<int:index>", methods=["POST"])
def update_status(index):

    if 0 <= index < len(applications):

        applications[index]["status"] = request.form["status"]


        with open("applications.json", "w") as file:

            json.dump(
                applications,
                file,
                indent=4
            )


    return redirect("/applications")


@app.route("/delete/<int:index>")
def delete_application(index):

    if 0 <= index < len(applications):

        applications.pop(index)


        with open("applications.json", "w") as file:

            json.dump(
                applications,
                file,
                indent=4
            )


    return redirect("/applications")


@app.route("/statistics")
def statistics():

    total = len(applications)

    applied = 0
    interview = 0
    selected = 0
    rejected = 0


    for application in applications:

        status = application["status"].strip().lower()


        if status == "applied":

            applied += 1

        elif status == "interview":

            interview += 1

        elif status == "selected":

            selected += 1

        elif status == "rejected":

            rejected += 1


    if total > 0:

        selection_rate = round(
            (selected / total) * 100,
            2
        )

    else:

        selection_rate = 0


    return render_template(
        "statistics.html",
        total=total,
        applied=applied,
        interview=interview,
        selected=selected,
        rejected=rejected,
        selection_rate=selection_rate
    )


@app.route("/eligibility", methods=["GET", "POST"])
def eligibility():

    if request.method == "POST":

        cgpa = float(
            request.form["cgpa"]
        )

        eligible_companies = []

        not_eligible_companies = []


        for company in companies:

            if cgpa >= company["cgpa"]:

                eligible_companies.append(company)

            else:

                not_eligible_companies.append(company)


        return render_template(
            "eligibility.html",
            cgpa=cgpa,
            eligible_companies=eligible_companies,
            not_eligible_companies=not_eligible_companies,
            companies=companies
        )


    return render_template(
        "eligibility.html",
        companies=companies
    )


@app.route("/add-company", methods=["POST"])
def add_company():

    company_name = request.form["company"]

    minimum_cgpa = float(
        request.form["cgpa"]
    )


    new_company = {
        "name": company_name,
        "cgpa": minimum_cgpa
    }


    companies.append(new_company)


    with open("companies.json", "w") as file:

        json.dump(
            companies,
            file,
            indent=4
        )


    return redirect("/eligibility")


@app.route("/delete-company/<int:index>")
def delete_company(index):

    if 0 <= index < len(companies):

        companies.pop(index)


        with open("companies.json", "w") as file:

            json.dump(
                companies,
                file,
                indent=4
            )


    return redirect("/eligibility")


@app.route("/about")
def about():

    return render_template("about.html")


if __name__ == "__main__":

    app.run(debug=True)