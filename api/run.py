from app import create_app
import os
# Create the application instance
app = create_app()

if __name__ == "__main__":
    # Run the app
    app.run(host="0.0.0.0", port=int(os.getenv("FLASK_PORT", 5000)))
