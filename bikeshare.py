import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    error_message_1="Sorry the value you entered is invalid, please try again using the following cities (chicago, new york city, washington)"
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city= input('Please enter the name of the city to analyze (chicago, new york city, washington)\n').lower()
        if city in ["chicago","new york city", "washington"]:
            break
        else:
            print(error_message_1)

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month= input('Please enter the name of the month to filter by, or "all" to apply no month filter (january, february, march, april, may, june, all)\n').lower()
        if month in ["january", "february", "march", "april", "may", "june", "all"]:
            break
        else:
            print(error_message_1)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day= input('Please enter the name of the day of week to filter by, or "all" to apply no day filter (monday, tuesday, wednesday, thursday, friday, saturday, sunday, all\n').lower()
        if day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]:
            break
        else:
            print(error_message_1)

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
    data = CITY_DATA[city]
    print ("Analysis of the city database: " + data)
    df = pd.read_csv(data)

    """Start Time column --> Datetime, change format"""
    df['Start Time'] = pd.to_datetime(arg = df['Start Time'], format = '%Y/%m/%d %H:%M:%S')

    """Extract Month"""
    if month != 'all':
        df['month'] = df['Start Time'].dt.month
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df.loc[df['month'] == month]

    """Extract Day of week"""
    if day != 'all':
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        df = df.loc[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(arg = df['Start Time'], format = '%Y/%m/%d %H:%M:%S')

    # TO DO: display the most common month
    print('The most common month is: ',calendar.month_name[df['Start Time'].dt.month.mode()[0]])

    # TO DO: display the most common day of week
    print('The most common day of the week is: ',df['Start Time'].dt.weekday_name.mode()[0])

    # TO DO: display the most common start hour
    print('The most frequent start hour is: ',df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    """Use value_counts to find max values"""
    print('The most commonly used start station is: ', df['Start Station'].value_counts().idxmax(), ':', df['Start Station'].value_counts().max(), 'uses')

    # TO DO: display most commonly used end station
    print('The most commonly used end station is: ', df['End Station'].value_counts().idxmax(), ':', df['End Station'].value_counts().max(), 'uses')

    # TO DO: display most frequent combination of start station and end station trip
    both_stations = df['Start Station'] + "x" + df['End Station']
    both_station = both_stations.value_counts().idxmax()
    print('\nThe most frequently used combination of stations is:\n{} ---> {}'.format(both_station.split('x')[0], both_station.split('x')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    def change_time(seconds):
        m, s = divmod(seconds,60)
        h, m = divmod(m,60)
        d, h = divmod(h,24)
        y, d = divmod(d,365)
        print('Years: {}\nDays: {}\nHours: {}\nMins: {}\nSecs: {}'.format(y,d,h,m,s))

    print('Total travel time:')
    change_time(df['Trip Duration'].sum())

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: {} seconds'.format(round(df['Trip Duration'].mean()),2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print("")

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nEarliest year of birth: " , str(int(df['Birth Year'].min())))
        print("\nMost recent year of birth: " , str(int(df['Birth Year'].max())))
        print("\nMost common year of birth: " , str(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    """Check on columns"""
    print(df.columns.unique())

def display_data(df):
    raw_data = input('\nWould you like to see 5 lines of raw data? Enter Y or N.\n')
    line = 0

    while True :
        if raw_data.lower() == 'y':
            print(df.iloc[line : line + 5])
            line += 5
            raw_data = input('\nWould you like to see 5 more lines raw data? Enter Y or N.\n')
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        reset = input('\nWould you like to restart? Enter Y or N.\n')
        if reset.lower() == 'n':
            break

if __name__ == "__main__":
	main()
