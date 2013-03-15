#Calorie Bank
-------------

A simple app for tracking a bank of calories for your diet. Assumes N kcals/day with a ceiling of X kcals/day.
 - X > N : Subtract from total banked calories
 - X < N : Add to total banked calores.
 - The bank can never drop below zero. Using more than you have banked will just reset the bank at zero.

#Setup
 - pip install -r requirements.txt
 - create secrets.py with your DB and static files settings (there is a sample file in CalorieBank/CalorieBank/secrets.py.sample
 - set your max options at the top of settings.py
 - run syncdb
 - using the python shell create a CalorieBank object (I know this sucks, but I will fix it later)
 - use the admin to create the first day you want to store calories
 - fire up runserver and open the site. The first time you run the site, it will create an entry for all dates between the newest date in the DB and today
 - start counting your calories

#License
--------
This is an open source project per the MIT licence. Fork it and use it at your leisure, but keep it open.
