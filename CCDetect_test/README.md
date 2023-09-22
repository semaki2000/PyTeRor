Clone CCDetect-lsp-pytest
https://github.com/semaki2000/CCDetect-lsp-pytest
Preconfigured to the 'right' settings in theory. 

Run make 
With the correct path, run ./cli path_to_master_refactoring_folder/master-refactoring/CCDetect_test 




Example output:
'''
Path: /mnt/c/skole/master/master-refactoring/CCDetect_test
Starting a Gradle Daemon (subsequent builds will be faster)

> Task :app:cli
Running CCDetect-LSP in CLI mode...
1 relevant files
Finding clones...
CodeClone(file:///mnt/c/skole/master/master-refactoring/CCDetect_test/calculator_type2.py
Range [
  start = Position [
    line = 4
    character = 0
  ]
  end = Position [
    line = 9
    character = 10
  ]
]
Matches 1
Match 1:
file:///mnt/c/skole/master/master-refactoring/CCDetect_test/calculator_type2.py
Range [
  start = Position [
    line = 15
    character = 0
  ]
  end = Position [
    line = 20
    character = 10
  ]
]
)

CodeClone(file:///mnt/c/skole/master/master-refactoring/CCDetect_test/calculator_type2.py
Range [
  start = Position [
    line = 22
    character = 4
  ]
  end = Position [
    line = 23
    character = 36
  ]
]
Matches 1
Match 1:
file:///mnt/c/skole/master/master-refactoring/CCDetect_test/calculator_type2.py
Range [
  start = Position [
    line = 11
    character = 4
  ]
  end = Position [
    line = 12
    character = 43
  ]
]
)

CodeClone(file:///mnt/c/skole/master/master-refactoring/CCDetect_test/calculator_type2.py
Range [
  start = Position [
    line = 15
    character = 0
  ]
  end = Position [
    line = 20
    character = 10
  ]
]
Matches 1
Match 1:
file:///mnt/c/skole/master/master-refactoring/CCDetect_test/calculator_type2.py
Range [
  start = Position [
    line = 4
    character = 0
  ]
  end = Position [
    line = 9
    character = 10
  ]
]
)

CodeClone(file:///mnt/c/skole/master/master-refactoring/CCDetect_test/calculator_type2.py
Range [
  start = Position [
    line = 11
    character = 4
  ]
  end = Position [
    line = 12
    character = 43
  ]
]
Matches 1
Match 1:
file:///mnt/c/skole/master/master-refactoring/CCDetect_test/calculator_type2.py
Range [
  start = Position [
    line = 22
    character = 4
  ]
  end = Position [
    line = 23
    character = 36
  ]
]
)

Found 4 clones

Deprecated Gradle features were used in this build, making it incompatible with Gradle 9.0.

You can use '--warning-mode all' to show the individual deprecation warnings and determine if they come from your own scripts or plugins.

See https://docs.gradle.org/8.1.1/userguide/command_line_interface.html#sec:command_line_warnings

BUILD SUCCESSFUL in 37s
3 actionable tasks: 1 executed, 2 up-to-date
Gradle command executed
'''