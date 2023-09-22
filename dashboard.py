import pandas as pd


# Function to get the count of each unique subject in the dataframe
def getvaluecounts(df):
    return dict(df['subject'].value_counts())

# Function to get the count of subscribers for each 'level'
def getlevelcount(df):
    return dict(list(df.groupby(['level'])['num_subscribers'].count().items())[1:])

# Function to get the count of subjects per level
def getsubjectsperlevel(df):
    
    # Get a list of tuples where each tuple contains a subject and its corresponding level
    ans = list(dict(df.groupby(['subject'])['level'].value_counts()).keys())
        # Create a list of strings combining the subject and its level
    alllabels = [ans[i][0]+'_'+ans[i][1] for i in range(len(ans))]
    # Get the values (counts) associated with each subject and level combination
    ansvalues = list(dict(df.groupby(['subject'])[
                     'level'].value_counts()).values())

    # Create a dictionary with subject_level as the key and its count as the value
    completedict = dict(zip(alllabels, ansvalues))

    return completedict

# Function to calculate profits year-wise and other aggregated metrics
def yearwiseprofit(df):
    # Replace 'Free' and 'TRUE' values with 0 in the 'price' column
    df['price'] = df['price'].replace({'Free': '0', 'TRUE': '0'})
     # Convert the 'price' column to float type
    df['price'] = df['price'].astype('float')


    # Calculate the profit by multiplying price with the number of subscribers
    df['profit'] = df['price'] * df['num_subscribers']

    # Converting the time column to year,month,day and many more
    # Extract the date part of the 'published_timestamp'
    df['published_date'] = df['published_timestamp'].apply(
        lambda x: x.split('T')[0])

    # dropping of that index which has '3 hours' as time
    # Drop the row with index 2066 (it has '3 hours' in the time column)
    df = df.drop(df.index[2066])

    # converting the published date to pandas datetime object
    # Convert 'published_date' to pandas datetime object
    df['published_date'] = pd.to_datetime(
        df['published_date'], format="%Y-%m-%d")

   # Extract Year, Month, and Day from 'published_date'
    df['Year'] = df['published_date'].dt.year

    df['Month'] = df['published_date'].dt.month

    df['Day'] = df['published_date'].dt.day


    # Extract the name of the month from 'published_date'
    df['Month_name'] = df['published_date'].dt.month_name()
   # Calculate the sum of profits for each year
    profitmap = dict(df.groupby(['Year'])['profit'].sum())
    # Calculate the sum of subscribers for each year
    subscribersmap = dict(df.groupby(['Year'])['num_subscribers'].sum())
    # Calculate the sum of profits for each month
    profitmonthwise = dict(df.groupby(['Month_name'])['profit'].sum())
    #
    monthwisesub = dict(df.groupby(['Month_name'])['num_subscribers'].sum())

    return profitmap, subscribersmap,profitmonthwise,monthwisesub
