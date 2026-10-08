import json

# Load saved applications
try:
    with open("applications.json", "r") as file:
        applications = json.load(file)
except FileNotFoundError:
    applications = []


while True:

    print()
    print("================================")
    print("      JOB APPLICATION TRACKER")
    print("================================")
    print("1. Add Application")
    print("2. View Applications")
    print("3. Search Application")
    print("4. Update Application Status")
    print("5. Edit Company Name")
    print("6. Delete Application")
    print("7. Application Statistics")
    print("8. Exit")

    choice = input("Enter your choice: ")


    # ---------------- ADD ----------------
    if choice == "1":

        print()
        print("----- ADD APPLICATION -----")

        company = input("Enter company name: ")
        role = input("Enter job role: ")
        status = input("Enter application status: ")

        application = {
            "company": company,
            "role": role,
            "status": status
        }

        applications.append(application)

        with open("applications.json", "w") as file:
            json.dump(applications, file, indent=4)

        print("Application added successfully! ✅")


    # ---------------- VIEW ----------------
    elif choice == "2":

        print()
        print("----- ALL APPLICATIONS -----")

        if len(applications) == 0:
            print("No applications found.")

        else:
            for i, application in enumerate(applications, start=1):

                print()
                print("Application", i)
                print("Company:", application["company"])
                print("Role:", application["role"])
                print("Status:", application["status"])
                print("---------------------------")


    # ---------------- SEARCH ----------------
    elif choice == "3":

        print()
        print("----- SEARCH APPLICATION -----")

        search_company = input("Enter company name to search: ")

        found = False

        for application in applications:

            if application["company"].lower() == search_company.lower():

                print()
                print("Application Found! ✅")
                print("Company:", application["company"])
                print("Role:", application["role"])
                print("Status:", application["status"])

                found = True

        if found == False:
            print("No application found for this company.")


    # ---------------- UPDATE STATUS ----------------
    elif choice == "4":

        print()
        print("----- UPDATE APPLICATION STATUS -----")

        search_company = input("Enter company name: ")

        found = False

        for application in applications:

            if application["company"].lower() == search_company.lower():

                print("Current status:", application["status"])

                new_status = input("Enter new status: ")

                application["status"] = new_status

                found = True

                print("Status updated successfully! ✅")

        if found == False:
            print("No application found for this company.")

        with open("applications.json", "w") as file:
            json.dump(applications, file, indent=4)


    # ---------------- EDIT COMPANY ----------------
    elif choice == "5":

        print()
        print("----- EDIT COMPANY NAME -----")

        old_company = input("Enter current company name: ")

        found = False

        for application in applications:

            if application["company"].lower() == old_company.lower():

                print("Current company:", application["company"])

                new_company = input("Enter new company name: ")

                application["company"] = new_company

                found = True

                print("Company name updated successfully! ✅")

        if found == False:
            print("No application found for this company.")

        with open("applications.json", "w") as file:
            json.dump(applications, file, indent=4)


    # ---------------- DELETE ----------------
    elif choice == "6":

        print()
        print("----- DELETE APPLICATION -----")

        if len(applications) == 0:
            print("No applications to delete.")

        else:

            for i, application in enumerate(applications, start=1):

                print(
                    i,
                    "-",
                    application["company"],
                    "|",
                    application["role"],
                    "|",
                    application["status"]
                )

            number = int(input("Enter application number to delete: "))

            if number >= 1 and number <= len(applications):

                deleted_application = applications.pop(number - 1)

                with open("applications.json", "w") as file:
                    json.dump(applications, file, indent=4)

                print()
                print(
                    deleted_application["company"],
                    "application deleted successfully! 🗑️"
                )

            else:
                print("Invalid application number.")


    # ---------------- STATISTICS ----------------
    elif choice == "7":

        print()
        print("===== APPLICATION STATISTICS =====")

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

        print()
        print("Total Applications :", total)
        print("Applied             :", applied)
        print("Interview           :", interview)
        print("Selected            :", selected)
        print("Rejected            :", rejected)


    # ---------------- EXIT ----------------
    elif choice == "8":

        print()
        print("Thank you for using Job Application Tracker! 👋")
        break


    else:

        print()
        print("Invalid choice. Please enter 1 to 8.")