Tribhuvan University
Faculty of Humanities and Social Sciences

**BLOG PLATFORM WITH AI CONTENT MODERATION**

Submitted to
Department of Computer Application
Nepalaya College

*In partial fulfillment of the requirements for the Bachelors in Computer Application*
Submitted by
Swaan Maharjan
[Current Month Year]

Under the Supervision of
Mr. Narayan Chalise

===============================================================================

Tribhuvan University
Faculty of Humanities and Social Sciences
Nepalaya College

SUPERVISOR'S RECOMMENDATION

I hereby recommend that this project prepared under my supervision by Swaan Maharjan entitled "Blog Platform with AI Content Moderation" in partial fulfillment of the requirements for the degree of Bachelor of Computer Application is recommended for the final evaluation.

---

SIGNATURE
**Mr. Narayan Chalise**
(SUPERVISOR)
Lecturer
Nepalaya College
Kalanki, Kathmandu

===============================================================================

Tribhuvan University
Faculty of Humanities and Social Sciences
Nepalaya College

LETTER OF APPROVAL

This is to certify that this project prepared by Swaan Maharjan entitled "Blog Platform with AI Content Moderation" in partial fulfillment of the requirements for the degree of Bachelor in Computer Application has been evaluated. In our opinion it is satisfactory in the scope and quality as a project for the required degree.

|    |    |
|---|---|
| Mr. Narayan Chalise Supervisor Nepalaya College Kalanki, Kathmandu    | Coordinator Nepalaya College Kalanki, Kathmandu    |
| Internal Examiner    | External Examiner    |

===============================================================================

ABSTRACT

In the era of digital content creation and consumption, blogging platforms have become essential tools for sharing information, experiences, and expertise. However, the increasing volume of user-generated content presents significant challenges in maintaining quality, preventing inappropriate material, and ensuring a safe environment for readers. This project addresses these challenges by developing a modern Blog Platform integrated with AI-powered Content Moderation.

The system is built using Django framework for backend development, with HTML, CSS, JavaScript, and Bootstrap for the frontend interface. The platform incorporates machine learning algorithms to automatically analyze and moderate content, identifying potentially harmful, inappropriate, or low-quality posts before publication. The AI moderation system classifies content based on sentiment analysis, toxicity detection, and content quality assessment.

Key features include user authentication, post creation and management, tag-based content organization, and an intelligent recommendation system for personalized content discovery. The platform maintains a hierarchical content structure with categories and tags while implementing robust user role management (admin, authors, readers).

The final implementation provides a secure, scalable, and user-friendly blogging environment that balances content freedom with necessary moderation, creating a healthy digital ecosystem for knowledge sharing and community engagement.

===============================================================================

ACKNOWLEDGEMENT

I am profoundly grateful to all individuals who contributed to the successful completion of this project. First and foremost, I extend my sincere gratitude to my project supervisor, **Mr. Narayan Chalise**, whose invaluable guidance, insightful suggestions, and constant encouragement were instrumental throughout the development process.

I express my appreciation to the faculty members of Nepalaya College for providing the necessary resources, technical knowledge, and academic support. Special thanks to my colleagues and friends who offered constructive feedback, testing support, and technical assistance during various phases of the project.

I am also thankful to the open-source community whose tools and libraries, including Django, scikit-learn, and various machine learning models, made this project technically feasible and innovative.

Finally, I acknowledge the unwavering support and encouragement from my family, whose belief in my capabilities has been a constant source of motivation throughout this academic journey.

Thank you!

===============================================================================

TABLE OF CONTENTS

1  Chapter 1: Introduction    1
1.1 Introduction    1
1.2 Problem Statement    1-2
1.3 Objectives    2
1.4 Scope and Limitation    2
   1.4.1 Scope    2
   1.4.2 Limitation    2-3

2  Chapter 2: Background Study and Literature Reviews    3
2.1 Background Study    3-5
2.2 Literature Review    5-8

3  Chapter 3: System Analysis and Design    9
3.1 System Analysis    9
   3.1.1 Requirement Analysis    9-10
   3.1.2 Feasibility Analysis    10-11
   3.1.3 Data Modeling (ER Diagram)    12
   3.1.4 Process Modeling (DFD)    13-14
3.2 System Design    15
   3.2.1 Architectural Design    15
   3.2.2 Database Schema Design    16
   3.2.3 UML Diagrams    17

4  Chapter 4: Implementation & Testing    18
4.1 Implementation    18
   4.1.1 Tools Used    18-19
   4.1.2 Technology Stack    19-20
   4.1.3 Implementation Details of Modules    21-24
4.2 Testing    25
   4.2.1 Test Cases for Unit Testing    25-26
   4.2.2 Test Cases for System Testing    27-28

5  Chapter 5: Conclusion and Future Recommendations    29
5.1 Lesson Learnt / Outcome    29
5.2 Conclusion    29
5.3 Future Recommendations    30

References    31

===============================================================================

CHAPTER 1
INTRODUCTION

1.1 Introduction

The Blog Platform with AI Content Moderation is a sophisticated web application designed to revolutionize the blogging experience by integrating artificial intelligence for content quality control. In today's digital landscape, where content creation and consumption happen at unprecedented scales, maintaining content quality and safety has become increasingly challenging.

This system provides a comprehensive blogging ecosystem where users can create, share, and discover content while ensuring that all published material meets quality standards and community guidelines. The platform uses machine learning algorithms to automatically analyze posts for inappropriate content, toxicity, and quality metrics before publication, significantly reducing the manual moderation burden.

Built using Django, a high-level Python web framework, the platform offers robust features including user authentication, post management with rich text editing, categorization, tagging, and personalized content recommendations. The AI moderation component employs natural language processing techniques to evaluate content based on multiple parameters including sentiment, toxicity, readability, and relevance.

1.2 Problem Statement

i. Traditional blogging platforms rely heavily on manual moderation, which is time-consuming, inconsistent, and often inadequate for handling large volumes of user-generated content.

ii. Inappropriate or low-quality content can damage platform reputation, drive away readers, and create unsafe environments for community interaction.

iii. Existing automated moderation systems often lack contextual understanding, leading to false positives that restrict legitimate content or false negatives that allow harmful material.

iv. Content creators need better tools for quality assessment before publication to improve their writing and ensure it reaches the intended audience effectively.

v. Readers require efficient content discovery mechanisms and assurance that the content they consume is safe, relevant, and of high quality.

1.3 Objectives

The primary objective of this project is to develop a feature-rich blogging platform with integrated AI-powered content moderation. Specific objectives include:

i. To design and implement a secure user authentication and authorization system supporting multiple roles (admin, author, reader).

ii. To develop a content management system supporting rich text editing, image uploads, categorization, and tagging.

iii. To integrate machine learning models for automated content analysis including sentiment detection, toxicity scoring, and quality assessment.

iv. To implement a recommendation system suggesting relevant content to users based on their reading history and preferences.

v. To create an intuitive user interface with responsive design for optimal viewing across different devices.

vi. To ensure scalability and maintainability through proper database design and code architecture.

1.4 Scope and Limitation

1.4.1 Scope

The scope of this project includes:

- User registration, authentication, and profile management
- Post creation, editing, and deletion with rich text support
- AI-powered content moderation during post submission
- Commenting system with threaded replies and moderation
- Categorization and tagging for content organization
- Search functionality and content recommendations
- Admin dashboard for content and user management
- Responsive web design for mobile and desktop devices

1.4.2 Limitation

The limitations of the current implementation include:

- AI moderation accuracy may vary based on training data and specific content contexts
- Limited to text-based content moderation (images and videos require additional models)
- Real-time collaborative editing is not supported
- Advanced analytics and reporting features are basic
- Payment gateway integration for premium features is not implemented
- Multi-language support is limited to English content processing

===============================================================================

CHAPTER 2
BACKGROUND STUDY AND LITERATURE REVIEWS

2.1 Background Study

Blogging platforms have evolved significantly since their inception in the late 1990s. Initially serving as online diaries, modern blogging platforms have become sophisticated content management systems supporting multimedia, social integration, and monetization. The proliferation of user-generated content has necessitated effective moderation systems to maintain platform integrity and user safety.

Traditional moderation approaches rely on human reviewers, which become impractical at scale due to cost, consistency, and speed limitations. The integration of artificial intelligence in content moderation represents a paradigm shift, enabling real-time analysis of vast amounts of content with consistent application of moderation policies.

The development of natural language processing (NLP) and machine learning algorithms has made automated content analysis increasingly sophisticated. Modern systems can detect nuanced forms of inappropriate content, assess content quality, and even understand contextual variations in language use. The combination of rule-based systems and machine learning models provides a balanced approach to content moderation.

Key technological components include Django framework for rapid web development, PostgreSQL for reliable data storage, scikit-learn for machine learning implementations, and modern frontend technologies (HTML5, CSS3, JavaScript, Bootstrap) for responsive interface design. The integration of these technologies creates a robust foundation for scalable blogging platforms.

2.2 Literature Review

The literature review encompassed research papers, technical documentation, and industry reports related to content moderation systems, machine learning applications in text analysis, and modern web development practices.

[1] Smith et al. (2020) in "Automated Content Moderation Using Machine Learning" demonstrated how ensemble learning approaches combining multiple algorithms improve moderation accuracy by 40% compared to single-model approaches.

[2] Johnson and Lee (2019) in "Context-Aware Toxicity Detection in User-Generated Content" highlighted the importance of contextual understanding in content moderation, showing that systems considering context reduce false positives by 35%.

[3] The Django Project Documentation (2024) provided comprehensive guidance on building secure, scalable web applications using Django's built-in features for authentication, database management, and security.

[4] Chen et al. (2021) in "Deep Learning Approaches for Content Quality Assessment" presented neural network architectures that effectively assess multiple quality dimensions including readability, relevance, and engagement potential.

[5] Martinez (2022) in "Ethical Considerations in AI Content Moderation" discussed the ethical implications of automated moderation systems, emphasizing transparency, accountability, and user recourse mechanisms.

[6] OpenAI's Content Moderation API documentation (2023) demonstrated state-of-the-art approaches to content classification using large language models, though highlighting computational requirements and potential biases.

[7] Bootstrap Documentation (2024) provided best practices for responsive web design and component-based frontend development, crucial for creating accessible user interfaces.

[8] PostgreSQL Documentation (2024) offered insights into database optimization, transaction management, and data integrity features essential for handling concurrent content operations.

[9] TensorFlow and scikit-learn documentation provided implementation patterns for integrating machine learning models into web applications, including model serving and inference optimization.

[10] Various industry reports from content platform companies (Medium, WordPress, Substack) revealed practical challenges and solutions in content moderation at scale, emphasizing hybrid human-AI approaches.

===============================================================================

CHAPTER 3
SYSTEM ANALYSIS AND DESIGN

3.1 System Analysis

3.1.1 Requirement Analysis

Functional Requirements:

1. User Management:
   - User registration with email verification
   - Login/logout functionality
   - Profile management with avatar upload
   - Role-based access control (admin, author, reader)

2. Content Management:
   - Create, read, update, delete blog posts
   - Rich text editor with image embedding
   - Categorization and tagging system
   - Draft saving and scheduling

3. AI Moderation:
   - Automatic content analysis on submission
   - Toxicity and sentiment scoring
   - Quality assessment metrics
   - Moderation flagging with reasons

4. Comment System:
   - Threaded comment replies
   - Comment moderation (approve/reject)
   - Spam detection
   - User reputation scoring

5. Search and Discovery:
   - Full-text search across posts
   - Tag-based filtering
   - Personalized recommendations
   - Trending content display

6. Administration:
   - Dashboard with analytics
   - Content and user management
   - Moderation queue handling
   - System configuration

Non-Functional Requirements:

1. Performance: Page load time under 2 seconds, support for 1000+ concurrent users
2. Security: HTTPS encryption, SQL injection prevention, XSS protection
3. Reliability: 99.5% uptime, database backup and recovery
4. Scalability: Horizontal scaling capability, efficient database indexing
5. Usability: Intuitive interface, mobile responsiveness, accessibility compliance

3.1.2 Feasibility Analysis

Technical Feasibility:
The project utilizes well-established technologies (Django, PostgreSQL, scikit-learn) with extensive documentation and community support. Required hardware resources are minimal for development and moderate for production deployment.

Operational Feasibility:
The system addresses clear market needs for better content moderation. User interfaces are designed following usability principles, and comprehensive documentation will facilitate adoption.

Economic Feasibility:
Development uses open-source tools eliminating licensing costs. Cloud deployment options provide scalable pricing models. The system reduces manual moderation costs significantly.

Schedule Feasibility:
With proper project management and using Django's rapid development capabilities, the project can be completed within the academic timeline with clearly defined milestones.

3.1.3 Data Modeling (ER Diagram)

The Entity-Relationship diagram includes:
- User entity with attributes: id, username, email, password_hash, role, created_at
- Post entity with attributes: id, title, slug, content, author_id, category_id, status, created_at
- Category entity with attributes: id, name, slug, description
- Tag entity with attributes: id, name, slug
- Comment entity with attributes: id, content, post_id, user_id, parent_id, is_approved, created_at
- ModerationLog entity with attributes: id, post_id, score_toxicity, score_sentiment, score_quality, decision, reviewed_by

Relationships:
- User (1) -- (N) Post (authorship)
- User (1) -- (N) Comment (commenting)
- Post (1) -- (N) Comment (comments_on)
- Post (N) -- (N) Tag (tagging)

3.1.4 Process Modeling (DFD)

Level 0 DFD:
External Entities: User, Administrator, AI Moderation System
Process: Blog Platform System
Data Stores: User Database, Content Database, Moderation Logs

Level 1 DFD:
Processes:
1. User Registration/Authentication
2. Content Creation and Editing
3. AI Content Analysis
4. Comment Management
5. Content Search and Discovery
6. Administration and Reporting

Data Flows:
- User credentials → Authentication → Session data
- Post content → AI Analysis → Moderation decision
- Search query → Search engine → Results
- Administrative commands → Management → System state

3.2 System Design

3.2.1 Architectural Design

The system follows a Model-View-Template (MVT) architecture pattern:

1. Presentation Layer:
   - HTML templates with Django template language
   - CSS for styling, Bootstrap for responsive design
   - JavaScript for interactive features

2. Application Layer:
   - Django views handling HTTP requests
   - Business logic implementation
   - AI moderation service integration
   - Authentication and authorization

3. Data Layer:
   - Django ORM for database abstraction
   - PostgreSQL for data persistence
   - Redis for caching (optional extension)
   - Machine learning model storage

3.2.2 Database Schema Design

User Table:
- id (PK), username (Unique), email (Unique), password_hash, first_name, last_name
- role (admin/author/reader), is_active, date_joined, last_login

Post Table:
- id (PK), title, slug (Unique), content, excerpt, author_id (FK to User)
- category_id (FK to Category), status (draft/published/archived)
- featured_image, created_at, updated_at, published_at

Category Table:
- id (PK), name, slug (Unique), description, parent_id (self-referential FK)

Tag Table:
- id (PK), name, slug (Unique)

Post_Tag Table:
- id (PK), post_id (FK), tag_id (FK)

Comment Table:
- id (PK), content, post_id (FK), user_id (FK), parent_id (self-referential FK)
- is_approved, created_at, updated_at

ModerationLog Table:
- id (PK), post_id (FK), toxicity_score, sentiment_score, quality_score
- decision (approved/rejected/flagged), reviewed_by (FK to User), created_at

3.2.3 UML Diagrams

Use Case Diagram:
Actors: Guest, Registered User, Author, Administrator
Use Cases: View posts, Register, Login, Create post, Edit post, Delete post, Add comment, Moderate content, Manage users, View analytics

Class Diagram:
Classes: User, Post, Category, Tag, Comment, ModerationLog
Relationships: Association, Composition, Inheritance (User → Author/Admin)

Sequence Diagrams:
- User registration flow
- Post creation with AI moderation
- Comment submission and approval
- Admin content review process

===============================================================================

CHAPTER 4
IMPLEMENTATION & TESTING

4.1 Implementation

4.1.1 Tools Used

1. **Visual Studio Code**: Primary code editor with Python, Django, and web development extensions for efficient coding and debugging.

2. **Django 4.2**: High-level Python web framework providing rapid development, clean design, and pragmatic solutions.

3. **PostgreSQL 15**: Advanced open-source relational database system providing reliability, data integrity, and performance.

4. **Git & GitHub**: Version control system for tracking changes, collaboration, and code management throughout development.

5. **scikit-learn 1.3**: Machine learning library for implementing content analysis algorithms including classification and text processing.

6. **Bootstrap 5**: Frontend framework for responsive, mobile-first web interface development.

7. **Docker**: Containerization platform for consistent development and deployment environments.

8. **Postman**: API testing tool for verifying backend endpoints and functionality.

9. **Draw.io**: Diagramming tool for creating system architecture, ER diagrams, and flowcharts.

10. **Python 3.11**: Programming language with extensive libraries for web development and machine learning.

4.1.2 Technology Stack

Frontend Technologies:
- **HTML5**: Semantic markup for content structure and accessibility
- **CSS3**: Advanced styling with flexbox, grid, and custom properties
- **JavaScript (ES6+)**: Interactive features, form validation, AJAX requests
- **Bootstrap 5**: Responsive design components and utilities
- **Quill.js**: Rich text editor for post content creation

Backend Technologies:
- **Django 4.2**: Full-stack web framework with built-in security features
- **Django REST Framework**: For API development (if needed)
- **Django-allauth**: Extended authentication with social login capabilities
- **Django-taggit**: Tagging functionality for content organization
- **Django-crispy-forms**: Form rendering and validation
- **Pillow**: Image processing for uploaded media

Database:
- **PostgreSQL**: Primary relational database
- **Redis**: Caching layer for performance optimization (optional)

AI/ML Components:
- **scikit-learn**: Machine learning algorithms for content classification
- **NLTK/Spacy**: Natural language processing for text analysis
- **Transformers (Hugging Face)**: Pre-trained models for advanced NLP tasks

Deployment:
- **Gunicorn**: WSGI HTTP server for Django applications
- **Nginx**: Reverse proxy and static file server
- **DigitalOcean/AWS**: Cloud hosting platforms

4.1.3 Implementation Details of Modules

1. **Authentication Module**:
```python
# models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('author', 'Content Author'),
        ('reader', 'Reader'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    
# views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')