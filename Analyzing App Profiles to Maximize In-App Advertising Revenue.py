#!/usr/bin/env python
# coding: utf-8

# # Analyzing App Profiles to Maximize In-App Advertising Revenue
# 

# In this project, we will explore data to help our company, which develops Android and iOS mobile apps, understand which types of apps are likely to attract the most users. Since our revenue is primarily generated through in-app ads, understanding user preferences and trends is crucial. By analyzing app profiles from Google Play and the App Store, we aim to identify the categories of apps that have the potential to engage the largest audiences.
# 
# Our ultimate goal is to provide data-driven insights to guide our developers in creating apps that align with user interests and maximize our company's revenue. This project will not only demonstrate our ability to analyze real-world data but also showcase our proficiency in using Python for practical data analysis tasks.

# # Opening and Exploring the Data

# In[1]:


import csv

# Opening the AppleStore.csv dataset
with open('AppleStore.csv', encoding='utf8') as file:
    ios_apps = list(csv.reader(file))

# Opening the googleplaystore.csv dataset
with open('googleplaystore.csv', encoding='utf8') as file:
    android_apps = list(csv.reader(file))


# In[2]:


# Defining the explore_data() function as provided
def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row
    
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

# Exploring the first few rows of the iOS dataset
print("First few rows of the iOS dataset:")
explore_data(ios_apps, 0, 5, rows_and_columns=True)

# Exploring the first few rows of the Android dataset
print("First few rows of the Android dataset:")
explore_data(android_apps, 0, 5, rows_and_columns=True)


# In[3]:


# Printing the header row for the iOS dataset
ios_header = ios_apps[0]
print("iOS dataset column names:")
print(ios_header)
#removing the header row from the the ios_apps
ios_apps = ios_apps[1:]
# Number of ios rows excluding the header 
print("Number of ios rows excluding the header")
print(len(ios_apps))

# Printing the header row for the Android dataset
android_header = android_apps[0]
print("\nAndroid dataset column names:")
print(android_header)
#removing the header row from the the android_apps
android_apps = android_apps[1:]

# Number of android rows excluding the header 
print("Number of android rows excluding the header")
print(len(android_apps))


# We see that the Google Play data set has 10841 apps and 13 columns. At a quick glance, the columns that might be useful for the purpose of our analysis are 'App', 'Category', 'Reviews', 'Installs', 'Type', 'Price', and 'Genres'.
# 
# We have 7197 iOS apps in this data set, and the columns that seem interesting are: 'track_name', 'currency', 'price', 'rating_count_tot', 'rating_count_ver', and 'prime_genre'. 

# # Deleting Wrong Data
# 

# In[4]:


# Printing the row with the error in the Google Play dataset
print(android_apps[10472])


# The Google Play dataset has a dedicated discussion section, and we can see that one of the discussions describes an error for the row 10472 .

# In[5]:


# Deleting the incorrect row
del android_apps[10472]


# In[6]:


#Checking the number of rows remaining in the android dataset
print(len(android_apps))


# # Deleting Duplicates

# In[7]:


# Identifying duplicate entries
duplicate_apps = []
unique_apps = []

for app in android_apps:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

# Printing the number of duplicates
print(f"Number of duplicate apps: {len(duplicate_apps)}")
print(f"Examples of duplicate apps: {duplicate_apps[:10]}")


# Once we've identified the duplicates, we'll create a new dataset that includes only the latest entries (those with the highest number of reviews):

# In[8]:


# Creating a dictionary to store the app name and the highest number of reviews
reviews_max = {}

for app in android_apps:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

# Creating a new dataset with only unique entries
android_clean = []
already_added = []

for app in android_apps:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[10]:


#exploring the clean dataset and checking the number of columns to be correct
print('Expected length:', len(android_apps) - 1181)
print()
explore_data(android_clean, 0, 5, True)


# # Removing Non-English Apps
# 

# We use is_english function to filter out the non English apps. With this function, Apps with names containing more than 3 characters not typically used in the English language will be filtered out. 
# The function is_english is  not perfect, and very few non-English apps might get past our filter, but this seems good enough at this point in our analysis.

# In[11]:


# Function to check if the app name is English
def is_english(string):
    non_ascii = 0
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    if non_ascii > 3:
        return False
    else:
        return True

# Filtering out non-English apps
android_english = [app for app in android_clean if is_english(app[0])]
ios_english = [app for app in ios_apps if is_english(app[1])]


# In[12]:


explore_data(android_english, 0, 3, True)
print()
explore_data(ios_english, 0, 3, True)


# # Filtering Paid Apps

# In[13]:


# Filtering out paid apps in the Android dataset
android_final = [app for app in android_english if app[6] == 'Free']

# Filtering out paid apps in the iOS dataset
ios_final = [app for app in ios_english if app[4] == '0.0']


# In[18]:


print('number of android apps=',len(android_final))
print()
print('number of ios apps=',len(ios_final))


# # Most Common Apps by Genre
# 

# To determine the most common genres in each market, we need to inspect the datasets and identify which columns contain information about the genre or category of the apps.
# 
#     For the Android dataset (Google Play): The relevant column is 'Genres' (column index 9) and 'Category' (column index 1). Both provide insight into the type of app, but the 'Genres' column can offer more detailed categorization.
# 
#     For the iOS dataset (App Store): The relevant column is 'prime_genre' (column index 11), which indicates the primary genre of the app

# In[19]:


#Building Frequency Tables
def freq_table(dataset, index):
    table = {}
    total = len(dataset)
    
    for row in dataset:
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    for key in table:
        table[key] = (table[key] / total) * 100
    
    return table


# In[24]:


#Displaying Frequency Tables
# Frequency table for the Category column in the Google Play dataset in descending  order 
android_category_freq = freq_table(android_final, 1)
print("Google Play Store - Category Frequency Table:")
for category in sorted(android_category_freq, key=android_category_freq.get, reverse=True):
    print(f"{category}: {android_category_freq[category]:.2f}%")
    


# In[25]:


# Frequency table for the Genres column in the Google Play dataset in descending  order
android_genres_freq = freq_table(android_final, 9)
print("Google Play Store - Genres Frequency Table:")
for genre in sorted(android_genres_freq, key=android_genres_freq.get, reverse=True):
    print(f"{genre}: {android_genres_freq[genre]:.2f}%")


# In[28]:


# Frequency table for the prime_genre column in the App Store dataset in descending order
ios_genre_freq = freq_table(ios_final, 11)
print("App Store - Prime Genre Frequency Table:")
for genre in sorted(ios_genre_freq, key=ios_genre_freq.get, reverse=True):
    print(f"{genre}: {ios_genre_freq[genre]:.2f}%")


# ## Most Popular Apps by Genre on the App Store
# 

# In[31]:


for ios_genre in ios_genre_freq:
    total = 0
    len_ios_genre = 0
    
    for app in ios_final:
        ios_genre_app = app[11]
        if ios_genre_app == ios_genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_ios_genre += 1
    
    avg_ios_ratings = total / len_ios_genre
    print(f"{ios_genre}: {avg_ios_ratings:.2f}")


# Top Genres by Average User Ratings
# Navigation: 86,090.33 average user ratings
# Reference: 74,942.11 average user ratings
# Social Networking: 71,548.35 average user ratings
# Music: 57,326.53 average user ratings
# Weather: 52,279.89 average user ratings
# Book: 39,758.50 average user ratings
# Food & Drink: 33,333.92 average user ratings
# Finance: 31,467.94 average user ratings
# Photo & Video: 28,441.54 average user ratings
# Travel: 28,243.80 average user ratings
# 
# Analysis and Recommendation
# Navigation Apps: Navigation apps have the highest average user ratings, suggesting they are highly engaging. If you can develop a navigation app with innovative features or improved user experience, it could perform very well in this category.
# 
# Reference Apps: These apps also have a high average number of user ratings. A reference app, perhaps something focused on a specific niche (like a comprehensive guide or an educational tool), could attract a significant user base.
# 
# Social Networking Apps: Social networking apps continue to be a dominant force, with high user engagement. This genre is competitive, but there's always room for innovation, especially in niche communities or specialized social platforms.
# 
# Music Apps: With a high average of user ratings, music apps also show strong engagement. A new music app could focus on unique features such as music discovery, sharing, or innovative ways to interact with music.
# 
# Weather Apps: Weather apps have surprisingly high engagement, indicating that users value accurate and detailed weather information. A weather app with personalized features or detailed forecasts might do well.
# 
# App Profile Recommendation
# Given the data, a Navigation app or Reference app could be a strategic choice for development. These genres have fewer competitors compared to Games or Social Networking but show high user engagement, which could translate into a solid user base and potentially higher revenue from in-app ads.

# # Most Popular Apps by Genre on Google Play

# In[43]:


display_table(android_final, 5) # the Installs columns


# In[45]:


for category in android_category_freq:
    total = 0
    len_category = 0
    
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            # Remove any commas and plus signs, and convert to a float
            n_installs = n_installs.replace(',', '').replace('+', '')
            n_installs = float(n_installs)
            total += n_installs
            len_category += 1
    
    avg_installs = total / len_category
    print(f"{category}: {avg_installs:.2f}")


# Analysis and App Profile Recommendation
# Here are a few observations:
# 
# Communication: This category has the highest average number of installs (38,456,119), indicating that communication apps are extremely popular. However, this category is likely very competitive.
# 
# Video Players: With an average of 24,727,872 installs, video players are also highly popular. A new video player app could be successful if it offers unique features or improved user experience.
# 
# Social: Social apps have an average of 23,253,652 installs, showing that they attract a large number of users. This category also aligns with the high user engagement seen in the App Store's Social Networking genre.
# 
# Photography: This category has an average of 17,840,110 installs, indicating that photography apps are widely used. Developing a photography app could be a good opportunity, especially if it offers innovative editing tools or social sharing capabilities.
# 
# Entertainment and Games: Both categories show strong engagement, with average installs of 11,640,705 and 15,588,015, respectively. Entertainment apps, including games, are always in demand, but this is also a highly competitive space.

# # Final Recommendation
# 

# Based on the analysis of both the App Store and Google Play Store datasets, here are the recommended app categories for development:
# 
# 1. Navigation Apps
# App Store Insight: Navigation apps have the highest average user ratings, with an average of 86,090.33 ratings per app. This indicates strong user engagement and satisfaction, suggesting that users value high-quality navigation apps.
# Recommendation: Developing a navigation app that offers innovative features, such as real-time traffic updates, offline maps, or integration with other services (e.g., ride-sharing or weather forecasting), could attract a large and loyal user base.
# 2. Reference Apps
# App Store Insight: Reference apps also show a high average number of user ratings, at 74,942.11 ratings per app. This category is less saturated than others like games or social networking but still demonstrates significant user engagement.
# Recommendation: A reference app focusing on a niche area (e.g., language learning, medical references, or DIY guides) could fill a gap in the market and attract users looking for specific, high-quality information.
# 3. Social Networking Apps
# Cross-Market Insight: Social networking apps are highly popular across both platforms, with an average of 71,548.35 ratings on the App Store and 23,253,652 installs on Google Play. This category is highly competitive, but there's still potential for growth, especially if the app offers a unique value proposition or targets a specific niche.
# Recommendation: Consider developing a social networking app that caters to a specific community or integrates new, engaging features like augmented reality (AR), real-time collaboration, or privacy-focused social interactions.
# 4. Photography Apps
# Cross-Market Insight: Photography apps have a strong presence on both platforms, with 28,441.54 average ratings on the App Store and 17,840,110 average installs on Google Play. The widespread use of smartphones with advanced cameras drives the demand for apps that offer photo editing, sharing, and creative tools.
# Recommendation: A photography app that combines powerful editing features with social sharing capabilities could stand out in this category. Consider adding features like AI-driven enhancements, filters, or community-driven content to increase user engagement.
# 5. Video Players and Editors
# Google Play Insight: Video players and editors have an average of 24,727,872 installs, indicating high popularity. Users increasingly consume and create video content on mobile devices, driving demand for apps that offer robust video editing and playback features.
# Recommendation: Developing a video player or editor app with unique functionalities—such as cloud integration, multi-platform support, or advanced editing tools—could attract a large user base. Consider including features like easy social media sharing, subtitle support, or streaming capabilities to enhance user experience.
# Conclusion
# For a company looking to maximize in-app advertising revenue, focusing on Navigation, Reference, Social Networking, Photography, or Video Player/Editor apps would be a strategic choice. These categories show strong user engagement across both the App Store and Google Play, offering a balance of high user ratings, download volumes, and potential for innovation. By developing apps in these categories, the company can tap into large, engaged audiences and increase its revenue through targeted in-app ads.
