


function sendArticleComment(articleId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();
    console.log(parentId);
    $.get('/article/add-article-comment', {
        article_comment: comment,
        article_id: articleId,
        parent_id: parentId
    }).then(res => {
        $('#comments_area').html(res);
        $('#commentText').val('');
        $('#parent_id').val('');

        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: "smooth"});
        } else {
            document.getElementById('comments_area').scrollIntoView({behavior: "smooth"});
        }
    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"});
}




function showLargeImage(imageSrc) {
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image_modal').attr('href', imageSrc);
}



function addProductToOrder(productId) {
    const productCount = $('#product_count').val();

    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount ).then(res => {
        console.log(res);
            Swal.fire({
                title: "اعلان",
                text: res.text,
                icon: res.icon,
                showCancelButton: false,
                confirmButtonText: res.confirm_button_text

              }).then(result => {
                if (result.isConfirmed && res.status === 'user_not_auth' ) {
                    window.location.href = '/login';
                }
              });
        
            }
       )}


function addProductToOrderList(productId) {
    
    $.get('/order/add-to-order?product_id=' + productId ).then(res => {
        console.log(res);
            Swal.fire({
                title: "اعلان",
                text: res.text,
                icon: res.icon,
                showCancelButton: false,
                confirmButtonText: res.confirm_button_text
    
                }).then(result => {
                    if (result.isConfirmed && res.status === 'user_not_auth' ) {
                        window.location.href = '/login';
                    }
                });
            
                }
        )}
        




function removeOrderDetail(detailId) {
    $.get('/User/remove-basket-detail?detail_id=' + detailId).then(res => {
    $('#order-detail-content').html(res.body)
});
}




//detail id  => order detail id product
//state => increase or decrease

// function changeOrderDetail(detailId, state) {
//     $.get('/User/change-basket-detail?detail_id=' + detailId + '&state=' + state).then(res => {
//         if (res.status === 'success') {
//             $('#order-detail-content').html(res.body);
//         }
//     });

// }





// function changeOrderDetailCount(detailId, state) {
//     $.get('/user/change-order-detail?detail_id=' + detailId + '&state=' + state).then(res => {
//         if (res.status === 'success') {
//             $('#order-detail-content').html(res.body);
//         }
//     });
// }


function changeOrderDetailCount(detailId, state) {
    $.ajax({
        url: '/user/change-order-detail',
        type: 'POST',
        data: {
            detail_id: detailId,
            state: state
        },
        success: function(response) {
            if (response.status === 'success') {
                $('#order-detail-content').html(response.body);
            }
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

