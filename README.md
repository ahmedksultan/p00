# FOLDOVER by Printer Carts
## Instructions on Using FoldOver:<br>
      *** Please run python db_builder.py before python app.py if there is no foldover.db in /data ***
      -Enter password and username
            -If you do not have an account, press sign up to make one
      -Mystories display all stories you have ever edited
      -All stories display stories made by all users
      -Make a new story by adding your own tags (make sure to put a hashtag) and adding a title plus some content
      -Searching a story
            -You can search by using tags
            -You can search by using title
      -Clicking on a story that you haven't edited allows you to edit 
            -if someone else is editing you will be in queue
            -Editing only allows 600 characters and then it cuts off your text
            -Allows for html tags to make hypermark text
            -After editing, you can view full story
      -Clicking on a story that you have edited allows you to view full story
      -Edit Profile
            -Select what you want to change:
                  -Type in old and then new Username if you want to change username
                  -Type in old password, new password, and new password again if you want to change password
      -Closed stories can't be edited anymore (usually 200 edits unless Admin closes early)
      -Admin Power:
            -Can add and delete tags
            -Can close story so no one can edited anymore
            -Can delete story if content is inappropriate 
                  -story is still in mystories but clicking on it will show it has been deleted
     
## Possible Future Add-Ons:
      -Tell User how many edits left before closing
      -Make buttons for html editing on the story instead of making the user make tags
      -Actively count down words for word limit
      -Report inappropriate content
      -Allow non-admins to add tags
      -Countdown timer for queue

## Ayham - Prime Minister <br>
      - Apparently nothing 
## Amanda - Python Search and Monitor <br>
       - Searching by tags and titles to most efficently find the story requested by user. 
       - Monitoring the ip logs and disconnects through flasks environment variable tracking.
       - Updates a server side wait time. 
## Tiffany - HTML & Jinja Frontend <br>
       - Modifying UI and UX for the website 
       - Incorporates Jesse and Amanda's backend into the frontend 
## Jesse - Backend SQL <br>
      - Making a database builder file and combined with app.py
      - Made csv files to facililate external output into the program's input
