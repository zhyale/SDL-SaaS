BEGIN;
CREATE TABLE `remindmgmt_remind_receivers` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `remind_id` integer NOT NULL,
    `user_id` integer NOT NULL,
    UNIQUE (`remind_id`, `user_id`)
)
;
ALTER TABLE `remindmgmt_remind_receivers` ADD CONSTRAINT `user_id_refs_id_89c8d463` FOREIGN KEY (`user_id`) REFERENCES `usermgmt_user` (`id`);
CREATE TABLE `remindmgmt_remind` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `create_time` datetime(6) NOT NULL,
    `create_user_id` integer NOT NULL,
    `title` varchar(256) NOT NULL,
    `content` varchar(1024),
    `extra_recipient` varchar(254),
    `remind_method` varchar(16) NOT NULL,
    `is_finished` bool NOT NULL,
    `finish_time` datetime(6) NOT NULL
)
;
ALTER TABLE `remindmgmt_remind` ADD CONSTRAINT `create_user_id_refs_id_d20c9e52` FOREIGN KEY (`create_user_id`) REFERENCES `usermgmt_user` (`id`);
ALTER TABLE `remindmgmt_remind_receivers` ADD CONSTRAINT `remind_id_refs_id_d6acba0a` FOREIGN KEY (`remind_id`) REFERENCES `remindmgmt_remind` (`id`);
CREATE TABLE `remindmgmt_deadlineremind` (
    `remind_ptr_id` integer NOT NULL PRIMARY KEY,
    `deadline_time` datetime(6)
)
;
ALTER TABLE `remindmgmt_deadlineremind` ADD CONSTRAINT `remind_ptr_id_refs_id_011e37d2` FOREIGN KEY (`remind_ptr_id`) REFERENCES `remindmgmt_remind` (`id`);
CREATE TABLE `remindmgmt_periodremind` (
    `remind_ptr_id` integer NOT NULL PRIMARY KEY,
    `first_remind_time` datetime(6) NOT NULL,
    `interval_seconds` integer NOT NULL,
    `expire_time` datetime(6) NOT NULL
)
;
ALTER TABLE `remindmgmt_periodremind` ADD CONSTRAINT `remind_ptr_id_refs_id_2aafdf97` FOREIGN KEY (`remind_ptr_id`) REFERENCES `remindmgmt_remind` (`id`);
CREATE TABLE `remindmgmt_onetimeremind` (
    `remind_ptr_id` integer NOT NULL PRIMARY KEY,
    `remind_time` datetime(6) NOT NULL
)
;
ALTER TABLE `remindmgmt_onetimeremind` ADD CONSTRAINT `remind_ptr_id_refs_id_6bea32eb` FOREIGN KEY (`remind_ptr_id`) REFERENCES `remindmgmt_remind` (`id`);
CREATE TABLE `remindmgmt_remindlog` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `log_time` datetime(6) NOT NULL,
    `remind_id` integer NOT NULL,
    `seconds_delta` integer NOT NULL
)
;
ALTER TABLE `remindmgmt_remindlog` ADD CONSTRAINT `remind_id_refs_id_832960cf` FOREIGN KEY (`remind_id`) REFERENCES `remindmgmt_remind` (`id`);
CREATE INDEX `remindmgmt_remind_receivers_9dc9f178` ON `remindmgmt_remind_receivers` (`remind_id`);
CREATE INDEX `remindmgmt_remind_receivers_6340c63c` ON `remindmgmt_remind_receivers` (`user_id`);
CREATE INDEX `remindmgmt_remind_d8b25398` ON `remindmgmt_remind` (`create_user_id`);
CREATE INDEX `remindmgmt_remindlog_9dc9f178` ON `remindmgmt_remindlog` (`remind_id`);

COMMIT;
