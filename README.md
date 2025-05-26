# Django Web Development Learning Journey

This repository documents my progress through a structured Django web development curriculum,  
where I built progressively more complex applications while mastering both fundamental and advanced concepts.

## Technical Scope

Starting with **core web technologies**, I implemented responsive layouts using **HTML5 and CSS**,  
then advanced to **form handling** with client-side validation and server-side processing.  
The projects demonstrate my **Django framework** proficiency, including the Model-View-Template (MVT) pattern,  
database design with the **Django ORM**, and efficient routing with **generic class-based views**.

For **backend functionality**, I developed secure **user authentication systems**, robust **CRUD interfaces** with relational data,  
and media management features like **image uploads and processing**.  
The later assignments involved **integrating external APIs**, generating dynamic **data visualizations**,  
and optimizing the **Django admin panel** for content management.

---
Temporory link to the website: 
1. https://cs-webapps.bu.edu/miclilzy/quotes/: Randomly displaying Aryton Senna's famous quotes with pictures
2. https://cs-webapps.bu.edu/miclilzy/restaurant/: An online ordering website for Boba Tea shop
3. https://cs-webapps.bu.edu/miclilzy/mini_fb/: An social media website restores all the key functions of facebook

---

# F1 Explorer: A Formula 1 Fan Community Platform

## Project Overview

**F1 Explorer** is a full-stack Django web application designed for Formula 1 enthusiasts to explore circuits, share insights, and connect with other fans. Inspired by Yelp-style review platforms but tailored for motorsport, it combines interactive maps, user-generated content, and community features to create an engaging experience for racing fans.
---
Temporory link to the website: https://cs-webapps.bu.edu/miclilzy/circuits/
---

## Key Features

### 🏁 Circuit Exploration

- **Interactive Map Interface**:  
  Browse all F1 circuits geographically without needing an account.

  <img width="1511" alt="截屏2025-05-26 下午4 38 00" src="https://github.com/user-attachments/assets/bb29ce47-fbd9-4826-9d75-098f242e7593" />


- **Detailed Circuit Profiles**:  
  View track layouts, historical statistics, fun facts, and technical specifications.

  <img width="1511" alt="截屏2025-05-26 下午4 38 07" src="https://github.com/user-attachments/assets/37574bb5-f3ff-4fde-8bc4-50d5faf06dd0" />


- **Smart Search**:  
  Filter circuits by name or geographical region.

---

### Community Interactions

- **User Reviews & Ratings**:  
  Share comments and rate circuits (login required).

- **Lap Time Tracking**:  
  Contribute and compare 2024 season lap times.

- **Dynamic Leaderboards**:  
  See how your quiz scores stack up against the community.

  <img width="1512" alt="截屏2025-05-26 下午4 46 39" src="https://github.com/user-attachments/assets/abeb0393-46e5-41f2-97b3-f98eefb110f3" />



---

### Gamification Elements

- **Interactive Quiz System**:  
  Tests your F1 knowledge with randomly selected questions from a pool of 25–30 items.

- **Personal Achievement Tracking**:  
  View your quiz history, submitted lap times, and circuit reviews in your profile.

---

### User Management

<img width="1512" alt="截屏2025-05-26 下午4 44 28" src="https://github.com/user-attachments/assets/dca69e08-a3b3-4e14-b063-ab8eef2ca0a2" />


- **Secure Authentication**:  
  Create accounts and manage profiles.

- **Personal Dashboard**:  
  Edit your profile, track your contributions, and manage your content.

- **Content Moderation**:  
  Edit or delete your own comments and lap times.

## Technical Implementation

---

### Backend Architecture

The application follows Django's **Model-View-Template (MVT)** pattern with a **PostgreSQL** database. Key backend components include:

- **Custom Models**  
  Designed relational schemas for circuits, user profiles, comments, lap times, and quiz systems.  
  Features include:
  - Proper foreign key constraints  
  - Custom field validations (e.g., regex-based lap time format validation)

- **Authentication Flow**  
  Implemented Django’s built-in auth system:
  - Extended `User` model via `Profile`
  - Secure password hashing
  - Session-based login/logout flow

- **Dynamic Querying**  
  Utilized powerful Django ORM methods:
  - `annotate()`, `aggregate()`, `select_related()`  
  - Examples: Average circuit ratings, efficient quiz history retrieval

- **Class-Based Views (CBVs)**  
  Reused generic views:
  - `ListView`, `DetailView`, `UpdateView`
  - Integrated `LoginRequiredMixin` for access control

---

### Frontend Integration

- **Interactive Maps**  
  Integrated **Leaflet.js** into Django templates:  
  - GeoJSON data rendered dynamically  
  - Context-passed location data for real-time mapping

- **Responsive Design (Bootstrap 5)**  
  - Custom dark theme for branding  
  - Toast messages for real-time feedback  
  - Mobile-optimized navigation

- **Template Inheritance**  
  - `base.html` contains shared structure (navbar, CSS/JS)  
  - `{% block %}` structure for page-specific overrides

---

### Key Features

- **Real-Time Leaderboards**  
  - Quiz attempts ranked using `order_by()` on combined score and completion time  

- **Concurrent Data Handling**  
  - Atomic transactions ensure consistency in:
    - Lap time submissions  
    - Quiz attempts  

- **Admin Customization**  
  - Extended Django Admin:
    - Inline editing of user content  
    - Filters, search bars for quick access to models

---

### 🚀 Optimizations

- **Database Query Efficiency**  
  - Used `select_related()` and `prefetch_related()` to prevent N+1 query issues

- **Form Validation**  
  - Paired client-side JS checks with server-side validation for robust data protection

- **Scalable Task Processing**  
  - Integrated **Celery** task queue (planned)  

