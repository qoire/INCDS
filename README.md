INCDS
=====

Repository for ECE496 Team tackling INCDS (Interactive Noise Cancellation Demo System)

Hi guys, I'm not sure if you're new to git but its pretty easy. (With the git clients)

##Installation Instructions on Windows

Grab a git client from:
https://windows.github.com/
or
https://mac.github.com/

or use a CVS client of your liking. 

##Some basic git concepts
###Cloning:
Cloning refers to the act of "cloning" a repository (in this case this one here) to your
local drive, much like how "svn checkout" works
###Pulling:
Executing a git pull means that you're syncing your current git repository
with the origin repository and merging them together, (think svn) there may be cases
where conflicts arise.
###Adding:
Similar to svn adding in git means adding new files to the stage. You must "add" new files
to the repository for them to be under version control.

Note that you must "add" files to the stage before you can commit them, if you've modified a file
but haven't added it to the stage, git won't commit that change.
###Removing:
Self explanatory
###Committing:
Committing is different compared to svn commit, commit means you've commited a change to your local repository.
To make the change appear on the network (to let us see your change and sync to it) you must perform a git push.
###Pushing:
Pushing is the act of pushing your change to the origin repository (here) you can commit multiple times before
pushing your changes with the origin repository (here). 
