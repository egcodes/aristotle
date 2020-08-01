findCachedLinksByDomain = "SELECT link FROM `link_cache` WHERE domain='%s'"

insertCacheLink = "INSERT INTO `link_cache` VALUES(NULL, '%s', '%s')"

insertLink = """
INSERT INTO `links_%s` (id,date,category,domain,link,title,description,image,clicked,timestamp)
SELECT * FROM (SELECT NULL, CURRENT_DATE(), '%s', '%s', '%s', '%s' as a, '%s' as b, '%s', 0, NOW()) AS tmp
WHERE NOT EXISTS (
    SELECT link FROM links_%s WHERE domain='%s' and link = '%s'
) LIMIT 1;
"""

truncateCache = "TRUNCATE `link_cache`"

checkTableIsExists = "SELECT id FROM `%s` LIMIT 1"

createTableIfNotExistsForLinkCache = """
CREATE TABLE IF NOT EXISTS `link_cache` (
  `id` int(11) NOT NULL,
  `domain` varchar(255) NOT NULL,
  `link` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;"""

createTableIfNotExists = """
CREATE TABLE IF NOT EXISTS `links_%s` (
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
