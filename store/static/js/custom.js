(function() {
	'use strict';

	var tinyslider = function() {
		var el = document.querySelectorAll('.testimonial-slider');

		if (el.length > 0) {
			var slider = tns({
				container: '.testimonial-slider',
				items: 1,
				axis: "horizontal",
				controlsContainer: "#testimonial-nav",
				swipeAngle: false,
				speed: 700,
				nav: true,
				controls: true,
				autoplay: true,
				autoplayHoverPause: true,
				autoplayTimeout: 3500,
				autoplayButtonOutput: false
			});
		}
	};
	tinyslider();

	


	var sitePlusMinus = function() {

		var value,
    		quantity = document.getElementsByClassName('quantity-container');

		let subtotalValue = document.getElementById('subtotal');
		let totalValue = document.getElementById('total');
		let discount = document.getElementById('coupon') || 0;

		function createBindings(quantityContainer, i) {
	      var quantityAmount = quantityContainer.getElementsByClassName('quantity-amount')[0];
	      var productPrice = document.getElementsByClassName('product-price-cart')[i];
	      var increase = quantityContainer.getElementsByClassName('increase')[0];
	      var decrease = quantityContainer.getElementsByClassName('decrease')[0];
		  var totalAmount = document.getElementById('total_amount')

		  productPrice = parseInt(productPrice.textContent.replace("$", ""));
	      increase.addEventListener('click', function (e) { increaseValue( quantityAmount, productPrice, totalAmount); });
	      decrease.addEventListener('click', function (e) { decreaseValue( quantityAmount, productPrice, totalAmount); });
	    }

	    function init() {
	        for (var i = 0; i < quantity.length; i++ ) {
				createBindings(quantity[i], i);
	        }
	    };

	    function increaseValue( quantityAmount, productPrice, totalAmount) {
	        value = parseInt(quantityAmount.value, 10);
	        value = isNaN(value) ? 0 : value;
	        value++;
			let amount = parseFloat(subtotalValue.textContent.replace(/[^0-9.-]+/g, ""));
			amount += productPrice*1000
			totalAmount.value = discount.value.length > 0  ? (amount*40)/100 : amount
			subtotalValue.innerText = `$${amount.toLocaleString('en-US',{ minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
			totalValue.innerText = discount.value.length > 0 ? `$${((amount*40)/100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2})}` : `$${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2})}`
	        quantityAmount.value = value;
	    }

	    function decreaseValue( quantityAmount, productPrice, totalAmount) {
	        value = parseInt(quantityAmount.value, 10);

	        value = isNaN(value) ? 0 : value;
	        if (value > 0) {
				value--;
				let amount = parseFloat(subtotalValue.textContent.replace(/[^0-9.-]+/g, ""));
				amount -= productPrice*1000
				totalAmount.value = discount.value.length > 0  ? (amount*40)/100 : amount
				subtotalValue.innerText = `$${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2})}`;
				totalValue.innerText = discount.value.length > 0 ? `$${((amount*40)/100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2})}` : `$${amount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2})}`
				
			}

	        quantityAmount.value = value;
	    }

	    
	    init();
		
	};
	sitePlusMinus();


})()

const images = document.querySelectorAll("img[name]");
images.forEach(image => {
  image.addEventListener("click", function(e) {
	e.preventDefault();
	const product = image.getAttribute("alt");
    window.location.href = `/product/${product}/add`
  });
});