
<?php
// Protection contre les appels directs.
defined("_JEXEC") or die("Restricted access");



function modChrome_joomspirit($module, &$params, &$attribs) {

   	// init vars
	$showtitle = $module->showtitle;
	$content   = $module->content;
	$suffix    = '';
	$badge		='';

	// create title
	$pos   = JString::strpos($module->title, ' ');
	$title = ($pos !== false) ? '<span>'.JString::substr($module->title, 0, $pos).'</span>'.JString::substr($module->title, $pos) : $module->title;

  
	// force module type
	if ($module->position == 'left')  $suffix = 'color';
	

	// set module skeleton using the suffix
	switch ($suffix) {
		case 'default':
			$skeleton = 'white';
			break;
		case 'color':
			$skeleton = 'color';
			break;
		case 'blank':
		default:
			$skeleton = 'not defined';
	}

	// Modules
	switch ($skeleton) {
		case 'white':
			/*
			 * white rounded
			 */
			?>
			
			<div class="<?php echo $suffix; ?>">
				<div class="module <?php echo $attribs['class'] ?>">
					<div class="module-2">
						<div class="module-3">
							<div class="module-4 deepest">
								<div class="module-5">
									<?php if ($showtitle) : ?>
									<h3 class="module"><span class="module-2"><?php echo $title; ?></span></h3>
									<?php endif; ?>
								
									<?php echo $content; ?>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>
			<?php 
			break;
		
		case 'color':
			/*
			 * color rounded
			 */
			?>
			
			<div class="<?php echo $suffix; ?>">
				<div class="module <?php echo $attribs['class'] ?>">
					<div class="module-2">
						<div class="module-3">
							<div class="module-4 deepest">
								<?php if ($showtitle) : ?>
								<h3 class="module"><span class="module-2"><?php echo $title; ?></span></h3>
								<?php endif; ?>
								
								<?php echo $content; ?>
							</div>
						</div>
					</div>
				</div>
			</div>
			<?php 
			break;
				
		default:
			/*
			 * not defined
			 */
			?>
			<div class="module <?php echo $suffix; ?>">
				<?php if ($showtitle) : ?>
				<h3 class="module"><?php echo $title; ?></h3>
				<?php endif; ?>
			
				<?php echo $content; ?>
			</div>
			<?php 
			break;
	}
}
  
  
  

?>


