-- ./init/init-datahub.sql

CREATE DATABASE IF NOT EXISTS `datahub` CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
USE `datahub`;

-- 创建 metadata_aspect_v2 表
CREATE TABLE IF NOT EXISTS metadata_aspect_v2 (
  urn VARCHAR(500) NOT NULL,
  aspect VARCHAR(200) NOT NULL,
  version BIGINT(20) NOT NULL,
  metadata LONGTEXT NOT NULL,
  systemmetadata LONGTEXT,
  createdon DATETIME(6) NOT NULL,
  createdby VARCHAR(255) NOT NULL,
  createdfor VARCHAR(255),
  CONSTRAINT pk_metadata_aspect_v2 PRIMARY KEY (urn, aspect, version),
  INDEX timeIndex (createdon)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

-- 插入默认记录
INSERT INTO metadata_aspect_v2 (urn, aspect, version, metadata, createdon, createdby) VALUES
('urn:li:corpuser:datahub', 'corpUserInfo', 0, '{"displayName":"Data Hub","active":true,"fullName":"Data Hub","email":"datahub@linkedin.com"}', NOW(), 'urn:li:corpuser:__datahub_system'),
('urn:li:corpuser:datahub', 'corpUserEditableInfo', 0, '{"skills":[],"teams":[],"pictureLink":"https://raw.githubusercontent.com/datahub-project/datahub/master/datahub-web-react/src/images/default_avatar.png"}', NOW(), 'urn:li:corpuser:__datahub_system');

-- 创建 metadata_index 表（根据需要添加表结构定义）
CREATE TABLE IF NOT EXISTS metadata_index (
  -- 表结构定义
) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;

