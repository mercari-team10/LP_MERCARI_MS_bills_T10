# Bills Microservice

The Bills Microservice contains the methods to get the bills for a particular patient, as well as to add additional charges for a patient. The microservice uses PostgreSQL as the database, owing to the highly dynamic nature of the database.

The various endpoints contained in the bills microservice include the following :

- `/bills [METHOD = GET]` : This endpoint is used to retrieve all the bills from the database corresponding to a particular `patient_id`

- `/bills [METHOD = POST]` : This endpoint is used to add additional charges to the databse for a particular patient, by the hospital


