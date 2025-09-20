from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Use debug=False for production, True for development
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
