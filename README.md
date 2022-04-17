KNU SE-20221 LOC Metrics Counter
==================================

How To Run Program
---------------------
* ### Environment
   1. #### Check python version
          $ python --version
         #### or
          $ python3 --version
   2. #### If python version lower than 3, then install ***python3***.
  + #### Linux Terminal
     + #### On Debian derivatives such as Ubuntu, use apt.
           $ sudo apt-get install python3
     + #### On Red Hat and derivatives, use yum.
           $ sudo yum install python3
     + #### On SUSE and derivatives, use zypper.
           $ sudo zypper install python3
  + #### Mac OS Terminal
     #### Download link: https://www.python.org/downloads/macos/
  + #### Windows
     #### Download link: https://www.python.org/downloads/windows/
* ### Clone
    1. #### Use the ***cd*** to move into the directory where you want to save the clone. For example:
           $ cd YourDirectoryForClone
    2. #### Enter the ***git clone URL*** command.
           $ git clone https://github.com/dexherodex/KNUSE-20221-6.git

* ### Execute Program
     #### (***Windows*** needs to install ***Windows Subsystem for Linux*** for running ***Shell Script*** file.)
    1. #### Use the ***cd*** to move into the cloned directory. For example:
           $ cd ClonedDirectory
    2. #### Enter the ***chmod*** command to change the permission of ***metric_counter.sh***.
           $ chmod 755 ./metric_counter.sh
    3. #### Run the program with ***in.file*** and ***out.file***. For example:
           $ ./metric_counter.sh in.file out.file
       (The ***in.file*** must be written by ***python***) 

Language
--------
+ #### Implementation Language: Python
+ #### Target Language:   Python
