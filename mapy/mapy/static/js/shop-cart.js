$(document).ready(()=>{
  $('.quantity').on('change',function(){
    $.ajax({
      type:'GET',
      url:'/update_item?id_item='+$(this).parent('div').find(".id_item").val()+'&&quatityItem='+$(this).val()
      ,success:function(request){
        $('#totalMoney').text('$ '+request['total']),
        $('#totalMoneyModePhone').text('$ '+request['total'])
      }
    })
  });

  $('.remove').on('click',function(){
    // This inside success references the request
    let divDelete = $(this).parent('div').parent('div')
    $.ajax({
      type:'GET',
      url:'/delete_item?id_item='+$(this).parent('div').find(".id_item").val()
      ,success:function(request){
        $('#totalMoney').text('$ '+request['total']),
        $('#totalMoneyModePhone').text('$ '+request['total']),
        $('#quantityModePhone').text(request['quantity'])
        divDelete.remove()
      }
    })
  });
})
