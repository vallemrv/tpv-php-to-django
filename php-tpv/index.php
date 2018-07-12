<?php
# @Author: Manuel Rodriguez <valle>
# @Date:   23-May-2018
# @Email:  valle.mrv@gmail.com
# @Last modified by:   valle
# @Last modified time: 21-Jun-2018
# @License: Apache license vesion 2.0


  // remove the following line when in production mode
defined('YII_DEBUG') or define('YII_DEBUG',true);
// include Yii bootstrap file
require_once('/Users/valle/opt/yii/yii.php');
// create application instance and run
$configFile=  dirname(__FILE__).'/protected/config/main.php';
Yii::createWebApplication($configFile)->run();

?>
