// cart management
const btn_increment = [...document.getElementsByClassName('btn-increment')]
const btn_decrement = [...document.getElementsByClassName('btn-decrement')]

const total_price = document.getElementById('total-price')
const shipping_charge = document.getElementById('shipping-charge')
const all_total = document.getElementById('all-total')





const session_cart_id =[...document.getElementsByClassName('session_cart_id')] 
console.log(session_cart_id[0].value)



// console.log(btn_increment.dataset.increment)
btn_increment.forEach(function(element){
    element.addEventListener('click',function(){
        let cart_id = element.dataset.id
        const count_value = document.getElementById('cart_id')
        const count = document.getElementById(`count-id-${cart_id}`)
        const price = document.getElementById(`price-${cart_id}`)
        // after the login we need to control the cart items thats why i take this 
        // product_id
        const product_id = document.getElementById(`cart-product-id-${cart_id}`)

        console.log(count.value)
        console.log(price.innerText)
        $.ajax({
            url: `increment/${cart_id}/`,
            type:'GET',
            data:{
                session_cart_id:session_cart_id[0].value,
                product_id: product_id.value
            },
            success:function(response){
                count.value = response.product_total_count
                count_value.innerHTML = response.all_cart_quantity
                price.innerText = '₹'+response.totalprice
                total_price.innerText = '₹'+response.all_total
                shipping_charge.innerText ='₹'+ response.shipping_charge
                all_total.innerText = '₹'+response.items_total
                },
            error: function(error){
                console.log(error)
            }
        })
 
    })
})


btn_decrement.forEach(function(element){
    element.addEventListener('click',function(){
        let cart_id = element.dataset.id
        const count_value = document.getElementById('cart_id')
        const count = document.getElementById(`count-id-${cart_id}`)
        const price = document.getElementById(`price-${cart_id}`)
        const row = document.getElementById(`cart_item_row_${cart_id}`)
        // after the login we need to control the cart items thats why i take this 
        // product_id
        const product_id = document.getElementById(`cart-product-id-${cart_id}`)
     
        $.ajax({
            url: `decrement/${cart_id}/`,
            type:'GET',
            data:{
                session_cart_id:session_cart_id[0].value,
                product_id: product_id.value
            },
            success:function(response){
                if (response.product_total_count==0){
                    row.style.display="none"
                }
                count.value = response.product_total_count
                price.innerText = '₹'+response.totalprice
                count_value.innerHTML = response.all_cart_quantity

                total_price.innerText = '₹'+response.all_total
                console.log(response.all_total,'this is all total')
                shipping_charge.innerText = '₹'+response.shipping_charge
                all_total.innerText = '₹'+response.items_total

                
                },
            error: function(error){
                console.log(error)
            }
        })

    })
})


$('.cart_delete').on('click',function(e){
    e.preventDefault();
    var self = $(this)
    console.log(self.data('title'))
    console.log(self.attr('href'))
    Swal.fire({
title: 'Are you sure?',
text: "You won't be able to revert this!",
icon: 'warning',
showCancelButton: true,
confirmButtonColor: '#3085d6',
cancelButtonColor: '#d33',
confirmButtonText: 'Yes, delete it!'
}).then((result) => {
if (result.isConfirmed) {
  Swal.fire(
    'Deleted!',
    'Your file has been deleted.',
    'success'
  )
  location.href = self.attr('href')
}
}) //
  })