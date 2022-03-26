import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv', encoding='utf-8')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    df_men = df[df['sex'] == 'Male']
    average_age_men = round(df_men[['age']].mean(axis=0)[0], 1)
    

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df['education'].value_counts().Bachelors) / df.shape[0] * 100, 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?
    df['advanced_education'] = df['education'].apply(lambda x: 'yes' if x in ['Bachelors', 'Masters', 'Doctorate'] else 'no')
    df_advanced_salary = df.pivot_table(index=['advanced_education', 'salary'], aggfunc='count').reset_index()
    df_advanced_salary = df_advanced_salary[['advanced_education', 'salary', 'education']]
    people_adv_ed = df_advanced_salary[df_advanced_salary['advanced_education'] == 'yes']['education'].sum(axis=0)
    people_adv_ed_more_50k = df_advanced_salary[(df_advanced_salary['advanced_education'] == 'yes') & (df_advanced_salary['salary'] == '>50K')]['education'].sum(axis=0)
    percentage_people_adv_more_50k = people_adv_ed_more_50k / people_adv_ed * 100
    people_without_adv_ed = df_advanced_salary[df_advanced_salary['advanced_education'] == 'no']['education'].sum(axis=0)
    people_without_adv_ed_more_50k = df_advanced_salary[(df_advanced_salary['advanced_education'] == 'no') & (df_advanced_salary['salary'] == '>50K')]['education'].sum(axis=0)
    percentage_people_without_adv_more_50k = people_without_adv_ed_more_50k / people_without_adv_ed * 100
  
  
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = round(people_adv_ed * df.shape[0] * 100, 1)
    lower_education = round(people_without_adv_ed * df.shape[0] * 100, 1)

    # percentage with salary >50K
    higher_education_rich = round(percentage_people_adv_more_50k, 1)
    lower_education_rich = round(percentage_people_without_adv_more_50k, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_hs_person_week = df['hours-per-week'].min(axis=0)
    min_work_hours = min_hs_person_week

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    people_work_min_hs = df[df['hours-per-week'] == min_hs_person_week]
    people_work_min_hs = people_work_min_hs.pivot_table(index=['salary'], aggfunc='count').reset_index()
    people_work_min_hs = people_work_min_hs[['salary', 'education']]
    people_work_min_hs_value = people_work_min_hs['education'].sum()
  
    num_min_workers = round(people_work_min_hs_value, 1)

    people_work_min_hs_more_50k = people_work_min_hs[people_work_min_hs['salary'] == '>50K']['education'].sum()
    percentage_people_work_min_hs_more_50k = people_work_min_hs_more_50k / people_work_min_hs_value * 100

    rich_percentage = round(percentage_people_work_min_hs_more_50k, 1)

    # What country has the highest percentage of people that earn >50K?
    df_resume = pd.crosstab(df['native-country'], df['salary'], normalize='index').reset_index().sort_values(by='>50K', ascending=False)
    highest_earning_country = df_resume.iloc[0]['native-country']
    highest_earning_country_percentage = round(df_resume.iloc[0]['>50K'] * 100, 1)

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['salary'] == '>50K') & (df['native-country'] == 'India')]['occupation'].value_counts().index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
