
### Course Recommendation and Analytics System for Udemy Courses

#### Overview:

This Course Recommendation and Analytics System aims to provide insightful recommendations for users who are seeking courses on Udemy. Not only does it suggest courses tailored to the user's preference but it also provides an in-depth analysis on various metrics such as the number of subscribers per subject category, profit metrics, and course levels. 

#### Key Features:

1. **Course Recommendations**: 
   - Utilizes advanced algorithms to recommend courses based on user queries or chosen courses. 
   - Uses techniques like Cosine Similarity to find courses that are most similar to the user's interests.

2. **Data Extraction**:
   - Extracted data from Udemy, including course titles, URLs, prices, and the number of subscribers.

3. **Subscriber Analysis**:
   - Provides a breakdown of the number of subscribers enrolled per subject category.
   - Allows filtering by year and month to observe trends and seasonal fluctuations.

4. **Profit Analysis**:
   - Calculates the estimated profit earned by each course.
   - Provides 'Domain-wise' breakdown, helping educators and students to understand which subject areas are most profitable.

5. **Level Metrics**:
   - Gives an overview of the number of courses available for each difficulty level (Beginner, Intermediate, Advanced).
   - Helps users to understand the skill level most catered to in each domain.

#### Analytics Dashboard:

The system features an analytics dashboard offering:

- **Value Counts**: A graphical representation of various features like the number of courses in each category.
  
- **Level Counts**: A bar chart displaying the number of courses according to their level (Beginner, Intermediate, Advanced).

- **Subject per Level**: A nested bar chart representing the distribution of subjects within each course level.

- **Yearwise Profit Map**: A line graph showing the profit earned year-over-year.

- **Subscribers Count Map**: A heat map indicating the number of subscribers across various categories.

- **Monthly Profit and Subscribers**: Pie charts representing the distribution of profit and subscribers on a month-to-month basis.

#### Technologies Used:

- Python for data extraction and analytics.
- Flask for the backend.
- Pandas for data manipulation.
- Sklearn for machine learning algorithms.
- HTML, CSS, and JavaScript for the frontend.

By providing both recommendations and fundamental in-depth analytics, this system serves as a comprehensive tool looking to navigate the expansive world of Udemy courses.


### Screenshot
![Image text](/static/img/CourseRecommendationSystem.gif)


## Installation
***
A little intro about the installation.
```
$ git clone 
$ cd ../path/to/the/file
$ python -m venv env  ==== to create venv

$ .\venv\Scripts\Activate ==== to active env

$ flask run === on the app.py
```
Side information: The application is only tested in a ```window``` specific  environment