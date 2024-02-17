# bitnbuild-back

## API

### Base URL

<http://127.0.0.1:5000>

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
- **Response Body:** None
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
  