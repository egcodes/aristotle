truncateCache = "TRUNCATE TABLE `link_cache`"

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
