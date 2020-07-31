findLinkFromLinksByCategoryAndDomainAndDate = "SELECT link FROM `links_%s` WHERE category='%s' AND domain='%s' AND date='%s'"
findDateFromLinkCacheByLink = "SELECT date FROM `link_cache` WHERE `link`='%s'"
findFromImgLinkByLink = "SELECT date, title, description, image FROM `links_%s` WHERE `link`='%s'"

countFromLinksByLink = "SELECT COUNT(*) FROM `links_%s` WHERE link='%s'"

updateTempLink = "UPDATE `link_cache` SET date=CURRENT_DATE() WHERE link='%s'"

insertTempLink = "INSERT INTO `link_cache` VALUES(NULL, CURRENT_DATE()-1, '%s')"
insertLink = "INSERT INTO `links_%s` VALUES(NULL, CURRENT_DATE(), '%s', '%s', '%s', '%s', '%s', '%s', 0, NOW())"

createTableIfNotExistsForLinkCache = """
CREATE TABLE IF NOT EXISTS `link_cache` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;"""

createTableIfNotExists = """CREATE TABLE IF NOT EXISTS `links_%s` (
`id` int(11) NOT NULL,
  `date` date NOT NULL,
  `category` varchar(32) NOT NULL,
  `domain` varchar(255) NOT NULL,
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(1024) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `clicked` int(11) NOT NULL DEFAULT '0',
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;"""

addPrimaryKeyToTable = "ALTER TABLE `%s` ADD PRIMARY KEY (`id`)"

addAutoIncrementToTable = "ALTER TABLE `%s` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT"