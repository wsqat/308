-- MySQL dump 10.13  Distrib 5.7.19, for macos10.12 (x86_64)
--
-- Host: localhost    Database: anchor_db
-- ------------------------------------------------------
-- Server version	5.7.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `anchor`
--

DROP TABLE IF EXISTS `anchor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anchor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userName` varchar(100) DEFAULT NULL,
  `avatar` text,
  `roomName` varchar(100) DEFAULT NULL,
  `plateform` varchar(100) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `fans` varchar(100) DEFAULT NULL,
  `reward` varchar(100) DEFAULT NULL,
  `roomUrl` varchar(200) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `keywords` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anchor`
--

LOCK TABLES `anchor` WRITE;
/*!40000 ALTER TABLE `anchor` DISABLE KEYS */;
INSERT INTO `anchor` VALUES (1,'White55开解说','https://apic.douyucdn.cn/upload/avanew/face/201612/30/02/c14ddc0a4d121d32fc5d150f0e97448b_big.jpg?rltime?rltime','对不起各位，再给我休息两天，爱你们','斗鱼','英雄联盟','12739520','807320.0','http://www.douyu.com/138286','20171101','卢本伟 牛逼 表面兄弟 凉凉'),(2,'冯提莫','https://apic.douyucdn.cn/upload/avanew/face/201710/13/19/cbfc90cd87d88c263776a5f1c528480f_big.jpg?rltime?rltime','冯提莫：唱会歌玩儿什么游戏呢？','斗鱼','英雄联盟','10392150','836130.0','http://www.douyu.com/71017','20171101','好听 一米五 人美歌甜 活泼可爱'),(3,'芜湖大司马丶','https://apic.douyucdn.cn/upload/avatar/face/201609/08/f6c0c08a3f3cb1fd074fe38907ae2508_big.jpg?rltime?rltime','大司马：我只能说再战一年，坚信可以','斗鱼','英雄联盟','9128445','195600.0','http://www.douyu.com/606118','20171101','真皮沙发 皮皮 弱智 老师'),(4,'陈一发儿','https://apic.douyucdn.cn/upload/avatar/002/28/65/01_avatar_big.jpg?rltime?rltime','陈一发儿：周一不播哟~','斗鱼','主机游戏','7634846','885580.0','http://www.douyu.com/67373','20171101','一发 关注 超级 话题'),(5,'老实敦厚的笑笑','https://apic.douyucdn.cn/upload/avanew/face/201706/29/20/64b39bcf6c3e3e46972258a26d5b78df_big.jpg?rltime?rltime','德云色 恰鸡冲前10！！！','斗鱼','英雄联盟','6031669','509840.0','http://www.douyu.com/154537','20171101','秃秃秃秃 老油子 办卡 德云色'),(6,'即将拥有人鱼线的PDD','http://i6.pdim.gs/fe6c1edaa50f1ae3f346f0452a9254ed.jpeg','北京鸽了 明天回来直播','熊猫','英雄联盟','5845141','1254858.968','https://www.panda.tv/6666','20171101','末日 人机 老师 渔夫'),(7,'指法芬芳张大仙','https://apic.douyucdn.cn/upload/avanew/face/201708/03/12/8768fecb8233437a579dc932d7f0a21c_big.jpg?rltime?rltime','御剑乘风来，除魔天地间，我是大仙','斗鱼','王者荣耀','5578728','70840.0','http://www.douyu.com/688','20171101','大仙 没人 哈哈哈 学校'),(8,'英雄联盟官方赛事','https://apic.douyucdn.cn/upload/avanew/face/201709/05/20/1f3ce55829bc50da263a938bd81aebfc_big.jpg','S7半决赛 WEvsSSG 重播','斗鱼','英雄联盟','4116078','44160.0','http://www.douyu.com/288016','20171101','关注 不亏 lpl LPL'),(9,'主播油条','https://apic.douyucdn.cn/upload/avatar/001/00/17/26_avatar_big.jpg?rltime?rltime','条:空头流双持M24近战红点狙？？？','斗鱼','绝地求生','4112368','668820.0','http://www.douyu.com/56040','20171101','喷子 15 油条 科技'),(10,'Misaya若风lol','http://i1.pdim.gs/t019b937b40d8b95c41.jpg','若风：31号中午左右开播','熊猫','绝地求生','3958533','613817.968','https://www.panda.tv/666666','20171101','亚索 风队 男人 miss'),(11,'七哥张琪格','https://apic.douyucdn.cn/upload/avanew/face/201703/15/02/8f8792bfd7e8ccc29ce69ea35298f7d8_big.jpg?rltime?rltime','萝莉控请进来！！！','斗鱼','炉石传说','3708507','223480.0','http://www.douyu.com/65251','20171101','emot 牌子 多人 换个'),(12,'东北大鹌鹑','https://apic.douyucdn.cn/upload/avanew/face/201610/17/19/b1060e87c9d17bd37e22c6a63818f07e_big.jpg?rltime?rltime','东北大鹌鹑 宇宙第一寒冰 相声艺术家！','斗鱼','英雄联盟','3618550','432260.0','http://www.douyu.com/96291','20171101','生日快乐 鹌鹑 山驴 生日'),(13,'韦神','https://apic.douyucdn.cn/upload/avatar/face/201606/27/11d6864e4e6437c95af780abe1862e30_big.jpg?rltime?rltime','o(*￣▽￣*)ブbiubiubiu','斗鱼','绝地求生','3592590','95140.0','http://www.douyu.com/7911','20171101','节奏 谢谢 今天 大气'),(14,'洞主丨歌神洞庭湖','https://apic.douyucdn.cn/upload/avanew/face/201708/23/22/7de486706f57f007704560894ea4f7d5_big.jpg?rltime?rltime','你的肉体我的心.歌神洞庭湖~','斗鱼','英雄联盟','3013718','170680.0','http://www.douyu.com/138243','20171101','真皮沙发 弱智 真皮 主播'),(15,'饼干狂魔MasterB','https://apic.douyucdn.cn/upload/avatar/000/18/41/65_avatar_big.jpg?rltime?rltime','滑板鞋打野！秘技：反复横跳！！','斗鱼','英雄联盟','2996252','498960.0','http://www.douyu.com/4809','20171101','i7 才会赢 饼干 大家'),(16,'阿冷aleng丶','https://apic.douyucdn.cn/upload/avanew/face/201710/27/15/30bfcb5821ced2bb6898fedc8ca8f38e_big.jpg?rltime?rltime','点击领取一个阿冷~','斗鱼','英雄联盟','2954324','92020.0','http://www.douyu.com/2371789','20171101','一天 冷冷 愿得 200'),(17,'周二珂','http://i7.pdim.gs/dmfd/200_200_100/0257040380bd7d294a8017532c07e39b.jpg','快递小妹~','熊猫','绝地求生','2853834','516386.122','https://www.panda.tv/35723','20171101','今天 今晚 开播 5000'),(18,'guoyun丶mini','https://apic.douyucdn.cn/upload/avanew/face/201710/24/02/ebbc31c0828e2573aa114e7be0be7f43_big.jpg?rltime?rltime','【年度抽奖送送送】最后一天，谢谢大家支持','斗鱼','炉石传说','2651397','280590.0','http://www.douyu.com/10903','20171101','古风女神 郭老师 送送送 抽奖'),(19,'我叫撸管飞','https://apic.douyucdn.cn/upload/avanew/face/201710/20/23/aa26204b7967594b01fa5d4c1c8bb8ee_big.jpg','国服第一风暴诺克！光速血怒！','斗鱼','英雄联盟','2601887','202360.0','http://www.douyu.com/453751','20171101','i7 韩服 主播 白银'),(20,'嗨氏','https://apic.douyucdn.cn/upload/avanew/face/201708/26/21/15f974b260c643688cd5b83480d19ccf_big.jpg?rltime?rltime','【嗨氏】晋级赛有毒','斗鱼','王者荣耀','2577457','21670.0','http://www.douyu.com/1229','20171101','疯狂 call 海涛 哥哥');
/*!40000 ALTER TABLE `anchor` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-01 13:09:00
