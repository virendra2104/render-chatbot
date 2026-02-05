from .gsheet_helper import add_registration

def register_user(user_data: dict):
    try:
        add_registration(
            name=user_data.get("name"),
            phone=user_data.get("phone"),
            email=user_data.get("email"),
            course=user_data.get("course")
        )
        return "Registration successful ✅"
    except Exception as e:
        # print the full exception
        print("Error in Google Sheets:", e)
        return f"Registration failed ❌ Error: {e}"
