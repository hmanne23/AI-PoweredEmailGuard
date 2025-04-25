from main import db, User

# 🔁 Change this username to the one you want to delete
username_to_delete = "example_username"

user = User.query.filter_by(username=username_to_delete).first()

if user:
    db.session.delete(user)
    db.session.commit()
    print(f"✅ User '{username_to_delete}' deleted successfully.")
else:
    print(f"❌ User '{username_to_delete}' not found.")