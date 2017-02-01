USE sidecar;
GO

-- Create the project_tests_list table
CREATE TABLE `project_tests_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `test_status` int(11) DEFAULT NULL,
  `test_create_time` datetime NOT NULL,
  `extra` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create the test_config table
CREATE TABLE `test_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `option_name` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  `project_id` int(11) NOT NULL,
  `test_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create the tests_list table
CREATE TABLE `tests_list` (
  `id` varchar(100) NOT NULL,
  `name` varchar(200) NOT NULL,
  `project_id` int(11) DEFAULT NULL,
  `test_service` varchar(200) NOT NULL,
  `test_scenario` varchar(100) NOT NULL,
  `test_regex` varchar(300) NOT NULL,
  `test_added` int(11) DEFAULT NULL,
  `test_verified` varchar(100) DEFAULT NULL,
  `test_create_time` datetime NOT NULL,
  `test_uuid` varchar(200) DEFAULT NULL,
  `results` longtext
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create the tests_log table
CREATE TABLE `tests_log` (
  `id` varchar(100) NOT NULL,
  `log_data` longtext NOT NULL,
  `results` longtext NOT NULL,
  `project_id` varchar(100) NOT NULL,
  `test_status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Create the test_history table
CREATE TABLE `test_history` (
  `id` varchar(100) NOT NULL,
  `testlist_id` varchar(100) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  `history_create_time` datetime NOT NULL,
  `results` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

GO

-- Inserting the Tests into the DB
INSERT into project_tests_list VALUES(1, 'All Tests', 1, '2016-12-05 20:47:47', 'NULL');
INSERT into project_tests_list VALUES(2, 'Benchmark Tests', 1, '2016-12-05 20:47:47', 'NULL');
INSERT into project_tests_list VALUES(3, 'Quick QA', 1, '2016-12-05 20:47:47', 'NULL');

-- Inserting the Test data
INSERT INTO `test_config` VALUES (1,'image_name','cirros',1,1),(2,'flavor_name','m1.tiny',1,1);
INSERT INTO `test_config` VALUES (3,'image_name','cirros',2,1),(4,'flavor_name','m1.tiny',2,1);
INSERT INTO `test_config` VALUES (5,'image_name','cirros',3,1),(6,'flavor_name','m1.tiny',3,1);
INSERT INTO `tests_log` VALUES (1,'test-log','test-result',1,1),(2,'test-log','test-result',2,1), (3,'test-log','test-result',3,1);
UPDATE tests_list SET test_added = 0;

GO
