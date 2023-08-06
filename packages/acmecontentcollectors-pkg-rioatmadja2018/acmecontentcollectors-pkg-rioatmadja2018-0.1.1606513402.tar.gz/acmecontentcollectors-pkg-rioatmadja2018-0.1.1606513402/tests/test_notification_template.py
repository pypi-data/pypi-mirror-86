#!/usr/bin/env python
from unittest import TestCase
from acme_collectors.utils.constants import NOTIFICATION_TEMPLATE
from uuid import uuid4
import os

class TestNotificationGeneration(TestCase):
    def test_file_generation(self):
        email: str = "admin@test.com"
        subject: str = "TEST TEMPLATE GENERATION".title()
        server_name: str = "admin_node"
        server_address: str = "127.0.0.1"
        message: str = "This is a test template"

        notification = NOTIFICATION_TEMPLATE % (email,
                                                subject,
                                                server_name,
                                                server_address,
                                                message)

        current_file: str = f"{str(uuid4())}.log"
        with open(current_file, 'w') as f:
            f.write(notification)
        f.close()

        self.assertEqual(os.path.exists(current_file) ,True)
