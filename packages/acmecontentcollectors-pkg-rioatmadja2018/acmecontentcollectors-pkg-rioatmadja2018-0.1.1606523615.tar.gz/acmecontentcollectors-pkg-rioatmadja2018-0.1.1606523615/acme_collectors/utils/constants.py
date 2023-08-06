#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: November 25, 2020
Description: Constant script
"""

# Create table query
CREATE_TABLE: str = """
    CREATE TABLE `justpasteit_posts` (
        `post_id` INT(11) NOT NULL AUTO_INCREMENT, 
        `date_created` TEXT, 
        `post_modified` TEXT, 
        `number_views` VARCHAR(255), 
        `url` VARCHAR(255),
        `image_url` TEXT, 
        `language` VARCHAR(255), 
        `posts` LONGTEXT , 
        PRIMARY KEY (post_id) 
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

# Notification template
NOTIFICATION_TEMPLATE: str = """
To: %s
From: dscnotifier@gmail.com  
Subject: %s

NOTIFICATION 
--------------------------------
Server Name: %s
Server Address: %s
--------------------------------

MESSAGE
--------------------------------
%s
"""

