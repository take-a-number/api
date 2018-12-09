# api
Python Django REST API for Take a Number. Supports the Front End of Take a Number, which maintains a
queue designed for university TA sessions.

[![Build Status](https://travis-ci.org/vanderbilt-design-studio/your-print-is-ready.svg?branch=master)](https://travis-ci.org/take-a-number/api)
[![Coverage Status](https://coveralls.io/repos/github/vanderbilt-design-studio/your-print-is-ready/badge.svg?branch=master)](https://coveralls.io/github/take-a-number/api?branch=master)  

# Potential Future Features
* Mechanism to indicate that a TA is now finished helping students
* Ability to insert students to arbitrary locations in the queue
* Storage of course information such as office hour schedules
* Role-based access with differeing permissions for admins vs. professors vs. students
* Integration with Vanderbilt SSO
	* Parsing of information from Brightspace
	* Automatic generation of courses based on registration
* Addition of notifications as queue status changes
	* Text messages (potentially through Twilio)
	* Emails
* Addition of universities besides Vanderbilt
* Different approach to keeping track of users (current approach is a cookie)
