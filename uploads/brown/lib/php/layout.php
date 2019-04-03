<?php
/**		LAYOUT SETUP  - Copyright JoomSpirit 2009**/
// no direct accessdefined('_JEXEC') or die('Restricted access');
$topmodules = 0;if ($this->countModules('user1')) $topmodules++;if ($this->countModules('user2')) $topmodules++;if ($this->countModules('user3')) $topmodules++;
if ( $topmodules == 3 ) {$user_top_width = '31%';} else if ($topmodules == 2){$user_top_width = '47%';}else if ($topmodules == 1) {$user_top_width = '99%';}
$bottommodules = 0;if ($this->countModules('user4')) $bottommodules++;if ($this->countModules('user5')) $bottommodules++;if ($this->countModules('user6')) $bottommodules++;if ( $bottommodules == 3 ) {$user_bottom_width = '31%';} else if ($bottommodules == 2){$user_bottom_width = '47%';}else if ($bottommodules == 1) {$user_bottom_width = '99%';}
$copy='<div style="display:none;text-indent:-9999px;font-size:0;line-height:0;"><a href="http://www.joomspirit.fr" alt="webmaster freelance">webmaster freelance</a></div>';
?>