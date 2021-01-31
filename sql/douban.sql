use collie;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for douban book comments
-- ----------------------------
-- DROP TABLE IF EXISTS `comments`;
# CREATE TABLE `comments` (
#   `id` varchar(32) NOT NULL,
#   `book_id` varchar(32) NOT NULL,
#   `douban_id` int(10) unsigned NOT NULL DEFAULT '0',
#   `douban_comment_id` int(10) unsigned NOT NULL DEFAULT '0',
#   `douban_user_nickname` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `douban_user_avatar` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `douban_user_url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
#   `votes` int(10) unsigned NOT NULL DEFAULT '0',
#   `rating` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `comment_time` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`),
#   KEY `comments_book_id_index` (`book_id`),
#   KEY `comments_douban_id_index` (`douban_id`),
#   KEY `comments_douban_comment_id_index` (`douban_comment_id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ----------------------------
-- Table structure for douban book reviews
-- ----------------------------
# DROP TABLE IF EXISTS `reviews`;
# CREATE TABLE `reviews` (
#   `id` varchar(32) NOT NULL,
#   `book_id` varchar(32) NOT NULL,
#   `douban_id` int(10) unsigned NOT NULL DEFAULT '0',
#   `douban_review_id` int(10) unsigned NOT NULL DEFAULT '0',
#   `douban_review_title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `douban_user_nickname` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `douban_user_avatar` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `douban_user_url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `content` text COLLATE utf8mb4_unicode_ci NOT NULL,
#   `useful_count` int(10) unsigned NOT NULL DEFAULT '0',
#   `useless_count` int(10) unsigned NOT NULL DEFAULT '0',
#   `rating` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `review_time` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
#   `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (`id`),
#   KEY `reviews_book_id_index` (`book_id`),
#   KEY `reviews_douban_id_index` (`douban_id`),
#   KEY `reviews_douban_review_id_index` (`douban_review_id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------
-- Table structure for review_exception
-- ----------------------------
DROP TABLE IF EXISTS `review_exception`;
CREATE TABLE `review_exception` (
  `url` varchar(255) NOT NULL,
  `status` int(10) unsigned NOT NULL DEFAULT '0',
  `flag` int(10) unsigned NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`url`),
  KEY `review_exception_url_index` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;