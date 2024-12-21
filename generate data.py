import pandas as pd
import random

# Random name generator
names = ["Jon Snow", "Tony Stark", "Jane Doe", "Alice Cooper", "Clark Kent", "Bruce Wayne", 
         "Diana Prince", "Peter Parker", "Natasha Romanoff", "Steve Rogers"]

# Random departments
departments = ["Dragon Taming", "Space Exploration", "IT", "Sales", "Finance", 
               "Journalism", "Superhero Training", "Cryptography", "Astrophysics", "Underwater Basket Weaving"]

# Random hobbies
hobbies = ["Swordfighting", "Inventing", "Gaming", "Singing", "Flying", "Juggling", "Astrophysics", 
           "Cat Memes", "Time Travel", "Dancing"]

# Random locations
locations = ["Winterfell", "Malibu", "New York", "Gotham", "Metropolis", "Paris", "Tokyo", "Atlantis", "Mars", "Asgard"]

# Generate dataset
num_employees = 50
data = {
    "EmployeeID": [i+1 for i in range(num_employees)],
    "Name": [random.choice(names) for _ in range(num_employees)],
    "Age": [random.randint(20, 60) for _ in range(num_employees)],
    "Department": [random.choice(departments) for _ in range(num_employees)],
    "Salary": [random.randint(40000, 200000) for _ in range(num_employees)],
    "ExperienceYears": [random.randint(0, 40) for _ in range(num_employees)],
    "Hobby": [random.choice(hobbies) for _ in range(num_employees)],
    "PerformanceScore": [random.randint(1, 10) for _ in range(num_employees)],
    "WorkLocation": [random.choice(locations) for _ in range(num_employees)],
    "RemoteWorkPercentage": [random.randint(0, 100) for _ in range(num_employees)],
}

# Create DataFrame
df = pd.DataFrame(data)

# Save as CSV for SQL upload
df.to_csv("EmployeeProfiles.csv", index=False)
print("Dataset created and saved as 'EmployeeProfiles.csv'")
