# bitnbuild-back

## API

### Base URL

<http://127.0.0.1:5000> locally

<https://shirotsuma.pythonanywhere.com> on web

### Endpoints

### `/modules`

#### Get Modules

- **URL:** `/modules`
- **Method:** `GET`
- **Description:** Retrieves a list of all module IDs.
- **Request Body:** None
- **Response Body:**
  
  ```json
  {
    [
      {
          "id": 1,
          "title": "some title",
          "image_url": "test.asasdcom",
          "description": "Tessat"
      },
       ...
    ]
  }

- **If no modules exist:**

  ```json
  {
    []
  }

- **Response Code:** None

#### Add module

- **URL:** `/modules`
- **Method:** `POST`
- **Description:** Adds a new module to the system.
- **Request Body:**

  ```json
  {
    "title": "Module Title",
    "image_url": "http://example.com/image.png",
    "description": "Description of the module."
  }

- **Response Body:**

  ```json
  {
    "id": 5,
    "response": 200
  }

### `/modules/<module_id>`

#### Get Module

- **URL:** `/modules/<module_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific module.
- **URL Parameters:**
  - `module_id`: ID of the module to retrieve.
- **Response Body:**

  ```json
  {
    "id": 1,
    "title": "Module 1",
    "image_url": "http://example.com/module1.png",
    "description": "Description of Module 1"
  }

- **If no modules exist:**

  ```json
  {
    "module": {}
  }

#### Delete Module

- **URL:** `/modules/<module_id>`
- **Method:** `DELETE`
- **Description:** Removes specific module.
- **URL Parameters:**
  - `module_id`: ID of the module to delete.
- **Response Body:**
  
  ```json
  {
      { "response": 200}
  }

#### Put Module

- **URL:** `/modules/<module_id>`
- **Method:** `PUT`
- **Description:** Updates specific module.
- **URL Parameters:**
  - `module_id`: ID of the module to update.
- **Request Body:**
  
  ```json
  {
    "title": "Updated Title",
    "image_url": "http://example.com/updated_image.png",
    "description": "Updated description."
  }

- **Response Body:**
  
  ```json
  {
      { "response": 200}
  }

### `/events`

#### Get Events

- **URL:** `/events/<module_id>`
- **Method:** `GET`
- **Description:** Retrieves a list of all event IDs.
- **Request Body:** None
- **Response Body:**
  
  ```json
  {
      [1, 2, 3, ...]
  }

- **If no events exist:**

  ```json
  {
    []
  }

- **Response Code:** None

#### Add Event

- **URL:** `/events/<module_id>`
- **Method:** `POST`
- **Description:** Adds a new event to the system.
- **Request Body:**

  ```json
  {
    "date": "YYYY-MM-DD",
    "title": "Event Title",
    "image_url": "http://example.com/image.png",
    "description": "Description of the event."
  }

- **Response Body:**

  ```json
  {
    "id": 5,
    "response": 200
  }

### `/event`

### `/event/<event_id>`

#### Get Event

- **URL:** `/event/<event_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific event.
- **URL Parameters:**
  - `event_id`: ID of the event to retrieve.
- **Request Body:** None
- **Response Body:**

  ```json
  {
    [
        "id": 1,
        "module_id": 1,
        "date": "1800-01-01",
        "title": "Event 1",
        "image_url": "http://example.com/event1.png",
        "description": "Description of Event 1"
    ]
  }

- **If no events exist:**

  ```json
  {
    []
  }

#### Delete Event

- **URL:** `/event/<event_id>`
- **Method:** `DELETE`
- **Description:** Removes specific event.
- **URL Parameters:**
  - `event_id`: ID of the event to delete.
- **Request Body:** None
- **Response Body:**
  
  ```json
  {
      { "response": 200}
  }

#### Put Event

- **URL:** `/event/<event_id>`
- **Method:** `PUT`
- **Description:** Updates specific event.
- **URL Parameters:**
  - `event_id`: ID of the event to update.
- **Request Body:**
  
  ```json
  {
    "date": "YYYY-MM-DD",
    "title": "Updated Title",
    "image_url": "http://example.com/updated_image.png",
    "description": "Updated description."
  }

- **Response Body:**
  
  ```json
  {
      { "response": 200}
  }

### `/timeline/<module_id>`

#### Get chronologically events

- **URL:** `/timeline/<module_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a events chronologically.
- **URL Parameters:**
  - `module_id`: ID of the module to retrieve.
- **Request Body:** None
- **Response Body:**

  ```json
  {
    [
      {
        "id": 1,
        "module_id": 4,
        "date": "1928-01-12",
        "title": "Event in place X",
        "image_url": "http://example.com/module1.png",
        "description": "Description of event"
      }
      ...
    ]
  }

- **If no modules exist:**

  ```json
  {
    []
  }

- **NOTE:** `first record returns all events chronologically`

### `/game/image-name/<module_id>/<number_of_events>`

#### Get pairs of image and name

- **URL:** `/game/image-name/<module_id>/<number_of_events>`
- **Method:** `GET`
- **Description:** Retrieves image and name for a game based on the specified module ID and number of events.
- **URL Parameters:**
  - `module_id`: ID of the module to retrieve events from.
  - `number_of_events`: Number of events to retrieve image and name for.
- **Request Body:** None
- **Response Body:**

  ```json
  [
      {
          "title": "Event 1",
          "image_url": "http://example.com/event1.png"
      },
      {
          "title": "Event 2",
          "image_url": "http://example.com/event2.png"
      },
      ...
  ]

### `/game/image-date/<module_id>/<number_of_events>`

#### Get pairs of image and date

- **URL:** `/game/image-date/<module_id>/<number_of_events>`
- **Method:** `GET`
- **Description:** Retrieves image and date for a game based on the specified module ID and number of events.
- **URL Parameters:**
  - `module_id`: ID of the module to retrieve events from.
  - `number_of_events`: Number of events to retrieve image and name for.
- **Request Body:** None
- **Response Body:**

  ```json
  [
      {
          "date": "1928-01-17",
          "image_url": "http://example.com/event1.png"
      },
      {
          "date": "1066-07-14",
          "image_url": "http://example.com/event2.png"
      },
      ...
  ]

### `/game/higher-lower/<module_id>`

#### Get Events for Higher Lower Game

- **URL:** `/game/higher-lower/<module_id>`
- **Method:** `GET`
- **Description:** Retrieves events for a Higher Lower game based on the specified module ID. They are returned chronologically
- **URL Parameters:**
  - `module_id`: ID of the module to retrieve events from.
- **Request Body:** None
- **Response Body:**

  ```json
  [
      {
          "date": "2023-12-31",
          "title": "Event 1",
          "image_url": "http://example.com/event1.png"
      },
      {
          "date": "2024-01-01",
          "title": "Event 2",
          "image_url": "http://example.com/event2.png"
      }
  ]

### `/game/chronological/<module_id>/<number_of_events>`

#### Get Events for Chronological Game

- **URL:** `/game/chronological/<module_id>/<number_of_events>`
- **Method:** `GET`
- **Description:** Retrieves events for a chronological game based on the specified module ID and number of events.
- **URL Parameters:**
  - `module_id`: ID of the module to retrieve events from.
  - `number_of_events`: Number of events to retrieve.
- **Request Body:** None
- **Response Body:**

  ```json
  [
      {
          "date": "2023-12-31",
          "title": "Event 1",
          "image_url": "http://example.com/event1.png"
      },
      {
          "date": "2024-01-01",
          "title": "Event 2",
          "image_url": "http://example.com/event2.png"
      }
  ]

### `/game/trivia/<module_id>`

#### Get Trivia Question

- **URL:** `/game/trivia/<module_id>`
- **Method:** `GET`
- **Description:** Retrieves a trivia question and possible answers for a trivia game based on the specified module ID.
- **URL Parameters:**
  - `module_id`: ID of the module to retrieve questions from.
- **Request Body:** None
- **Response Body:**

  ```json
  {
      "question": "What is the capital of France?",
      "answers": ["Paris", "London", "Berlin", "Madrid"],
      "correct_answer": "Paris"
  }

### `/questions/<module_id>`

#### Get Questions

- **URL:** `/questions/<module_id>`
- **Method:** `GET`
- **Description:** Retrieves a list of questions related to the specified module ID.
- **URL Parameters:**
  - `module_id`: ID of the module to retrieve questions for.
- **Response Body:**

  ```json
  [
      1,
      2,
      3,
      ...
  ]

#### Add Question

- **URL:** `/questions/<module_id>`
- **Method:** `POST`
- **Description:** Adds a new question related to the specified module ID.
- **URL Parameters:**
  - `module_id`: ID of the module the question belongs to.
- **Request Body:**

  ```json
  {
      "question": "What is the capital of France?",
      "answers": ["Paris", "London", "Berlin", "Madrid"],
      "correct_answer": "Paris"
  }

- **Response Body:**

  ```json
  {
    "id": 123,
    "response": 200
  }

### `/question/<question_id>`

#### Get Question

- **URL:** `/question/<question_id>`
- **Method:** `GET`
- **Description:** Retrieves details of a specific question.
- **URL Parameters:**
  - `question_id`: ID of the question to retrieve.
- **Request Body:** None
- **Response Body:**

  ```json
  {
      "id": 123,
      "module_id": 456,
      "question": "What is the capital of France?",
      "answers": ["Paris", "London", "Berlin", "Madrid"],
      "correct_answer": "Paris"
  }

- **If no events exist:**

  ```json
  {
    []
  }

#### Delete Question

- **URL:** `/question/<question_id>`
- **Method:** `DELETE`
- **Description:** Deletes a specific question.
- **URL Parameters:**
  - `question_id`: ID of the question to delete.
- **Request Body:** None
- **Response Body:**

  ```json
  {
      "response": 200
  }

#### Update Question

- **URL:** `/question/<question_id>`
- **Method:** `PUT`
- **Description:** Updates details of a specific question.
- **URL Parameters:**
  - `question_id`: ID of the question to update.
- **Request Body:**

  ```json
  {
      "question": "Updated question?",
      "answers": ["Updated answer 1", "Updated answer 2", "Updated answer 3"],
      "correct_answer": "Updated answer 1"
  }

- **Response Body:**

  ```json
  {
      "response": 200
  }
