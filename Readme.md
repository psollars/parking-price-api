# Parking Price API

## Running the Application

This project is built with [pipenv](https://pipenv.pypa.io/en/latest/) which is required to run the start up and testing scripts.

You can start the application by running the `./start.sh` script from the command line. This will install necessary packages, create the database and initialize it with a set of parking rates, and launch the server on port `5000`.

**Alternatively**, the API can be launched in debug mode with VS Code. There is a `launch.json` that is configured to run this Django server on port `5000`, but VS Code will allow you to set breakpoints, etc.

## The API

### Base URL

The API is accessible at: http://127.0.0.1:5000/

### GET `/rates/`

Fetches all the parking rates stored in the database.

**Response**

- 200 OK: Returns a JSON array of rate objects.

```json
[
  {
    "days": "mon,tues,wed",
    "times": "0900-1700",
    "tz": "America/Chicago",
    "price": 1500
  }
  // ... more rates
]
```

### PUT `/rates/`

Updates the parking rates by overwriting the existing rates with the new rates provided in the request body.

**Request Body**

- A JSON array of rate objects.
- The timezones specified as `tz` in the JSON should adhere to the 2017c version of the tz database. For more information, refer to: [https://en.wikipedia.org/wiki/List_of_tz_database_time_zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

```json
[
  {
    "days": "mon,tues,wed",
    "times": "0900-1700",
    "tz": "America/Chicago",
    "price": 1500
  }
  // ... more rates
]
```

**Response**

- 201 Created: Successfully updated the rates.
- 400 Bad Request: Invalid data format.

### GET `/price/`

Fetches the price for parking within a specific time range.

**Query Parameters**

- start: The start time in ISO-8601 format with timezones.
- end: The end time in ISO-8601 format with timezones.

Datetime ranges must be specified in ISO-8601 format. A rate must completely encapsulate a datetime range for it to be available. **Example:** `?start=2015-07-01T07:00:00-05:00&end=2015-07-01T12:00:00-05:00`

**Response**

- 200 OK: Returns a JSON object with the price.

```json
{
  "price": 1500
}
```

- 200 OK: If the price is unavailable.

```json
{
  "price": "unavailable"
}
```

## Testing

This project is equipped with a testing script (`./test.sh`) that runs the Django test command once required packages have been installed. This script isn't required to run tests if the environment has already been initialized and you know what you are doing.
