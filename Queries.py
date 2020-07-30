findLinkFromLinksByCategoryAndSourceAndDate = "SELECT link FROM `links_%s` WHERE category='%s' AND source='%s' AND date='%s'"
findDateFromTempLinksByLink = "SELECT date FROM `tempLinks` WHERE `link`='%s'"
findFromImgLinkByLink = "SELECT date, title, description, imgLink FROM `links_%s` WHERE `link`='%s'"

countFromLinksByLink = "SELECT COUNT(*) FROM `links_%s` WHERE link='%s'"

updateTempLink = "UPDATE `tempLinks` SET date=CURRENT_DATE() WHERE link='%s'"

insertTempLink = "INSERT INTO `tempLinks` VALUES(NULL, CURRENT_DATE()-1, '%s')"
insertLink = "INSERT INTO `links_%s` VALUES(NULL, CURRENT_DATE(), '%s', '%s', '%s', %d, %d, %d, '%s', '%s', '%s',0, NULL)"

createTableIfNotExistsForTempLinks = """
CREATE TABLE IF NOT EXISTS `tempLinks` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;"""

createTableIfNotExists = """CREATE TABLE IF NOT EXISTS `links_%s` (
`id` int(11) NOT NULL,
  `date` date NOT NULL,
  `category` varchar(32) NOT NULL,
  `source` varchar(255) NOT NULL,
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `tweetCount` int(11) NOT NULL,
  `facebookCount` int(11) NOT NULL,
  `googleCount` int(11) NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `imgLink` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `clickedCount` int(11) NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;"""

addPrimaryKeyToTable = "ALTER TABLE `%s` ADD PRIMARY KEY (`id`)"

addAutoIncrementToTable = "ALTER TABLE `%s` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT"