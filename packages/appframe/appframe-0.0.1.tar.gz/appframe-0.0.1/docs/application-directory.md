# Webplane Application Directory

The application directory contains all the artifacts that are required by an application. Each directory at the top level represents a feature, when an application is started the webplane engine will run the initialization code associated with each feature. The content of the folder will be used as described on the feature documentation below.

## Application Features

Each directory at the top level is associated with a feature, all features are optional.

| Directory | Description
| --- | ---
| *boot* | Python modules with a boot() function, invoked when the application starts
| *modules* | Python modules that can be imported from other features
| *http* | Static files or web request handlers to be served via HTTP
| *tools* | CherryPy tools that will be imported and enabled for the application

### _http_ Content

The _http_ directory content is scanned and processed according to the following rules:

- If a top level file with name *.static*, each line on it will identify a file or directory which will be associated with a static content handler
- Filenames with a leading underscore *(_)* are skipped, they can be referenced while processing other files.
- Files with extension *.html* will be associated with a JinjaController
    - if there is a *_base.html* file , this base file will be rendered using the main html file for the content
    - if there is a corresponding *.yaml* file, its rendering will be extended to the template rendering arguments
    - if there is a corresponding **.py*, the python module *render()* will be invoked and the resulting dict will extended to the template rendering arguments

- Files with extension *.py* will be imported as Controller modules .
- If both .html and a .py files for the same base, the python module will be imported as a Renderer module.
