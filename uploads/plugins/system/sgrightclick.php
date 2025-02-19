<?php

/**
 * @version		$Id: sgrightclick.php 2010-03-29 16:03:10 val $
 * @package		SGRightClick
 * @subpackage	System
 * @copyright	Copyright (C)2010 SiteGround.com - All Rights Reserved.
 * @author		Val Markov <val@siteground.com>
 * @version		1.0.7
 * @license		GNU/GPL, see LICENSE
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>
 *
 * This version may have been modified pursuant
 * to the GNU General Public License, and as distributed it includes or
 * is derivative of works licensed under the GNU General Public License or
 * other free or open source software licenses.
 * See LICENSE for more details.
 */
// no direct access
defined('_JEXEC') or die('Restricted access');

jimport('joomla.plugin.plugin');

class plgSystemSgrightclick extends JPlugin {

    /**
     * Constructor. PHP4 Compatibility.
     * @param $subject
     * @param $config
     * @return void
     */
    function plgSystemSgrightclick(&$subject, $config) {
        parent::__construct($subject, $config);
        $this->_plugin = JPluginHelper::getPlugin('system', 'sgrightclick');
        $this->_params = new JParameter($this->_plugin->params);
    }

    function onAfterRender() {

        $output = JResponse::getBody();
        if (!(preg_match("/sgfooter/", $output))) {
            $pattern = '/<\/body>/';
            $replacement = "<center><span class='modifydate' id='sgfooter' style='padding: 5px;'></span><center></body>";
            $output = preg_replace($pattern, $replacement, $output, 1);
        }
        JResponse::setBody($output);
        return true;
    }

    /**
     * Adds JS code to avoid novice visitors from right-clicking on the page.
     * This is not a solution, but work-around and 'advanced' visitors will still be able to see the content.
     *
     * @return void
     */
    function onAfterInitialise() {
        global $mainframe;
        if ($this->params->get('allow_admin')) {
            //Halt execution here because the logged-in person is in administrators area.
            if ($mainframe->isAdmin()) {
                return;
            }
        }
        /* Generate the JScript code */
        $js = '<!--
			
		var message="' . $this->params->get('errmsg') . '";
		
		function clickIE4(){
		if (event.button==2){
		alert(message);
		return false;
		}
		}
		
		function clickNS4(e){
		if (document.layers||document.getElementById&&!document.all){
		if (e.which==2||e.which==3){
		alert(message);
		return false;
		}
		}
		}
		
		if (document.layers){
		document.captureEvents(Event.MOUSEDOWN);
		document.onmousedown=clickNS4;
		}
		else if (document.all&&!document.getElementById){
		document.onmousedown=clickIE4;
		}
		
		document.oncontextmenu=new Function("alert(message);return false")
		
		// -->';

        $page = & JFactory::getDocument();

        /* Check for Logged in users */
        if ($this->params->get('allow_users')) {
            $user = & JFactory::getUser();
            if ($user->guest) {
                //User is not user.. adding JS.
                $page->addScriptDeclaration($js);
            } // Else: user is user ;) Skipping JS.
        } else {
            // No difference should be made between users, displaying JS:
            $page->addScriptDeclaration($js);
        }
    }

}

/* End of plugins/system/sgrightclick.php */
