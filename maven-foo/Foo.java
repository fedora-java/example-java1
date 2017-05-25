package org.fedoraproject.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Foo {
    Logger logger = LoggerFactory.getLogger(Foo.class);

    public void doStuff() {
        logger.info("Doing stuff");
    }
}