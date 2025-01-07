import pandas as pd
import numpy as np


allowance_events_path = 'allowance_events.json'
allowance_backend_table_path = 'allowance_backend_table.csv'
payment_schedule_backend_table_path = 'payment_schedule_backend_table.csv'


with open(allowance_events_path, 'r') as file:
    allowance_events = pd.read_json(file, lines=False)


def process_allowance_events(df):
    df['user_id'] = df['user'].apply(lambda x: x.get('id'))
    df['event_timestamp'] = pd.to_datetime(df['event'].apply(lambda x: x.get('timestamp')))
    df['event_name'] = df['event'].apply(lambda x: x.get('name'))
    df['frequency'] = df['allowance'].apply(lambda x: x['scheduled'].get('frequency'))
    df['day'] = df['allowance'].apply(lambda x: x['scheduled'].get('day'))
    return df[['user_id', 'event_timestamp', 'event_name', 'frequency', 'day']]

allowance_events_cleaned = process_allowance_events(allowance_events)


allowance_backend_table = pd.read_csv(allowance_backend_table_path)
payment_schedule_backend_table = pd.read_csv(payment_schedule_backend_table_path)


def calculate_next_payment(event_date, frequency, day):
    days_of_week = {'sunday': 6, 'monday': 0, 'tuesday': 1, 'wednesday': 2,
                    'thursday': 3, 'friday': 4, 'saturday': 5}
    if frequency == 'daily':
        return event_date + pd.Timedelta(days=1)
    elif frequency == 'weekly':
        target_day = days_of_week.get(day.lower(), -1)
        days_until_next = (target_day - event_date.weekday() + 7) % 7
        return event_date + pd.Timedelta(days=days_until_next)
    elif frequency == 'biweekly':
        target_day = days_of_week.get(day.lower(), -1)
        days_until_next = (target_day - event_date.weekday() + 7) % 7
        return event_date + pd.Timedelta(days=days_until_next + 7)
    elif frequency == 'monthly':
        if day.lower() == '1st':
            return event_date.replace(day=1) + pd.offsets.MonthBegin()
        elif day.lower() == '15th':
            return event_date.replace(day=1) + pd.offsets.MonthBegin() + pd.Timedelta(days=14)
    return np.nan


allowance_events_cleaned['calculated_next_payment'] = allowance_events_cleaned.apply(
    lambda row: calculate_next_payment(row['event_timestamp'], row['frequency'], row['day']),
    axis=1
)


comparison = allowance_backend_table.merge(
    allowance_events_cleaned,
    how='left',
    left_on=['uuid', 'frequency', 'day'],
    right_on=['user_id', 'frequency', 'day']
)
comparison['discrepancy'] = comparison['next_payment_day'] != comparison['calculated_next_payment'].dt.day


def classify_discrepancy(row):
    if pd.isna(row['calculated_next_payment']):
        return "Missing Calculation"
    elif row['next_payment_day'] != row['calculated_next_payment'].day:
        return "Mismatched Values"
    return "Other"

comparison['discrepancy_type'] = comparison.apply(classify_discrepancy, axis=1)


discrepancy_summary = comparison['discrepancy_type'].value_counts().reset_index()
discrepancy_summary.columns = ['Discrepancy Type', 'Count']


comparison.to_csv('comparison_results.csv', index=False)
discrepancy_summary.to_csv('discrepancy_summary.csv', index=False)


print("Discrepancy Summary:")
print(discrepancy_summary)
