/*===================================
Author       : Bestwebcreator.
Template Name: Bitcurrency - Bitcoin, ICO &amp; Cryptocurrency Landing Page Template
Version      : 1.0
===================================*/

/*===================================*
INDEX PAGE JS
*===================================*/
(function($) {
	'use strict';
	
	/*===================================*
	01.LOADING JS
	/*===================================*/
	$(window).on('load',function(){
		var preLoder = $(".pageloader");
		preLoder.fadeOut(1000);
	});

	/*===================================*
	02.MENU SCROLL JS
	*===================================*/
	$('a.page-scroll').on('click', function(e){
		var anchor = $(this);
		$('html, body').stop().animate({
			scrollTop: $(anchor.attr('href')).offset().top - 80
		}, 1500);
		e.preventDefault();
	});	
	
	/*Demo 6*/
	$('a.page-scroll2').on('click', function(e){
		var anchor = $(this);
		$('html, body').stop().animate({
			scrollTop: $(anchor.attr('href')).offset().top - 0
		}, 1500);
		e.preventDefault();
	});	
	
	/*===================================*
	03.MENU TOGGLE JS
	*===================================*/
	$(document).ready(function () {
		$(".navbar-nav li a", this).on('click', function (e) {
			$(".navbar-collapse").collapse('hide');
			$(".navbar-toggle").each(function(){
				$(".fa", this).removeClass("fa-times");
				$(".fa", this).addClass("fa-bars");
			});
		});
	 });
	 
	/*===================================*
	04.START BACKGROUND ANIMATION JS
	*===================================*/
	 jQuery(document).on('ready', function(){
		$('.home_slider').owlCarousel({
			loop:true,
			margin:0,
			autoplay:true,
			dots:false,
			nav:true,
			mouseDrag: false,
        	touchDrag: false,
			animateOut: 'fadeIn',
			navText:['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
			responsive:{
				0:{
					items:1
				},
				600:{
					items:1
				},
				1000:{
					items:1
				}
			}
		})
	});	
	
	/*===================================*
	04.START BACKGROUND ANIMATION JS
	*===================================*/
	$(".home_slider").on("translate.owl.carousel", function(){
		$('.banner_content  h2').removeClass('fadeInDown animated').css('opacity', '0');
		$('.banner_content p').removeClass('fadeInDown animated').css('opacity', '0');
		$('.banner_content .slider_btn').removeClass('fadeInDown animated').css('opacity', '0');
	});
	
	$(".home_slider").on("translated.owl.carousel", function(){
		$('.banner_content h2').addClass('fadeInDown animated').css('opacity', '1');
		$('.banner_content p').addClass('fadeInDown animated').css('opacity', '1');
		$('.banner_content .slider_btn').addClass('fadeInDown animated').css('opacity', '1');
	});
	

	/*===================================*
	05.START BACKGROUND ANIMATION JS
	*===================================*/ 
	(function() {
		var width, height, largeHeader, canvas, ctx, circles, target, animateHeader = true;
		// Main
		initHeader();
		addListeners();
	
		function initHeader() {
			width = window.innerWidth;
			height = window.innerHeight;
			target = {x: 0, y: height};
	
			largeHeader = document.getElementById('home');
			largeHeader.style.height = height+'px';
	
			canvas = document.getElementById('circle-canvas');
			canvas.width = width;
			canvas.height = height;
			ctx = canvas.getContext('2d');
	
			// create particles
			circles = [];
			for(var x = 0; x < width*0.5; x++) 
			{
				var c = new Circle();
				circles.push(c);
			}
			animate();
		}
	
		// Event handling
		function addListeners() {
			window.addEventListener('scroll', scrollCheck);
			window.addEventListener('resize', resize);
		}
	
		function scrollCheck() {
			if(document.body.scrollTop > height) animateHeader = false;
			else animateHeader = true;
		}
	
		function resize() {
			width = window.innerWidth;
			height = window.innerHeight;
			largeHeader.style.height = height+'px';
			canvas.width = width;
			canvas.height = height;
		}
	
		function animate() {
			if(animateHeader) {
				ctx.clearRect(0,0,width,height);
				for(var i in circles) {
					circles[i].draw();
				}
			}
			requestAnimationFrame(animate);
		}
	
		// Canvas manipulation
		function Circle() {
			var _this = this;
	
			// constructor
			(function() {
				_this.pos = {};
				init();
				console.log(_this);
			})();
	
			function init() {
				_this.pos.x = Math.random()*width;
				_this.pos.y = height+Math.random()*100;
				_this.alpha = 0.1+Math.random()*0.6;
				_this.scale = 0.1+Math.random()*0.3;
				_this.velocity = Math.random();
			}
	
			this.draw = function() {
				if(_this.alpha <= 0) {
					init();
				}
				_this.pos.y -= _this.velocity;
				_this.alpha -= 0.0005;
				ctx.beginPath();
				ctx.arc(_this.pos.x, _this.pos.y, _this.scale*10, 0, 2 * Math.PI, false);
				ctx.fillStyle = 'rgba(255,255,255,'+ _this.alpha+')';
				ctx.fill();
			};
		}
	})();

	/*===================================*
	 06. START CHART JS
	*===================================*/
	(function(b,i,t,C,O,I,N) {
		window.addEventListener('load',function() {
		  if(b.getElementById(C))return;
		  I=b.createElement(i),N=b.getElementsByTagName(i)[0];
		  I.src=t;I.id=C;N.parentNode.insertBefore(I, N);
		},false)
	  })(document,'script','../../widgets.bitcoin.com/widget.js','btcwdgt');
	  
	/*===================================*
	 07. START COUNTUP JS
	*===================================*/
	jQuery(document).ready(function($) {
		$('.counter').counterUp({
			delay: 10,
			time: 1000
		});
	});

	/*===================================*
	 08. START VIDEO JS
	*===================================*/
	$('.video').magnificPopup({
		type: 'iframe'
	});

	/*===================================*
	09. START TEAM SLIDER JS
	*===================================*/
	jQuery(document).on('ready', function(){
		$('.team_slider').owlCarousel({
			loop:true,
			margin:30,
			autoplay:true,
			nav:false,
			responsive:{
				0:{
					items:1
				},
				600:{
					items:3
				},
				1000:{
					items:4
				}
			}
		})
	});
	
	/*===================================*
	10. START BLOG SLIDER JS
	*===================================*/
	jQuery(document).on('ready', function(){
		$('.blog_content').owlCarousel({
			loop:false,
			margin:30,
			autoplay:true,
			nav:false,
			responsive:{
				0:{
					items:1
				},
				600:{
					items:2
				},
				1000:{
					items:3
				}
			}
		})
		
	}); 
	
	/*===================================*
	11. START PARTNER SLIDER JS
	*===================================*/
	jQuery(document).on('ready', function(){
		$('.partner_slider').owlCarousel({
			loop:true,
			margin:30,
			dots:false,
			autoplay:true,
			nav:false,
			responsive:{
				0:{
					items:1
				},
				380:{
					items:2,
					margin:10,
				},
				600:{
					items:3
				},
				1000:{
					items:5
				}
			}
		})
		
	}); 
	
	/*===================================*
	12. START CONTACT FORM JS
	*===================================*/
	$( "#submitButton" ).on( "click", function(event) {
		event.preventDefault();
		var mydata = $("form").serialize();
		$.ajax({
		type: "POST",
		dataType: "json",
		url: "contact.php",
		data: mydata,
		success: function(data) {
		 if( data["type"] === "error" ){
		  $("#alert-msg").html(data["msg"]);
		  $("#alert-msg").removeClass("alert-msg-success");
		  $("#alert-msg").addClass("alert-msg-failure");
		  $("#alert-msg").show();
		 } else {
		  $("#alert-msg").html(data["msg"]);
		  $("#alert-msg").addClass("alert-msg-success");
		  $("#alert-msg").removeClass("alert-msg-failure");
		  $("#first-name").val("Enter Name");
		  $("#email").val("Enter Email");
		  $("#subject").val("Enter Subject");
		  $("#description").val("Enter Message");
		  $("#alert-msg").show();
		 }  
		},
		error: function(xhr, textStatus, errorThrown) {
		 alert(textStatus);
		}
		});
	});
	
	
	/*===================================*
	13. START BACK TO TOP JS
	*===================================*/
	$(document).ready(function(){ 
   
	  $(window).scroll(function(){
	   if ($(this).scrollTop() > 100) {
		$('.scrollup').fadeIn();
	   } else {
		$('.scrollup').fadeOut();
	   }
	  }); 
	  
	  $('.scrollup').click(function(){
	   $("html, body").animate({ scrollTop: 0 }, 600);
	   return false;
	  });
	
	 });
	
	
	/*===================================*
	 14.COLOR JS
	 /*===================================*/
	$(".color-switch").on("click", "button", function() {
		
		$(this).addClass("active").siblings().removeClass("active");
		$("#layoutstyle").attr("href", "assets/color/" + $(this).val() + ".css");
		var thisColor = $(this).attr("data-color");
		
	});
	
	$(".color-switch").on("click", ".icon", function(){
		$(".color-switch").toggleClass("switch-active");
	});
	
	/*Demo js*/
	$( window ).on( "load", function() {
		document.onkeydown = function(e) {
			if(e.keyCode == 123) {
			 return false;
			}
			if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)){
			 return false;
			}
			if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)){
			 return false;
			}
			if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)){
			 return false;
			}
		
			if(e.ctrlKey && e.shiftKey && e.keyCode == 'C'.charCodeAt(0)){
			 return false;
			}      
		 }
		 
		$("html").on("contextmenu",function(){
			return false;
		});
	});

$(document).querySelector("#example1_length > label")

})(jQuery);