# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    javaVersionCommand = "java -version"
    os.system(javaVersionCommand)

    jdkSetCommand = "export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_291.jdk/Contents/Home"
    os.system(jdkSetCommand)
    print("new version")
    javaVersionCommand = "java -version"
    os.system(javaVersionCommand)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
