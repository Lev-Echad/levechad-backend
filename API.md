# LevEchad API Documentation

This is the documentation for the available (and future) APIs under `/api/`.

## General Usage

### Paginating
List views (such as `/api/volunteers`) have built-in paginating.

##### Parameters

* `page=<num>` - where <num> is a number between 1 and the maximum page size, or the string `last` to get the last page.
_Default: 1_
* `page_size=<size>` - where <size> is a number between 1 and 100, the number of items to put in each page. _Default:
30_

##### Response
**Note**: The response always looks like this, even if you haven't specified a page number.
```json

{
  "count": <amount-of-total-items>, // the number of total items (in all pages)
  "next": <next-page-url>,  // is null if there is no next page
  "previous": <previous-page-url>,  // is null if there is no previous page
  "results": [  // the results for this page
     ...
  ]
      
}
```

### Token Authentication
Restricted views (such as `/api/volunteers`) are endpoints that require authentication to access.

To generate a token, query `/api/authtoken` using POST with the following data:

```json
{"username": "", "password": ""}
```

A successful response looks like this:

```json
{ 'token' : '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b' }
```

Then you can supply the token to the restricted endpoint using the `Authorization` HTTP header:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```


Also see the [TokenAuthentication Django REST framework
documentation](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication). 

### Filtering
Some views have filtering available on them. These should contain an `Available Filters` section in their documentation.
This section contains the fields you can filter on, and what filters you can apply on each one.

For example, to filter on the `phone_number` field with the `icontains` filter, specify the GET parameter
`phone_number__icontains` (notice the double underscore).

| Filter    | Description                   | GET parameter    | Value specification     | Comments                               |
|-----------|-------------------------------|------------------|-------------------------|----------------------------------------|
| exact     | Field is exactly value        | field            |                         | Can be specified multiple times, OR-ed |
| icontains | String contains, ignore case  | field__icontains |                         |                                        |
| gt        | Greater than (numbers, dates) | field__gt        |                         |                                        |
| lt        | Lower than (numbers, dates)   | field__lt        |                         |                                        |
| range     | Is between <low> and <high>   | field__range     | <low>,<high>            |                                        |
| in        | Value is one of given options | field__in        | <optionA>,<optionB>,... |                                        |

### Throttling (Rate Limiting)
Most views should have throttling enabled. This makes it so they can only be accessed a certain amount of times in a certain
timeframe.

There are two types of throttling:

 * Anonymous throttling - only works for unauthenticated users (unlimited access for authenticated users), throttles by
 IP address
 * User throttling - always works, throttles by username (or IP address for unauthenticated users if the view doesn't
 require authentication)
 
Throttling is divided by `scopes` - if two endpoints share the same throttling scope that means they share the limit of
requests (if 5 requests are allowed per minute in a certain scope, and two views share this scope, it's 5 requests per
minute for both together).

Each endpoint with throttling has their scope declared in the documentation below, and whether they're anonymous or user
throttles.

Available scopes:

| Throttle scopes   | Amount of requests allowed | per...    |
|-------------------|----------------------------|-----------|
| hamal-data        | 1                          | 1 second  |
| login             | 1                          | 1 second  |
| user-choices-list | 2                          | 1 second  |
| city-autocomplete | 2                          | 1 second  |
| register          | 1                          | 5 seconds |
| send-sms          | 1                          | 5 minutes |
| check-sms         | 1                          | 2 seconds | 

Requests denied by throttling have the `429 Too Many Requests` status code and the following response (where X is the
no. of seconds left):

```json
{"detail":"Request was throttled. Expected available in X seconds."}
```

## API Endpoints

### `/api/volunteers`

* _This view is pageable. See "Paginating" section for more details. Results described here will be contained in the
`results` item of the pagination response._
* _This view requires authentication. See "Token Authentication" section for more details._
* _This view is filterable. See "Filtering" section above for more details & the filters available here._

**Description**: Returns a list of all volunteers (paginated & filtered).

**Allowed methods**: GET

**Throttling**: `hamal-data`, user throttle

**Parameters**: None

##### Response
```json
[
  {
    "id": 0,
    "first_name": "",
    "last_name": "",
    "tz_number": "",
    "phone_number": "",
    "date_of_birth": "yyyy-mm-dd",
    "age": 0,  // may be null
    "gender": "",  // choices: זכר, נקבה, מגדר אחר
    "city": {
      "name": "" // choices: a valid city (see #262 for city autocomplete)
      "x": 0,
      "y": 0            
    },
    "address": "",
    "coordinates": {
       // TODO - see #272
    },  
    "areas": [], // choices: צפון, ירושלים והסביבה, מרכז, יהודה ושומרון, דרום, סיוע טלפוני
    "organization": "", // may be null
    "moving_way": "", // choices: אופניים, קטנוע, מכונית, תחבורה ציבורית, רגלית
    "week_assignments_capacity": 1,
    "wanted_assignments": [
      "" // choices: חלוקת מזון, משלוח תרופות, סיוע לעובדים חיוניים, הסעות, תמיכה טלפונית, עזרה במשפחתונים, אחר
    ],
    "email": "",
    "email_verified": false,
    "score": 0, // the volunteer score: currently unused
    "created_date": "yyyy-mm-ddThh:mm:ss.MMMMMM+ZZ:ZZ",  // MMMMMM is microseconds, ZZ:ZZ is timezone
    "times_volunteered": 0,
    "languages": []  // choices: עברית, אנגלית, רוסית, צרפתית, ערבית, אחר
  },
  ...
]
```

#### Available Filters
```
'id': ['exact'],
'first_name': ['exact', 'icontains'],
'last_name': ['exact', 'icontains'],
'tz_number': ['exact', 'icontains'],
'phone_number': ['exact', 'icontains'],
'date_of_birth': ['gt', 'lt', 'exact'],
'age': ['gt', 'lt', 'exact'],
'gender': ['exact'],
'city': ['exact', 'in'],
'neighborhood': ['exact', 'icontains'],
'areas': ['exact'],
'moving_way': ['exact'],
'week_assignments_capacity': ['exact', 'range'],
'wanted_assignments': ['exact'],
'score': ['exact'],
'created_date': ['gt', 'lt', 'exact'],
'organization': ['exact', 'in']
```

### `/api/helprequests`
* _This view is pageable. See "Paginating" section for more details. Results described here will be contained in the
`results` item of the pagination response._
* _This view requires authentication. See "Token Authentication" section for more details._
* _This view is filterable. See "Filtering" section above for more details & the filters available here._

**Description**: Returns a list of all help requests (paginated & filtered)

**Allowed methods**: GET

**Throttling**: `hamal-data`, user throttle

**Parameters**: None

##### Response
```json
[
  {
    "id": 0,
    "full_name": "",
    "phone_number": "",
    "area": "", // one of: צפון, ירושלים והסביבה, מרכז, יהודה ושומרון, דרום, סיוע טלפוני
    "city": {
        "name": "",
        "x": 0,
        "y": 0
    },
    "address": "",
    "notes": "",
    "type": "", // one of: קניות, איסוף, תרופות, עזרה בבית, תמיכה טלפונית, סיוע לעובדים חיוניים, אחר
    "type_text": "",
    "request_reason": "", // one of: בידוד, קבוצת סיכון גבוהה, אחר
    "status": "", // one of: התקבלה, בטיפול, הועבר למתנדב, טופל, לא טופל
    "status_updater": "",
    "helping_volunteer": {
      "id": 0,
      "full_name": ""
    },
    "created_date": ""
  },
  ...
]
```

#### Available Filters
```
'id': ['exact'],
'city': ['exact', 'in'],
'area': ['exact', 'in'],
'status': ['exact', 'in'],
'type': ['exact', 'in']
```

### `/api/register`

**Description**: Registers a volunteer into the system.

**Allowed methods**: POST

**Throttling**: `register`, anonymous throttle

##### Parameters

_Access `/api/register` with OPTIONS to see accepted request (in development, click the OPTIONS button in the
`/api/register` web view)._

##### Response

* On invalid input, returns status code `400 Bad Request`. Specifies all invalid fields & their error messages. Example
response:

  ```json
  {
    "first_name": [
        "This field may not be blank."
    ],
    "parental_consent": {
        "parent_name": [
            "This field may not be blank."
        ],
        "parent_id": [
            "This field may not be blank."
        ]
    }
  }
  ```
* On success, returns status code `201 Created`. Returns the request data.

### `/api/createhelprequest`

**Description**: Creates a help request.

**Allowed methods**: POST

##### Parameters

_Access `/api/createhelprequest` with OPTIONS to see accepted request (in development, click the OPTIONS button in the
`/api/createhelprequest` web view)._

##### Response

* On invalid input, returns status code `400 Bad Request`. Specifies all invalid fields & their error messages. Example
response:

  ```json
  {
    "full_name": [
      "This field may not be blank."
    ],
    "phone_number": [
      "This field may not be blank."
    ],
    "address": [
      "This field may not be blank."
    ],
    "request_reason": [
        "\"invalidchoice\" is not a valid choice."
    ]
  }
  ```
* On success, returns status code `201 Created`. Returns the request data.

### `/api/sendverificationcode`

**Description**: Sends an SMS verification code to the given number. **Currently a stub, see #198**

**Allowed methods**: POST

**Throttling**: `send-sms`, anonymous throttle

##### Parameters

```json
{
  "phoneNumber": ""  
}
```

##### Response

 * On invalid input, returns status code `400 Bad Request`. Example response:
    ```json
    {
        "success": false,
        "message": "Invalid phone number specified."
    }
    ```
 * Valid input returns status code `200 OK`.
    ```json
    {
        "success": true,
        "message": ""
    }
    ```

### `/api/checkverificationcode`

**Description**: Checks the verfication code sent be `/api/sendverificationcode`. **Currently a stub, see #198**

**Allowed methods**: POST

**Throttling**: `check-sms`, anonymous throttle

##### Parameters

```json
{
  "phoneNumber": "",
  "codeReceived": ""
}
```

##### Response

 * On invalid input, returns status code `400 Bad Request`. Example response:
    ```json
    {
        "success": false,
        "message": "The \"phoneNumber\", \"codeReceived\" parameters must be specified."
    }
    ```
 * Valid input returns status code `200 OK`, with the `verified` field stating whether the code was correct or not.
 Example response:
   ```json
    {
        "success": true,
        "message": "",
        "verified": true  // whether the code sent is verified or not
    }
    ```

### `/api/cityautocomplete`

**Description**: Provides city autocomplete for two characters and up.

**Allowed methods**: GET

**Throttling**: `city-autocomplete`, anonymous throttle

##### Parameters

This view accepts query parameters:

* `name__startswith`: the string to autocomplete with city names. Must be above two characters. _Notice the double
underscore!_

##### Response

* On invalid input, returns status code `400 Bad Request`. Response (if `name__startswith` is missing/below two
characters):
    ```json
    {
        "detail": [
            "name__startswith parameter must be above 2 characters."
        ]
    }
    ```
  
* On valid input, returns status code `200 OK`, with a list of all city names that match. Example response (for
`name__startswith=אב`):

    ```json
    [
        "אבירים",
        "אבו עבדון (שבט)",
        ...
    ]
    ```
  
  The list will be empty if no results were found.
  
### `/api/areas`

* _This view requires authentication. See "Token Authentication" section for more details._

**Description**: Returns all available areas (hamals).

**Allowed methods**: GET

**Throttling**: `user-choices-list`, user throttle

**Parameters**: None

##### Example response

```json
[
  "צפון",
  "ירושלים והסביבה",
  "מרכז",
  "יהודה ושומרון",
  "דרום",
  "סיוע טלפוני"
]
```

### `/api/languages`

* _This view requires authentication. See "Token Authentication" section for more details._

**Description**: Returns all available languages.

**Allowed methods**: GET

**Throttling**: `user-choices-list`, user throttle

**Parameters**: None

##### Example response

```json
[
  "עברית",
  "אנגלית",
  ...
]
```