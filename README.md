# HaxOcean - recruitment task.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Authentication](#Authentication)
* [Setup](#setup)
* [Common issue](#common-issue)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
- This project is using a drf_spectacular to create a documentation. I also used flake8 to write a code with PEP8 standard. All project is in docker. In past,
I didn't have a lot of experience with containers.


## Technologies Used
- Django,
- Django Rest Framework,
- DRF Spectacular,
- Celery,
- Docker,
- Flake8

If you want to generate expiry link there are type of images:
![kind](https://user-images.githubusercontent.com/83407728/174257588-8be0b1b8-e3a2-4b45-afa6-81b71e0f32e1.png)


## Authentication

I used token authentication, so firstly You should create a user account in django-admin panel. Don't forget add a user group!.
![ssauthuser1](https://user-images.githubusercontent.com/83407728/174156829-a555731b-aa56-497d-9c14-9c7cdb4ae784.png)
Next, you can use a api/docs to get a token:
![token](https://user-images.githubusercontent.com/83407728/174157200-4147b4d9-53f4-4fc3-a1f8-e307b53e522b.png)
This token give you authentication. You can use this to login in drf_spectacular. Notice, that before authtoken you must write 'Token'.
![login](https://user-images.githubusercontent.com/83407728/174157720-7aa12b88-7dd5-4ca6-8e15-97e499448ba5.png)
Now you can pretty easy test my API.


## Setup
#### 1 Step: 
Clone a repository: 
`git clone https://github.com/bie7u/HexOcean_Exercise.git` 
#### 2 Step: 
-Navigate to local procject repository and run docker-compose: 
`docker-compose build` 
#### 3 Step: 
-Start the container: 
`docker-compose up` 
#### Create superuser:
When server is running, write in another console (in repo folder) \
`docker-compose run --rm app sh -c "python manage.py createsuperuser"` 


## Common issue
If you first time login on app and want to generate auth token you can have probably this issue:
![Zrzut ekranu 2022-06-16 214917](https://user-images.githubusercontent.com/83407728/174158585-cc76f74f-1879-41b0-a610-bfa55bc1f84e.png)
In this case you must delete cookies from our website. Fot this task, you can use EditThisCookie Chrome plug.

## Contact
Created by [krystiantsp@gmail.com](krystiantsp@gmail.com) - feel free to contact me!
