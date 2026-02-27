```bash
2026-02-27 14:26:08,551 - INFO - envs.py:83 - Loaded .env file for google_app_01 at E:\projects\agentic-ai-course\tutorials\google_app_01\.env
2026-02-27 14:26:08,552 - INFO - envs.py:83 - Loaded .env file for google_app_01 at E:\projects\agentic-ai-course\tutorials\google_app_01\.env
2026-02-27 14:26:09,033 - INFO - agent_loader.py:129 - Found root_agent in google_app_01.agent
2026-02-27 14:26:09,073 - INFO - _api_client.py:640 - The project/location from the environment variables will take precedence over the API key from the environment variables.
2026-02-27 14:26:09,517 - INFO - google_llm.py:181 - Sending out request, model: gemini-2.5-flash-lite, backend: GoogleLLMVariant.VERTEX_AI, stream: False
2026-02-27 14:26:09,518 - WARNING - models.py:7468 - Tools at indices [1] are not compatible with automatic function calling (AFC). AFC is disabled. If AFC is intended, please include python callables in the tool list, and do not include function declaration in the tool list.
2026-02-27 14:26:13,305 - ERROR - adk_web_server.py:1560 - Error in event_generator: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Multiple tools are supported only when they are all search tools.', 'status': 'INVALID_ARGUMENT'}}
Traceback (most recent call last):
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\cli\adk_web_server.py", line 1533, in event_generator
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\runners.py", line 519, in run_async
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\runners.py", line 507, in _run_with_trace
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\runners.py", line 739, in _exec_with_plugin
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\runners.py", line 496, in execute
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\agents\base_agent.py", line 294, in run_async
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\agents\llm_agent.py", line 468, in _run_async_impl
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\flows\llm_flows\base_llm_flow.py", line 362, in run_async
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\flows\llm_flows\base_llm_flow.py", line 439, in _run_one_step_async
    async for llm_response in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\flows\llm_flows\base_llm_flow.py", line 812, in _call_llm_async
    async for event in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\flows\llm_flows\base_llm_flow.py", line 796, in _call_llm_with_tracing
    async for llm_response in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\flows\llm_flows\base_llm_flow.py", line 1049, in _run_and_handle_error
    raise model_error
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\flows\llm_flows\base_llm_flow.py", line 1035, in _run_and_handle_error
    async for response in agen:
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\models\google_llm.py", line 262, in generate_content_async
    raise ce
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\models\google_llm.py", line 241, in generate_content_async
    response = await self.api_client.aio.models.generate_content(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\models.py", line 7475, in generate_content
    return await self._generate_content(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\models.py", line 6242, in _generate_content
    response = await self._api_client.async_request(
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1442, in async_request
    result = await self._async_request(
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1375, in _async_request
    return await self._async_retry(  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 111, in __call__
    do = await self.iter(retry_state=retry_state)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 153, in iter
    result = await action(retry_state)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\_utils.py", line 99, in inner
    return call(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\__init__.py", line 420, in exc_check
    raise retry_exc.reraise()
          ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\__init__.py", line 187, in reraise
    raise self.last_attempt.result()
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\concurrent\futures\_base.py", line 449, in result
    return self.__get_result()
           ^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\concurrent\futures\_base.py", line 401, in __get_result
    raise self._exception
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 114, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
    await errors.APIError.raise_for_async_response(response)
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\errors.py", line 216, in raise_for_async_response
    await cls.raise_error_async(status_code, response_json, response)
    raise self._exception
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 114, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
    await errors.APIError.raise_for_async_response(response)
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\errors.py", line 216, in raise_for_async_response
    raise self._exception
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 114, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
    await errors.APIError.raise_for_async_response(response)
    raise self._exception
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 114, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
    raise self._exception
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 114, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
    await errors.APIError.raise_for_async_response(response)
    raise self._exception
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 114, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
    await errors.APIError.raise_for_async_response(response)
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\errors.py", line 216, in raise_for_async_response
    await cls.raise_error_async(status_code, response_json, response)
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\errors.py", line 238, in raise_error_async
    raise ClientError(status_code, response_json, response)
    raise self._exception
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 114, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
    await errors.APIError.raise_for_async_response(response)
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\errors.py", line 216, in raise_for_async_response
    await cls.raise_error_async(status_code, response_json, response)
    raise self._exception
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\tenacity\asyncio\__init__.py", line 114, in __call__
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
    result = await fn(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\_api_client.py", line 1320, in _async_request_once
    await errors.APIError.raise_for_async_response(response)
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\errors.py", line 216, in raise_for_async_response
    await cls.raise_error_async(status_code, response_json, response)
  File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\errors.py", line 238, in raise_error_async
    raise ClientError(status_code, response_json, response)
google.genai.errors.ClientError: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Multiple tools are supported only when they are all search tools.', 'status': 'INVALID_ARGUMENT'}}
```
