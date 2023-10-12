/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - mental_health
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`mental_health` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `mental_health`;

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `booking_id` int(11) NOT NULL AUTO_INCREMENT,
  `bdate` varchar(50) DEFAULT NULL,
  `btime` varchar(50) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `sched_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`booking_id`,`bdate`,`btime`,`userid`,`sched_id`) values 
(1,'2023-05-06','15:36:53',4,1);

/*Table structure for table `complaints` */

DROP TABLE IF EXISTS `complaints`;

CREATE TABLE `complaints` (
  `comp_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `complaint` varchar(200) DEFAULT NULL,
  `reply` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`comp_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `complaints` */

insert  into `complaints`(`comp_id`,`user_id`,`date`,`complaint`,`reply`) values 
(1,4,'2023-05-06','delay in response','ok we will fix it');

/*Table structure for table `health_state` */

DROP TABLE IF EXISTS `health_state`;

CREATE TABLE `health_state` (
  `health_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `time` varchar(50) DEFAULT NULL,
  `health_state` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`health_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `health_state` */

insert  into `health_state`(`health_id`,`user_id`,`date`,`time`,`health_state`) values 
(1,4,'2023-05-06','16:14:35','Neutral');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `usertype` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values 
(1,'admin@gmail.com','12341234','admin'),
(2,'smi123@gmail.com','123456','psychiatrist'),
(3,'prajitha@gmail.com','123456','rejected'),
(4,'priya123@gmail.com','priya123','user'),
(5,'navya123@gmail.com','123navya','user');

/*Table structure for table `patient` */

DROP TABLE IF EXISTS `patient`;

CREATE TABLE `patient` (
  `patient_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `psych_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`patient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `patient` */

insert  into `patient`(`patient_id`,`date`,`user_id`,`psych_id`,`status`) values 
(2,'2023-05-06',4,2,'accepted');

/*Table structure for table `psychiatrist` */

DROP TABLE IF EXISTS `psychiatrist`;

CREATE TABLE `psychiatrist` (
  `psych_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `qualification` varchar(100) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`psych_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `psychiatrist` */

insert  into `psychiatrist`(`psych_id`,`name`,`place`,`email`,`phone`,`qualification`,`image`) values 
(2,'smitha','ksd','smi123@gmail.com','9876788888','mbbs','/static/psych_img/20230506_152331.jpg'),
(3,'prajitha','kasaragod','prajitha@gmail.com','9876543211','MBBS','/static/psych_img/20230506_152448.jpg');

/*Table structure for table `schedule` */

DROP TABLE IF EXISTS `schedule`;

CREATE TABLE `schedule` (
  `sched_id` int(11) NOT NULL AUTO_INCREMENT,
  `psych_id` int(11) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `from_time` varchar(50) DEFAULT NULL,
  `to_time` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`sched_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `schedule` */

insert  into `schedule`(`sched_id`,`psych_id`,`date`,`from_time`,`to_time`) values 
(1,2,'2023-05-07','09:00','10:30'),
(2,2,'2023-05-08','10:00','11:00');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `photo` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`name`,`email`,`phone`,`photo`) values 
(4,'priya','priya123@gmail.com','9207231367','/static/user_imgs/20230506_152539.jpg'),
(5,'navya','navya123@gmail.com','9496123456','/static/user_imgs/20230506_152624.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
