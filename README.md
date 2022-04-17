KNU SE-20221 Team Four: LOC Metrics Counter
============================================

How To Run Program
---------------------
* ### Environment
   1. Check python version
         ```bash
          python --version
         ```
         or
         ```bash
          python3 --version
         ```
   2. If python version lower than 3, then install ***python3***.
  
  + Linux
     + On Debian derivatives such as Ubuntu, use apt.
          ```bash
           sudo apt-get install python3
          ```
     + On Red Hat and derivatives, use yum.
          ```bash
           sudo yum install python3
          ```
     + On SUSE and derivatives, use zypper.
          ```bash
           sudo zypper install python3
          ```
  + Mac OS
  
     Download link: https://www.python.org/downloads/macos/
  
  + Windows
  
     Download link: https://www.python.org/downloads/windows/
---
* ### Clone
    1. Use the ***cd*** to move into the directory where you want to save the clone. For example:
         ```bash
           cd YourDirectoryForClone
         ```
    2. Enter the ***git clone URL*** command.
          ```bash
           git clone https://github.com/dexherodex/KNUSE-20221-6.git
          ```
---
* ### Execute Program
     (***Windows*** needs to install ***Windows Subsystem for Linux*** for running ***Shell Script*** file.)
    1. Use the ***cd*** to move into the cloned directory. For example:
          ```bash
           cd ClonedDirectory
          ```
    2. Enter the ***chmod*** command to change the permission of ***metric_counter.sh***.
          ```bash
           chmod 755 ./metric_counter.sh
          ```
    3. Run the program with ***in.file*** and ***out.file***. (The ***in.file*** must be written by ***python***.) For example:
          ```bash
           ./metric_counter.sh in.file out.file
          ```
---
Language
--------
+ Implementation Language: Python
+ Target Language:   Python
---

About Sample "***in.py***"
--------------------
+ The ***in.py*** file is a clone of https://github.com/kakao/khaiii/blob/master/src/main/python/khaiii/khaiii.py
---