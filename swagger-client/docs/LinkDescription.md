# LinkDescription

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**href** | **str** | a URI template, as defined by RFC 6570, with the addition of the $, ( and ) characters for pre-processing | 
**rel** | **str** | relation to the target user of the link | 
**title** | **str** | a title for the link | [optional] 
**media_type** | **str** | media type (as defined by RFC 2046) describing the link target | [optional] [default to 'application/json']
**method** | **str** | method for requesting the target of the link (e.g. for HTTP this might be &#39;GET&#39; or &#39;DELETE&#39;) | [optional] [default to '(Optional) GET']
**enc_type** | **str** | The media type in which to submit data along with the request | [optional] [default to 'application/json']

[[Back to Model list]](../../swagger-client/README.md#documentation-for-models) [[Back to API list]](../../swagger-client/README.md#documentation-for-api-endpoints) [[Back to README]](../../swagger-client/README.md)


