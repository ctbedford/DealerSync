# DealerSync

## 📋 Project Overview

DealerSync is a comprehensive web application for managing vehicle listings. It comprises a frontend developed with React and a backend built using Django. The backend includes Django applications for authentication, data scraping, and dashboard functionalities. The frontend integrates Tailwind CSS for styling.

## 🗂️ Project Structure

Backend (Django)

    dealer_sync_backend: Main project directory containing settings and configuration files.
    authentication: Handles user registration and authentication.
    scraper: Manages the scraping tasks and vehicle listings.
    dashboard: Provides dashboard views and API endpoints.

Frontend (React)

    dealer_sync_frontend: Main directory for the React frontend.
    public: Contains public assets like images and the index.html.
    src: Contains the source code for the React application, including components, views, and styles.
    mocks: Mock files for testing.

## 📂 Directory Breakdown

Backend

    dealer_sync_backend
        __init__.py
        settings.py
        urls.py
        wsgi.py
        asgi.py
        celery.py

    authentication
        admin.py
        apps.py
        models.py
        serializers.py
        urls.py
        views.py
        tests.py

    scraper
        admin.py
        apps.py
        models.py
        serializers.py
        urls.py
        views.py
        tasks.py
        tests.py
        management/commands
            check_database.py

    dashboard
        admin.py
        apps.py
        models.py
        serializers.py
        urls.py
        views.py
        tests.py

Frontend

    dealer_sync_frontend
        package.json
        package-lock.json
        tailwind.config.js
        babel.config.js
        public
            index.html
            manifest.json
            favicon.ico
            logo192.png
            logo512.png
        src
            index.js
            App.js
            App.css
            components
                Card.js
                CardHeader.js
                CardTitle.js
                CardContent.js
                Layout.js
                ProtectedRoute.js
            views
                Dashboard.js
                Listings.js
                Auth.js
                Sync.js
            styles
                index.css
                Dashboard.css
            tests
                setupTests.js
                Sync.test.js
                Dashboard.test.js
                Auth.test.js
            images
                default-vehicle.webp
                logo.svg

## ⚙️ Key Features

Backend

    Authentication: User registration, login, and token-based authentication using Django REST Framework and SimpleJWT.
    Scraping: Celery tasks for scraping vehicle listings from various sources.
    Dashboard: API endpoints providing statistics and recent activity data.

Frontend

    React: Single-page application for managing and viewing vehicle listings.
    Tailwind CSS: Responsive design and custom themes.
    Axios: For making API requests to the backend.
    React Router: Navigation and protected routes.

## 🚀 Getting Started

Prerequisites

    Python 3.x
    Node.js and npm
    PostgreSQL
    Redis (for Celery)

Backend Setup

    Clone the repository:

    bash

git clone <repository-url>
cd dealer_sync_backend

Create a virtual environment:

bash

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

Install dependencies:

bash

pip install -r requirements.txt

Set up environment variables:
Create a .env file with the required variables:

makefile

POSTGRES_DB=<your_db>
POSTGRES_USER=<your_user>
POSTGRES_PASSWORD=<your_password>
DATABASE_HOST=localhost
DATABASE_PORT=5432

Run migrations:

bash

python manage.py migrate

Start the development server:

bash

    python manage.py runserver

Frontend Setup

    Navigate to the frontend directory:

    bash

cd dealer_sync_frontend

Install dependencies:

bash

npm install

Start the development server:

bash

    npm start

🧪 Running Tests
Backend Tests

Run Django tests:

bash

python manage.py test

Frontend Tests

Run React tests:

bash

npm test

📄 License

This project is licensed under the MIT License.
📞 Contact

For any inquiries or feedback, please contact tybed7@icloud.com.


## TODO

To get your DealerSync project hosted and working online quickly, AWS (Amazon Web Services) is a good choice due to its comprehensive services and scalability. Here's a high-level overview of the steps you'd need to take to deploy your project on AWS:

1. Set up AWS account:
   - Create an AWS account if you don't have one already.

2. Set up a Virtual Private Cloud (VPC):
   - Create a VPC to isolate your resources.

3. Database setup:
   - Use Amazon RDS for PostgreSQL to host your database.

4. Backend deployment:
   - Use Elastic Beanstalk for deploying your Django backend.

5. Frontend deployment:
   - Use S3 and CloudFront for hosting your React frontend.

6. Task queue:
   - Use Amazon ElastiCache for Redis to support Celery.

7. Domain and SSL:
   - Use Route 53 for domain management and ACM for SSL certificates.

Here's a more detailed step-by-step guide:

1. Set up AWS account:
   - Go to aws.amazon.com and sign up for an account.
   - Set up IAM users and groups for secure access.

2. Set up VPC:
   - In the AWS Console, go to VPC service.
   - Create a new VPC with public and private subnets.

3. Database setup:
   - Go to RDS in the AWS Console.
   - Launch a new PostgreSQL instance.
   - Make sure it's in the private subnet of your VPC.
   - Note down the endpoint, username, and password.

4. Backend deployment:
   - Install the Elastic Beanstalk CLI on your local machine.
   - In your Django project, create an `.ebextensions` folder with configuration files.
   - Update your `settings.py` to use environment variables for sensitive data.
   - Run `eb init` to initialize your EB application.
   - Run `eb create` to create an environment and deploy your application.
   - Set environment variables in the EB console for database credentials, etc.

5. Frontend deployment:
   - Create an S3 bucket for your frontend files.
   - Enable static website hosting on the bucket.
   - Build your React app (`npm run build`).
   - Upload the build files to the S3 bucket.
   - Create a CloudFront distribution pointing to the S3 bucket.

6. Task queue setup:
   - Create an ElastiCache Redis cluster.
   - Update your Celery configuration to use the Redis cluster.

7. Domain and SSL:
   - Register a domain in Route 53 (or transfer an existing one).
   - Request an SSL certificate in ACM.
   - Update your CloudFront distribution to use the SSL certificate.
   - Create Route 53 records to point your domain to the CloudFront distribution and Elastic Beanstalk environment.

8. Final configuration:
   - Update your frontend code to use the new backend URL.
   - Rebuild and redeploy your frontend.

9. Continuous Integration/Continuous Deployment (CI/CD):
   - Set up AWS CodePipeline to automate deployments.
   - Connect it to your GitHub repository.

10. Monitoring and logging:
    - Set up CloudWatch for monitoring and logging.
    - Configure alarms for important metrics.

This process will give you a scalable, production-ready setup for your DealerSync project. However, it's quite complex and can take some time to set up correctly, especially if you're new to AWS.

For a quicker, simpler deployment (though less scalable), you could consider alternatives:

1. Heroku: Easier to set up, supports both Django and React apps, and provides a PostgreSQL database. However, it can be more expensive as you scale.

2. DigitalOcean App Platform: Simpler than AWS, supports Django and static site hosting for your React app.

3. Python Anywhere: Very easy to set up for Django projects, but you'd need to host your React frontend elsewhere (like Netlify or Vercel).

These alternatives sacrifice some scalability and control for ease of use, which might be a good trade-off for getting your project online quickly. Once you're live and need more control or specific AWS services, you can always migrate to a full AWS setup later.