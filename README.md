# crego_backend_assignment
Python Backend Developer Intern Assignment

In this section the methods to run it local and the images of the API results, MongoDB database has been attached separately

Prerequisites that are required to run the app locally
1.Pycharm or any Python IDE
2.Python(version 3.7)
3.Mongo DB Community Version
4.AWS Account to create redis cache
5.Postman App

# Process:
Make git clone of this repository on the local machine,
Change directory to the project in the terminal or in IDE,
Create a local conda environment and activate it,
Install all the necessary libraries by running pip install -r requirements.txt,
Now open the MongoDB start the connection,
If there is an AWS account create an redis cache.

In the crego_app fill your mongodb url in the required place,
Also get the endpoint url from redis cache created and fill it where it is required,
Run the app and test the api's in postman.

# API results

For creating webhook
API Request
![Screenshot (90)](https://github.com/Nikhilkrishna98/crego_backend_assignment/assets/45559705/2e00faed-e006-4fa1-be99-bef3f67e983c)
Database
![Screenshot (89)](https://github.com/Nikhilkrishna98/crego_backend_assignment/assets/45559705/1e75b34d-49de-44a7-8097-58d4cf26400f)

For updating the webhook
Data no.4 before updating
![Screenshot (94)](https://github.com/Nikhilkrishna98/crego_backend_assignment/assets/45559705/76d23e06-bcc6-45e5-a63c-1023985a4569)
API Request
![Screenshot (95)](https://github.com/Nikhilkrishna98/crego_backend_assignment/assets/45559705/abbcf994-71b1-43b4-8c4f-351247df5398)
Data no.4 after updating
![Screenshot (96)](https://github.com/Nikhilkrishna98/crego_backend_assignment/assets/45559705/76a53d89-08b1-478e-b178-ef09af299a03)

For fetching the data
API Request for one company_id
![Screenshot (92)](https://github.com/Nikhilkrishna98/crego_backend_assignment/assets/45559705/6c897568-a6a3-4d7e-8941-2dccbff0a27f)
API Request for fetching all data from database
![Screenshot (91)](https://github.com/Nikhilkrishna98/crego_backend_assignment/assets/45559705/57d8404d-48b0-48bb-8120-fb4cfa6e8ec9)

For deleting the data
API Request
![Screenshot (93)](https://github.com/Nikhilkrishna98/crego_backend_assignment/assets/45559705/aa1fc117-9c03-418e-b5c0-f64289b3a155)











