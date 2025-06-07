
1. Run `django-admin startproject alarms`

2. Run `django-admin startapp core`

3. Config settings
    1. Add core app in installed apps
    2. Add rest_framework in installed apps
    3. Add api-gateway to allowed hosts
    4. Add alarms-db on databases

4. Create Models
    1. Create Alarm Model
    2. Create Alarm User Model
    3. Create validation on saving Alarm User to check user on external service

5. Create Serializer for the Models
    1. Create Alarm Serializer
    2. Create AlarmUser Serializer
    3. Making Nested serialization on "alarm" field of AlarmUser

6. Create Viewsets
    1. Create Alarm View Set
    2. Create AlarmUser View Set

7. Add router on urls.py to map for 
