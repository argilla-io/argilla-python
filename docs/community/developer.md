---
description: Argilla-python is the reference argilla python server SDK.
---

Being a developer in Argilla means that you are a part of the Argilla community and you are contributing to the development of Argilla. This page will guide you through the steps that you need to take to set up your development environment and start contributing to Argilla. Argilla is built upon different core components:

- **Documentation**: The documentation for Argilla serves as an invaluable resource, providing a comprehensive and in-depth guide for users seeking to explore, understand, and effectively harness the core components of the Argilla ecosystem.

- **Python SDK**: A Python SDK which is installable with `pip install argilla`, to interact with the Argilla Server and the Argilla UI. It provides an API to manage the data, configuration, and annotation workflows.

- **FastAPI Server**: The core of Argilla is a Python `FastAPI server` that manages the data, by pre-processing it and storing it in the vector database. Also, it stores application information in the relational database. It provides a REST API to interact with the data from the Python SDK and the Argilla UI. It also provides a web interface to visualize the data.

- **Relational Database**: A relational database to store the metadata of the records and the annotations. `SQLite` is used as the default built-in option and is deployed separately with the Argilla Server but a separate `PostgreSQL` can be used too.

- **Vector Database**: A vector database to store the records data and perform scalable vector similarity searches and basic document searches. We currently support `ElasticSearch` and `AWS OpenSearch` and they can be deployed as separate Docker images.

- **Vue.js UI**: A web application to visualize and annotate your data, users, and teams. It is built with `Vue.js` and is directly deployed alongside the Argilla Server within our Argilla Docker image.
