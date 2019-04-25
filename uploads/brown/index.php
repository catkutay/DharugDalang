<?php

/**
 * @copyright	Copyright (C) 2009 - JoomSpirit. All rights reserved.
 */




defined('_JEXEC') or die('Restricted access');




$path = $this->baseurl.'/templates/'.$this->template;
$height = $this->params->get('height');
$width = $this->params->get('width');
$showPathway = $this->params->get('showPathway');
$footer = $this->params->get('footer');
$copyright = $this->params->get('copyright');
$firstName = $this->params->get('firstName');
$secondName = $this->params->get('secondName');
$slogan = $this->params->get('slogan');
$show_effect_nav = $this->params->get('show_effect_nav');
$show_tooltips = $this->params->get('show_tooltips');
$background = $this->params->get('background');


if ($this->params->get('fontSize') == '') 
{
$fontSize ='13px';
} 
else 
{
$fontSize = $this->params->get('fontSize');
}



JHTML::_('behavior.mootools');



include_once(JPATH_ROOT . "/templates/" . $this->template . '/lib/php/layout.php');
?>



<?php echo '<?xml version="1.0" encoding="utf-8"?'.'>'; ?>



<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php echo $this->language; ?>" lang="<?php echo $this->language; ?>" dir="<?php echo $this->direction; ?>" >



<head>
<jdoc:include type="head" />

<!-- style sheet links -->
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/_system/css/general.css" type="text/css" />
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/css/main.css" type="text/css" />
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/css/color.css" type="text/css" />
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/css/nav.css" type="text/css" />
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/css/modules.css" type="text/css" />
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/css/typo.css" type="text/css" />
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/css/MenuMatic.css" type="text/css" />



<!-- CSS pour IE  -->



<!--[if lt IE 7]>
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/css/MenuMatic-ie6.css" type="text/css" />
<link rel="stylesheet" href="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/css/ie6.css" type="text/css" />
<![endif]-->


<?php if ($height == "fluid") : ?>


<script type="text/javascript">
window.addEvent('domready', function() {
	var hauteur = screen.height;
	


	$('left').setStyle('height', hauteur - 360);
	$('right').setStyle('height', hauteur - 530);
	$('main_content').setStyle('height', hauteur - 554);
	$('bottom_nav').setStyle('top', hauteur - 290);
	
});
</script>
<?php endif; ?>

<script type="text/javascript">
window.addEvent('domready', function() {
	var hauteur = screen.height;
	$('fond_right').setStyle('height', hauteur - 170);
	$('fond_left').setStyle('height', hauteur - 170);
});
</script>

<?php if ($show_effect_nav == '1') : ?>
<script src="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/lib/js/effect_nav.js"></script>
<?php endif; ?>
<?php if ($show_tooltips == '1') : ?>
<script src="<?php echo $this->baseurl ?>/templates/<?php echo $this->template ?>/lib/js/tooltips.js"></script>
<?php endif; ?>

<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-9658987-3']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>

</head>



<body <?php echo ('style="font-size:'.$fontSize.';"');?>>
<div id="fond_right" <?php if ($background != "none") : echo ('style="background: transparent url('.$this->baseurl.'/templates/'.$this->template.'/images/'.$background.'.jpg);"'); endif; ?>></div>
<div id="fond_left"></div>

<div id="wrapper" <?php echo ('style="width:'.$width.';"');?>>
	
	<div id="right" <?php if ($height != "fluid") : echo ('style="height:'.($height - 30).'px;"'); endif; ?> >
		
			<?php if($this->countModules('image')) : ?>
			<div id="image"  >    
				<jdoc:include type="modules" name="image" style="xhtml" />
			</div>
			
			<?php ; else : ?>			
			<!--  MAIN COMPONENT -->
			<div id="main_content " <?php if ($height != "fluid") : echo ('style="height:'.($height - 30 -2*12).'px;"'); endif; ?> >
				<div id="main_component">
				<?php if($showPathway==1) { ?>
					<div id="pathway">
					<jdoc:include type="modules" name="breadcrumb" />
					</div>
				<?php } ?>
                               
				<?php echo$copy; ?>
				<jdoc:include type="message" />
				<jdoc:include type="component" />
				</div>
			</div>
			<?php endif; ?>
<div id="logo">
                         <img align="right" src="/Dharug/default/filedown/images/banners/NPWS_logo.bmp" />
</div>			
	</div>
	
	<!--  LEFT-COLUMN -->
	<div id="left" <?php if ($height != "fluid") : echo ('style="height:'.($height + 110).'px;"'); endif; ?>>



		<a href="index.php">
		<div id="site_name">
			<h2><?php echo $firstName; ?><span><?php echo $secondName; ?></span></h2>
			<?php if($slogan != '') : ?><div id="slogan" ><?php echo $slogan; ?></div><?php endif; ?>
		</div>
		</a>

		<div id="menu">
			<?php if ($this->countModules( 'menu' )) : ?>
			<div id="nav_main">
				<jdoc:include type="modules" name="menu" style="xhtml" />
			</div>
			<?php endif; ?>		
			<div id="clr">

                         </div>
			<?php if($this->countModules('search')) : ?>
			<div id="search">
				<jdoc:include type="modules" name="search" />
			</div>
			<?php endif; ?>
		</div>
		
		<!-- 	Copyright & Syndicate	-->
		<div id="footer">
                        
			
			<?php if ($this->countModules( 'syndicate' )) : ?>
			<div id="syndicate">
				<jdoc:include type="modules" name="syndicate" style="xhtml" />
			</div>
			<?php endif; ?>				
					
		 <?php if ($footer == 1) : ?>
                        <div id="copyright"><?php  echo $copyright ;?></div>
                        <?php endif; ?>
              	
				
	
		</div>

            

	</div>

	</div>
	<!--	bottom nav	-->
        
	<?php if ($this->countModules( 'banner' )) : ?>
	<div id="bottom_nav" <?php if ($height != "fluid") : echo ('style="top:'.($height + 190).'px;"'); endif; ?>>
		<div class="float_right">
                <jdoc:include type="modules" name="banner" style="xhtml" />
<?php if ($this->countModules( 'bottom_nav' )) : ?>
		<jdoc:include type="modules" name="bottom_nav" style="xhtml" />
   <?php endif; ?>
		</div>
	</div>
        <?php endif; ?>
    
       
	
	
	
</div>

</body>
</html>
