import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': '._chicago.csv',
              'new york city': '._new_york_city.csv',
              'washington': '._washington.csv' }

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter one of the specified cities.")

    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Which month? January, February, March, April, May, June or 'all'?\n").lower()
        if month in months:
            break
        else:
            print("Invalid input. Please enter a valid month.")

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or 'all'?\n").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day.")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print(f"\nError: The data file for {city.title()} was not found.")
        return pd.DataFrame()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0].title()
    print(f'Most Common Month: {common_month}')

    common_day = df['day_of_week'].mode()[0].title()
    print(f'Most Common Day of Week: {common_day}')

    common_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].mode()[0]
    print(f'Most Commonly Used Start Station: {start_station}')

    end_station = df['End Station'].mode()[0]
    print(f'Most Commonly Used End Station: {end_station}')

    df['Start-End Combo'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Start-End Combo'].mode()[0]
    print(f'Most Frequent Trip: {common_trip}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    print(f'Total Travel Time: {total_duration} seconds')

    mean_duration = df['Trip Duration'].mean()
    print(f'Mean Travel Time: {mean_duration:.2f} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User Types:")
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("\nGender Distribution:")
        print(df['Gender'].value_counts())
    else:
        print("\nGender data not available for this city.")

    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nBirth Year Stats:")
        print(f"Earliest: {earliest}")
        print(f"Most Recent: {most_recent}")
        print(f"Most Common: {most_common}")
    else:
        print("\nBirth Year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def summary_report(df):
    print("\nSummary Report:")
    print("Total trips: {len(df)}")
    print(f"Average Trip Duration: {df['Trip Duration'].mean():.2f} seconds")

    if 'User Type' in df.columns:
        print("\nUser Types:")
        print(df['User Type'].value_counts().to_string())

    if 'Gender' in df.columns:
        print("\nGender Breakdown:")
        print(df['Gender'].value_counts().to_string())

def display_raw_data(df):
    index = 0
    show_data = input('/nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()

    while show_data == 'yes':
        if index + 5 > len(df): 
            print(df.iloc[index:])
            print("\nNo more data to display")
        else:
            print(df.iloc[index:index+5])
            index += 5
            show_data = input('\nWould you like to see more lines of raw data? Enter yes or no.\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()