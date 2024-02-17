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
      "modules": [1, 2, 3, ...]
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
      "module": [
          1,
          "Module 1",
          "http://example.com/module1.png",
          "Description of Module 1"
      ]
  }

- **If no modules exist:**

  ```json
  {
    "module": []
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
