#include <iostream>
#include <memory>

#include <log4cplus/configurator.h>
#include <log4cplus/consoleappender.h>
#include <log4cplus/logger.h>
#include <log4cplus/loggingmacros.h>
#include <log4cplus/loglevel.h>

int main() {
    log4cplus::initialize();

    log4cplus::SharedAppenderPtr appender(new log4cplus::ConsoleAppender());
    appender->setLayout(std::auto_ptr<log4cplus::Layout>(new log4cplus::PatternLayout(
        LOG4CPLUS_TEXT("%d{%Y-%m-%d %H:%M:%S.%q} %-5p [%i.%t] %c@%b:%L - %m%n"))));

    log4cplus::Logger rootLogger = log4cplus::Logger::getRoot();
    rootLogger.addAppender(appender);


    LOG4CPLUS_INFO(rootLogger, LOG4CPLUS_TEXT("Test output"));
}
