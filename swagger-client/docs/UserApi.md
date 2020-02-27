# swagger_client.UserAPIApi

All URIs are relative to *http://0.0.0.0:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
*UserApi* | [**delete_user_uuid_post**](docs/UserApi.md#delete_user_uuid_post) | **POST** /delete_user/<user_uuid> | Delete a single user record
*UserApi* | [**get_total_users_get**](docs/UserApi.md#get_total_users_get) | **GET** /get_total_users | Get all system users
*UserApi* | [**get_user_by_email_get**](docs/UserApi.md#get_user_by_email_get) | **GET** /get_user_by_email/<user_email> | Get's a single user record
*UserApi* | [**get_user_by_uuid_get**](docs/UserApi.md#get_user_by_uuid_get) | **GET** /get_user_by_uuid/<user_uuid> | Get's a single user record
*UserApi* | [**post_user_post**](docs/UserApi.md#post_user_post) | **POST** /post_user | Adds a single user record
*UserApi* | [**post_users_post**](docs/UserApi.md#post_users_post) | **POST** /post_users | Adds users to User db. Upload as many as you want.
*UserApi* | [**update_user_by_uuid_put**](docs/UserApi.md#update_user_by_uuid_put) | **PUT** /update_user/<user_uuid> | Updates an existing user

[**delete_user_uuid_post**](UserApi.md#delete_user_uuid_post) | **POST** /delete_user/<user_uuid> | Delete a single user record
[**get_total_users_get**](UserApi.md#get_total_users_get) | **GET** /get_total_users | Get all system users
[**get_user_by_email_get**](UserApi.md#get_user_by_email_get) | **GET** /get_user_by_email/<user_email> | Get's a single user record
[**get_user_by_uuid_get**](UserApi.md#get_user_by_uuid_get) | **GET** /get_user_by_uuid/<user_uuid> | Get's a single user record
[**post_user_post**](UserApi.md#post_user_post) | **POST** /post_user | Adds a single user record
[**post_users_post**](UserApi.md#post_users_post) | **POST** /post_users | Adds users to User db. Upload as many as you want.
[**update_user_by_uuid_put**](UserApi.md#update_user_by_uuid_put) | **PUT** /update_user/<user_uuid> | Updates an existing user


# **delete_user_uuid_post**
> delete_user_uuid_post(user_uuid)

Delete a single user record

Delete a user

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UserAPIApi()
user_uuid = 'user_uuid_example' # str | UUID of the user to delete

try:
    # Delete a single user record
    api_instance.delete_user_uuid_post(user_uuid)
except ApiException as e:
    print("Exception when calling UserApi->delete_useruser_uuid_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_uuid** | **str**| UUID of the user to delete | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../../swagger-client/README.md#documentation-for-api-endpoints) [[Back to Model list]](../../swagger-client/README.md#documentation-for-models) [[Back to README]](../../swagger-client/README.md)

# **get_total_users_get**
> get_total_users_get()

Get all system users

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UserAPIApi()

try:
    # Get all system users
    api_instance.get_total_users_get()
except ApiException as e:
    print("Exception when calling UserApi->get_total_users_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../../swagger-client/README.md#documentation-for-api-endpoints) [[Back to Model list]](../../swagger-client/README.md#documentation-for-models) [[Back to README]](../../swagger-client/README.md)

# **get_user_by_email_get**
> User get_user_by_email_get(user_email)

Get's a single user record

Get single user record by given user_email

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UserAPIApi()
user_email = 'user_email_example' # str | Email of the user to get

try:
    # Get's a single user record
    api_response = api_instance.get_user_by_email_get(user_email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_by_email_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_email** | **str**| Email of the user to get | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../../swagger-client/README.md#documentation-for-api-endpoints) [[Back to Model list]](../../swagger-client/README.md#documentation-for-models) [[Back to README]](../../swagger-client/README.md)

# **get_user_by_uuid_get**
> User get_user_by_uuid_get(user_uuid)

Get's a single user record

Get single user record by given user_uuid

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UserAPIApi()
user_uuid = 'user_uuid_example' # str | UUID of the user to get

try:
    # Get's a single user record
    api_response = api_instance.get_user_by_uuid_get(user_uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->get_user_by_uuid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_uuid** | **str**| UUID of the user to get | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../../swagger-client/README.md#documentation-for-api-endpoints) [[Back to Model list]](../../swagger-client/README.md#documentation-for-models) [[Back to README]](../../swagger-client/README.md)

# **post_user_post**
> User post_user_post(body)

Adds a single user record

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UserAPIApi()
body = swagger_client.User() # User | User object

try:
    # Adds a single user record
    api_response = api_instance.post_user_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->post_user_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**User**](User.md)| User object | 

### Return type

[**User**](User.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../../swagger-client/README.md#documentation-for-api-endpoints) [[Back to Model list]](../../swagger-client/README.md#documentation-for-models) [[Back to README]](../../swagger-client/README.md)

# **post_users_post**
> Users post_users_post(body)

Adds users to User db. Upload as many as you want.

Add as many users to User db, as want.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UserApi()
body = swagger_client.Users() # Users | List of users to post

try:
    # Adds users to User db. Upload as many as you want.
    api_response = api_instance.post_users_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling UserApi->post_users_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Users**](Users.md)| List of users to post | 

### Return type

[**Users**](Users.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../../swagger-client/README.md#documentation-for-api-endpoints) [[Back to Model list]](../../swagger-client/README.md#documentation-for-models) [[Back to README]](../../swagger-client/README.md)

# **update_useruser_uuid_put**
> update_user_by_uuid_put(user_uuid, body)

Updates an existing user

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.UserApi()
user_uuid = 56 # int | UUID of user to update
body = swagger_client.User() # User | User object to update

try:
    # Updates an existing user
    api_instance.update_user_by_uuid_put(user_uuid, body)
except ApiException as e:
    print("Exception when calling UserApi->update_user_by_uuid_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_uuid** | **int**| UUID of user to update | 
 **body** | [**User**](User.md)| User object to update | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../../swagger-client/README.md#documentation-for-api-endpoints) [[Back to Model list]](../../swagger-client/README.md#documentation-for-models) [[Back to README]](../../swagger-client/README.md)

