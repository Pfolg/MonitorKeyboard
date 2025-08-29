cmake_minimum_required(VERSION 3.16)

project(KeyMonitor VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets Core Gui Widgets Network REQUIRED)
qt_standard_project_setup()

qt_add_executable(KeyMonitor
        main.cpp
        globalinputlistener.cpp
        globalinputlistener.h
        convertcodetostring.cpp
        convertcodetostring.h
        window.h
        window.cpp
)
target_link_libraries(KeyMonitor PRIVATE Qt${QT_VERSION_MAJOR}::Widgets Qt6::Core Qt6::Gui Qt6::Widgets Qt6::Network user32)

set_target_properties(KeyMonitor PROPERTIES
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

include(GNUInstallDirs)
install(TARGETS KeyMonitor
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
