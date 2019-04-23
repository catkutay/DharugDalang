window.addEvent('domready', function() {
	var Tips2 = new Tips($$('.tips'), {	initialize:function(){		this.fx = new Fx.Style(this.toolTip, 'opacity', {duration: 400, wait: false}).set(0);	},	onShow: function(toolTip) {		this.fx.start(1);	},	onHide: function(toolTip) {		this.fx.start(0);	}	});	
});
