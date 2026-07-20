---
name: firestore-data
description: Handles NoSQL document operations and collection hierarchy exploration. Use for CRUD tasks and data retrieval. Provides flexible document manipulation and structured querying.
metadata:
  version: v1
  publisher: google
license: Apache-2.0
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and `<param_value>` with actual values.

**Bash:**
`node <skill_dir>/scripts/<script_name>.js '{"<param_name>": "<param_value>"}'`

**PowerShell:**
`node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\": \"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env files. Do not ask the user to set vars unless skill executions fails due to env var absence.


## Scripts


### add_documents

Adds a new document to a Firestore collection. Please follow the best practices :
 1. Always use typed values in the documentData: Every field must be wrapped with its appropriate type indicator (e.g., {"stringValue": "text"})
 2. Integer values can be strings in the documentData: The tool accepts integer values as strings (e.g., {"integerValue": "1500"})
 3. Use returnData sparingly: Only set to true when you need to verify the exact data that was written
 4. Validate data before sending: Ensure your data matches Firestore's native JSON format
 5. Handle timestamps properly: Use RFC3339 format for timestamp strings
 6. Base64 encode binary data: Binary data must be base64 encoded in the bytesValue field
 7. Consider security rules: Ensure your Firestore security rules allow document creation in the target collection


#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| collectionPath | string | The relative path of the collection where the document will be added to (e.g., 'users' or 'users/userId/posts'). Note: This is a relative path, NOT an absolute path like 'projects/{project_id}/databases/{database_id}/documents/...' | Yes |  |
| documentData | object | The document data in Firestore's native JSON format. Each field must be wrapped with a type indicator:
- Strings: {"stringValue": "text"}
- Integers: {"integerValue": "123"} or {"integerValue": 123}
- Doubles: {"doubleValue": 123.45}
- Booleans: {"booleanValue": true}
- Timestamps: {"timestampValue": "2025-01-07T10:00:00Z"}
- GeoPoints: {"geoPointValue": {"latitude": 34.05, "longitude": -118.24}}
- Arrays: {"arrayValue": {"values": [{"stringValue": "item1"}, {"integerValue": "2"}]}}
- Maps: {"mapValue": {"fields": {"key1": {"stringValue": "value1"}, "key2": {"booleanValue": true}}}}
- Null: {"nullValue": null}
- Bytes: {"bytesValue": "base64EncodedString"}
- References: {"referenceValue": "collection/document"} | Yes |  |
| returnData | boolean | If set to true the output will have the data of the created document. This flag if set to false will help avoid overloading the context of the agent. | No | `false` |


---

### delete_documents

Delete multiple documents from Firestore

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| documentPaths | array | Array of relative document paths to delete from Firestore (e.g., 'users/userId' or 'users/userId/posts/postId'). Note: These are relative paths, NOT absolute paths like 'projects/{project_id}/databases/{database_id}/documents/...' | Yes |  |


---

### get_documents

Gets multiple documents from Firestore by their paths

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| documentPaths | array | Array of relative document paths to retrieve from Firestore (e.g., 'users/userId' or 'users/userId/posts/postId'). Note: These are relative paths, NOT absolute paths like 'projects/{project_id}/databases/{database_id}/documents/...' | Yes |  |


---

### list_collections

List Firestore collections for a given parent path

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| parentPath | string | Relative parent document path to list subcollections from (e.g., 'users/userId'). If not provided, lists root collections. Note: This is a relative path, NOT an absolute path like 'projects/{project_id}/databases/{database_id}/documents/...' | No |  |


---

### query_collection

Retrieves one or more Firestore documents from a collection in a database in the current project by a collection with a full document path.
Use this if you know the exact path of a collection and the filtering clause you would like for the document.


#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| collectionPath | string | The relative path to the Firestore collection to query (e.g., 'users' or 'users/userId/posts'). Note: This is a relative path, NOT an absolute path like 'projects/{project_id}/databases/{database_id}/documents/...' | Yes |  |
| filters | array | Array of filter objects to apply to the query. Each filter is a JSON string with:
- field: The field name to filter on
- op: The operator to use ("<", "<=", ">", ">=", "==", "!=", "array-contains", "array-contains-any", "in", "not-in")
- value: The value to compare against (can be string, number, boolean, or array)
Example: {"field": "age", "op": ">", "value": 18} | Yes |  |
| orderBy | string | JSON string specifying the field and direction to order by (e.g., {"field": "name", "direction": "ASCENDING"}). Leave empty if not specified | Yes |  |
| limit | integer | The maximum number of documents to return | No | `100` |
| analyzeQuery | boolean | If true, returns query explain metrics including execution statistics | No | `false` |


---

### update_document

Updates an existing document in Firestore. Supports both full document updates and selective field updates using an update mask. Please follow the best practices:
 1. Use update masks for precision: When you only need to update specific fields, use the updateMask parameter to avoid unintended changes
 2. Always use typed values in the documentData: Every field must be wrapped with its appropriate type indicator (e.g., {"stringValue": "text"})
 3. Delete fields using update mask: To delete fields, include them in the updateMask but omit them from documentData
 4. Integer values can be strings: The skill accepts integer values as strings (e.g., {"integerValue": "1500"})
 5. Use returnData sparingly: Only set to true when you need to verify the exact data after the update
 6. Handle timestamps properly: Use RFC3339 format for timestamp strings
 7. Consider security rules: Ensure your Firestore security rules allow document updates


#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| documentPath | string | The relative path of the document which needs to be updated (e.g., 'users/userId' or 'users/userId/posts/postId'). Note: This is a relative path, NOT an absolute path like 'projects/{project_id}/databases/{database_id}/documents/...' | Yes |  |
| documentData | object | The document data in Firestore's native JSON format. Each field must be wrapped with a type indicator:
- Strings: {"stringValue": "text"}
- Integers: {"integerValue": "123"} or {"integerValue": 123}
- Doubles: {"doubleValue": 123.45}
- Booleans: {"booleanValue": true}
- Timestamps: {"timestampValue": "2025-01-07T10:00:00Z"}
- GeoPoints: {"geoPointValue": {"latitude": 34.05, "longitude": -118.24}}
- Arrays: {"arrayValue": {"values": [{"stringValue": "item1"}, {"integerValue": "2"}]}}
- Maps: {"mapValue": {"fields": {"key1": {"stringValue": "value1"}, "key2": {"booleanValue": true}}}}
- Null: {"nullValue": null}
- Bytes: {"bytesValue": "base64EncodedString"}
- References: {"referenceValue": "collection/document"} | Yes |  |
| updateMask | array | The selective fields to update. If not provided, all fields in documentData will be updated. When provided, only the specified fields will be updated. Fields referenced in the mask but not present in documentData will be deleted from the document | No |  |
| returnData | boolean | If set to true the output will have the data of the updated document. This flag if set to false will help avoid overloading the context of the agent. | No | `false` |


---

