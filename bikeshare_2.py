import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = { 'all': 0, 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please enter one of the following cities name: chicago, new york city, washington')
    city = input().lower()
    while city not in CITY_DATA.keys():
        print('Your input was invalid, please enter one of the following cities name: chicago, new york city, washington')
        city = input().lower()

    # get user input for month (all, january, february, ... , june)
    print('Please enter name of the month to be filtered by, or all for all months, (e.g. all, january, february, ... , june)')
    month = input().lower()
    while month not in MONTH_DATA.keys():
        print('Your input was invalid, please enter name of the month to be filtered by, or all for all months, (e.g. all, january, february, ... , june)')
        month = input().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Please enter the day of the week to be filtered by, or all for all days, (e.g. all, saturday, sunday,..., friday)')
    day = input().lower()
    DAYS = [ 'all', 'saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday',  'friday']
    while day not in DAYS:
        print('Your input was invalid, please enter name of the month to be filtered by, or all for all months, (e.g. all, january, february, ... , june)')
        day = input().lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # loading city data:
    df = pd.read_csv(CITY_DATA[city])

    # filtering by month:
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    if month != 'all':
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months_list.index(month) + 1
        df = df[df['month'] == month]

    # filtering by day:    
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month = list({i for i in MONTH_DATA if MONTH_DATA[i]==common_month})[0]
    print('The most common month is: ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is: ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is: ', common_hour)    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ', common_start_station)  

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: ', common_end_station)  

    # display most frequent combination of start station and end station trip
    df['Start ~ End'] = df['Start Station'].str.cat(df['End Station'], sep=' ~ ')
    start_end_station = df['Start ~ End'].mode()[0]
    print('The most frequent combination of start station and end station trip is: ', start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    minutes, seconds = divmod(total_time, 60)
    hours, minutes = divmod(minutes, 60)
    print('The total travel time is ', hours, ' hours,', minutes, ' minutes and ', seconds, 'seconds.')

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean())
    min, sec = divmod(mean_travel_time, 60)    
    if min >= 60:
        hrs, min = divmod(min, 60)
        print('The mean travel time is ', hrs, ' hours, ', min, ' minutes and ', sec, ' seconds.')
    else:
        print('The mean travel time is ', min, ' minutes and ', sec, ' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types are: ', user_types) 

    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print('The counts of gender are: ', gender)
    else:
        print("This data doesn't include information about the gender")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print('The earliest year of birth is: ', earliest_year, '\nThe most recent year of birth is: ', recent_year,'\nThe most common year of birth is: ', common_year)
    else:
        print("This data doesn't include information about the birth year")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#to view the trip data:
def view_trip_data(df):
    """Displays 5 rows of the trip data for chosen city."""

    RLIST = ['yes', 'no']
    rdata = ''
    counter = 0 # to track the displayed rows 
    while rdata not in RLIST:
        print("\nWould you like to view individual trip data? Enter yes or no.\n")
        rdata = input().lower()
        # to handle the user input:
        if rdata == "yes":
            print(df.head())
            # to display the next 5 rows:
            while rdata == 'yes':
                counter += 5
                print("\nWould you like to view more of the trip data? Enter yes or no.\n")
                rdata = input().lower()
                if rdata == "yes":
                    print(df[counter:counter+5])
                elif rdata != "yes":
                    break
        elif rdata == "no":
            break    

    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
# Would you like to view individual trip data