$('.addToWishlist').click(function(e) {
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('.prod_id').val();
    var url = "/add-to-wishlist"
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'product_id': product_id }),
        }).then((response) => {
            return response.json()
        })
        .then((data) => {
            console.log('data', data)
            location.reload()
        })


})