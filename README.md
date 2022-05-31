KNU SE-20221 Team Four
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
          git clone https://github.com/dohyungpark/KNUSE-20221-4-TeamFour.git
          ```
    3. Use the ***cd*** to move into the cloned directory.
          ```bash
         cd KNUSE-20221-4-TeamFour
         ```
---
  * ### Execute Program
       (***Windows*** needs to install ***Windows Subsystem for Linux*** for running ***Shell Script*** file.)
      * ## metric_counter.py
      1. Use the ***cd*** to move into **metric_counter**.
            ```bash
            cd metric_counter
            ```
      2. Enter the ***chmod*** command to change the permission of ***metric_counter.sh***.
            ```bash
            chmod 755 ./metric_counter.sh
            ```
      3. Run the program with ***in.file*** and ***out.file***. (The ***in.file*** must be written by ***python***.)
            ```bash
            ./metric_counter.sh in.py out.file
            ```
    
      * ## complexity_counter.py
      1. Use the ***cd*** to move into **complexity_counter**.
            ```bash
            cd complexity_counter
            ```
      2. Enter the ***chmod*** command to change the permission of ***complexity_counter.sh***.
            ```bash
            chmod 755 ./complexity_counter.sh
            ```
      3. Run the program with ***in.file*** and ***out.file***. (The ***in.file*** must be written by ***python***.)
            ```bash
            ./complexity_counter.sh complexity.sample out.file
            ```
       
      * ## oom_counter.py
      1. Use the ***cd*** to move into the **oom_counter**.
            ```bash
            cd oom_counter
            ```
      2. Enter the ***chmod*** command to change the permission of ***oom_counter.sh***.
            ```bash
            chmod 755 ./oom_counter.sh
            ```
      3. Run the program with ***in.file*** and ***out.file***. (The ***in.file*** must be written by ***python***.)
            ```bash
            ./oom_counter.sh oom.sample out.file
            ```
       
      * ## metric_tracker.py
      1. Use the ***cd*** to move into **metric_tracker**.
            ```bash
            cd metric_tracker
            ```
      2. Install the necessary packages.
            ```bash
            pip install pyyaml
            ```
            ```bash
            pip install gitpython
            ```
      3. Modify _**in.yaml**_ as in the format below. (You can also refer to sample(_**in.yaml**_) in **metric_tracker**.)
            ```yaml
            repository: YourTargetRepository
            target_path: YourTargetFilePath
            commits:
               - YourCommit1
               - YourCommit2
               - YourCommit3
                    ...
            ```
      4. Enter the _**chmod**_ command to change the permission of _**metric_counter.sh**_.
           ```bash
           chmod 755 ./metric_tracker.sh
           ```
      5. Run the program with _**in.yaml**_ and _**out.json**_.
            ```bash
            ./metric_tracker.sh in.yaml out.json
            ```
---
Language
--------
+ Implementation Language: Python
+ Target Language:   Python
---

About Sample Files
--------------------
+ The ***in.py*** file in ***metric_counter*** is a clone of \
https://github.com/kakao/khaiii/blob/918955f276c6cdddcc1a32e692618470cb571fa4/src/main/python/khaiii/khaiii.py
+ The ***complexity.sample*** file in ***complexity_counter*** is a clone of \
https://github.com/TheAlgorithms/Python/blob/629848e3721d9354d25fad6cb4729e6afdbbf799/data_structures/binary_tree/binary_search_tree.py
+ The ***oom.sample*** file in ***oom_counter*** is a clone of \
https://github.com/geekcomputers/Python/blob/f0af0c43340763724f139fa68aa1e5a9ffe458b4/BlackJack_game/blackjack_simulate.py
---
