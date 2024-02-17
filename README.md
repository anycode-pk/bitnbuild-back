# bitnbuild-back

## Modules API

This API allows users to manage modules within the system.

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
    "modules": [
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
    "modules": []
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
      "module": {
          "id": 1,
          "title": "Module 1",
          "image_url": "http://example.com/module1.png",
          "description": "Description of Module 1"
      }
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
- **Response Body:**
  
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
      "events": [1, 2, 3, ...]
  }

- **If no events exist:**

  ```json
  {
    "events": []
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
- **Response Body:**

  ```json
  {
      "event": [
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
    "event": []
  }

#### Delete Event

- **URL:** `/event/<event_id>`
- **Method:** `DELETE`
- **Description:** Removes specific event.
- **URL Parameters:**
  - `event_id`: ID of the event to delete.
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
- **Response Body:**
  
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
