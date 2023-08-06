# pynexusic
```pynexusic``` is a package that allows communication with Wood NEXUS IC tool

#### Installation
``` python
pip install pynexusic
```
#### Example
1) Import ```NEXUSIC_RESTAPI```
    ```python
   from pynexusic import NEXUSIC_RESTAPI as api
    ```
2) Initialize ```NEXUSIC_REST``` class
    ```python
   NX_REST = api.NEXUSIC_REST(baseURI, APIKey)
    ```
 3) Execute required function
    ```python
    result, result_code = NX_REST.getVersion()
    ```
    Output:
    ```python
    result = {'version': 'x.x.xxxxx.x', 'schema': 'x.xxx'}
    result_code = 200
    ```
#### License
This project is licensed under the MIT license.
