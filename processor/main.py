from datetime import datetime
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient


DASHBOARD_URL = os.environ["DASHBOARD_URL"]
MONGODB_URL = os.environ["MONGODB_URL"]


def distance(velocity: float, time: float) -> float:
    """
    Calculate the distance traveled based on the given velocity and time.

    Parameters:
    - velocity (float): The velocity of the object in meters per second.
    - time (float): The time taken for the motion in seconds.

    Returns:
    float: The distance traveled in meters.
    """
    return velocity * time


def calories(height: float, weight: float, velocity: float) -> float:
    """
    Estimate calories burned per minute during physical activity using a simplified model.

    Parameters:
    - height (float): Height of the individual in meters.
    - weight (float): Weight of the individual in kilograms.
    - velocity (float): Velocity of the activity in meters per second.

    Returns:
    float: Estimated calories burned per minute.
    """
    return 0.035 * weight + ((velocity**2) / height) * 0.029 * weight


def get_average_velocity(age: int, gender: str) -> float:
    """
    Estimate speed based on age and gender.

    Parameters:
    - age (int): The age of the individual.
    - gender (str): The gender of the individual, either 'male' or 'female'.

    Returns:
    float: The estimated speed in meters per second.

    Returns 0.0 if age doesn't fall into any specified range or if gender is not 'male' or 'female'.
    """
    gender = gender.lower()

    if 20 <= age <= 29:
        return 1.36 if gender == "male" else 1.34
    elif 30 <= age <= 39:
        return 1.43 if gender == "male" else 1.34
    elif 40 <= age <= 49:
        return 1.43 if gender == "male" else 1.39
    elif 50 <= age <= 59:
        return 1.43 if gender == "male" else 1.31
    elif 60 <= age <= 69:
        return 1.34 if gender == "male" else 1.24
    elif 70 <= age <= 79:
        return 1.26 if gender == "male" else 1.13
    elif 80 <= age <= 89:
        return 0.97 if gender == "male" else 0.94
    else:
        return 0.0


def get_dates(current_datetime: datetime) -> list:
    """
    Generates a list of dates representing the days of the week for the given input date.

    Parameters:
    - current_datetime (datetime): The input datetime for which the week's dates are to be generated.

    Returns:
    - list: A list of formatted strings representing the dates of the week in the format "%d/%m/%y".

    Note:
    The function uses the ISO calendar to determine the year and week number of the given input date.
    It then generates a list of dates from Monday (1) to Sunday (7) of that week in the specified format.
    """
    iso_calendar = current_datetime.isocalendar()
    iso_year, iso_week_number, _ = iso_calendar

    return [
        datetime.fromisocalendar(iso_year, iso_week_number, i).strftime("%d/%m/%y")
        for i in range(1, 8)
    ]


def get_data(
    results: list, average_velocity: float, height: float, weight: float
) -> dict:
    """
    Calculates and returns various activity-related data based on input parameters.

    Parameters:
    - results (list): A list of dictionaries containing activity results, each with an "activity" key
                     indicating the type of activity (e.g., 1 for running, 0 for walking).
    - average_velocity (float): The average velocity of the activities in meters per second.
    - height (float): The height of the individual in meters.
    - weight (float): The weight of the individual in kilograms.

    Returns:
    - dict: A dictionary containing calculated data for running and walking activities, including:
        - durations: Dictionary with "run" and "walk" keys, representing the duration (in seconds) of each activity.
        - distances: Dictionary with "run" and "walk" keys, representing the distance (in meters) covered in each activity.
        - calories: Dictionary with "run" and "walk" keys, representing the calories burned in each activity.

    Note:
    - The function calculates durations, distances, and calories for both running and walking activities.
    - Velocity for running is assumed to be twice the average velocity, and for walking, it is the average velocity.
    - Make sure the `distance` and `calories` functions are implemented elsewhere in your code.
    """

    duration_total = len(results)
    duration_run = len([result for result in results if result["activity"] == 1])
    duration_walk = duration_total - duration_run

    run_velocity = average_velocity * 2
    walk_velocity = average_velocity

    distance_run = distance(run_velocity, duration_run)
    distance_walk = distance(walk_velocity, duration_walk)

    calories_run = calories(height, weight, run_velocity) * (duration_run / 60.0)
    calories_walk = calories(height, weight, walk_velocity) * (duration_walk / 60.0)

    return {
        "durations": {
            "run": duration_run,
            "walk": duration_walk,
        },
        "distances": {
            "run": distance_run,
            "walk": distance_walk,
        },
        "calories": {
            "run": calories_run,
            "walk": calories_walk,
        },
    }


app = FastAPI()

origins = ["http://localhost:3000", DASHBOARD_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/data")
def data():
    mongo_client = MongoClient(MONGODB_URL)
    mongo_database = mongo_client["database"]
    mongo_collection = mongo_database["collection"]

    gender = "male"
    age = 27
    height = 1.70
    weight = 60.0

    current_datetime = datetime.now()
    current_day = current_datetime.strftime("%d")
    current_month = current_datetime.strftime("%m")
    current_year = current_datetime.strftime("%y")

    query = {"date": {"$regex": f"\\d{{2}}/{ current_month }/{ current_year }"}}
    results = list(mongo_collection.find(query))

    # Velocity (in meters per second)
    average_velocity = get_average_velocity(age, gender)

    month_data = get_data(results, average_velocity, height, weight)

    dates = get_dates(current_datetime)
    week_data = [
        get_data(
            [result for result in results if result["date"] == date],
            average_velocity,
            height,
            weight,
        )
        for date in dates
    ]

    today_data = get_data(
        [
            result
            for result in results
            if result["date"] == f"{ current_day }/{ current_month }/{ current_year }"
        ],
        average_velocity,
        height,
        weight,
    )
    return {"month": month_data, "week": week_data, "today": today_data}
