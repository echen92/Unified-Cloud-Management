CS242 Final Project Proposal
___________________________________

Overview: My proposal is to build a webapp that will make it easy to access multiple cloud storage services from one place.
Users will be able to login to services such as Dropbox, Google Drive, etc. and have a tabbed view of the files that are stored for each.
They will also be able to download files or folders to the computer or upload a file to one or all services.
If there is not enough storage space, it will notify the user and the upload will not happen.
The view will mainly have a dashboard sort of feel with options between storage services to login to.
If there are media files in the storage, the user will have the option to play the media within the browser.
If it is a text or pdf file, the user will be able to view the contents within the browser as well.
The webapp will require users to login, where each user will have their own profile of cloud services they have already logged into.
The app will be written mainly in Django and Python, with an sqlite database for the user profiles.

Week 1
_____________
Design of and setting up models for the user profile
Basic views and user profile login
Spike code to make sure API can be properly used


Week 2
_____________
Begin integrating services into app
View files currently in storage, free space available
Upload and download files to/from the service
Create views necessary for functionality and dialogs (templates for storage contents, dialog confirmations, etc)


Week 3
_____________
Integrate jQuery/AJAX to make all operations inlined
Play/view/load content from files/media within the drive (stream music/video, display text)


Week 4
_____________
Add file/folder sharing functionality (manage permissions and share link)
Realtime editing of files
