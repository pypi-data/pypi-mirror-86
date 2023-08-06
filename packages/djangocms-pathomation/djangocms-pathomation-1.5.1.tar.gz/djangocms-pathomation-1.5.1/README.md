

# djangocms-pathomation


Add live slide viewing capabilities to your own website built on Django CMS


## HOW TO INSTALL

1. Install our package

    `pip install djangocms-pathomation`
    

2. Get the plugin code (this will create a folder "plugin" in the
    location where you currently are with your cmd)

    `pip install --no-deps djangocms-pathomation -t plugin`

3. Go to the location and inside the folder "plugin" copy the folder
    "pathomation" and copy this in the directory of your django-cms
    project where *settings.py* is also located.
4. Open *settings.py* with an editor and add "pathomation" to INSTALLED_APPS

    `INSTALLED_APPS = ['pathomation',]`

5. With your cmd navigate to your django-cms project where manage.py is located and run the following command:

    `Python manage.py makemigrations`

6. Finally run the following command:

   `Python manage.py migrate`



## QUICK START



1. Inside Django CMS, navigate to administration -> Pathomation -> Settings -> My Pathomation connection settings and fill in your credentials and save.

2. To make sure your credentials are correct. You can always test the connection, by clicking on the *Test connection* button

3. Go to a page where you want to create a new post, toggle the structure by clicking on the icon on the top right.

4. Click on the "+" sign to add a new content and select *Pathomation slide*

5. Select the slide that you want to display and click on *save*.

6. To see the result, click on *publish page changes*
